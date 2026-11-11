
import pandas as pd
from pathlib import Path


def transform_data():

    # --------------------------------------------------
    # 1. Define project folders
    # --------------------------------------------------

    project_folder = Path(__file__).resolve().parent.parent

    raw_folder = project_folder / "data" / "raw"
    processed_folder = project_folder / "data" / "processed"

    processed_folder.mkdir(parents=True, exist_ok=True)

    print("\nStarting data transformation...")

    # --------------------------------------------------
    # 2. Load source datasets
    # --------------------------------------------------

    orders = pd.read_csv(raw_folder / "olist_orders_dataset.csv")
    order_items = pd.read_csv(raw_folder / "olist_order_items_dataset.csv")
    products = pd.read_csv(raw_folder / "olist_products_dataset.csv")
    translations = pd.read_csv(
        raw_folder / "product_category_name_translation.csv"
    )

    print("All source datasets loaded.")

    # --------------------------------------------------
    # 3. Select required columns
    # --------------------------------------------------

    orders = orders[
        [
            "order_id",
            "order_status",
            "order_purchase_timestamp"
        ]
    ].copy()

    order_items = order_items[
        [
            "order_id",
            "order_item_id",
            "product_id",
            "price",
            "freight_value"
        ]
    ].copy()

    products = products[
        [
            "product_id",
            "product_category_name"
        ]
    ].copy()

    translations = translations[
        [
            "product_category_name",
            "product_category_name_english"
        ]
    ].copy()

    # --------------------------------------------------
    # 4. Transform orders
    # --------------------------------------------------

    orders["order_purchase_timestamp"] = pd.to_datetime(
        orders["order_purchase_timestamp"],
        errors="coerce"
    )

    # --------------------------------------------------
    # 5. Transform order items
    # --------------------------------------------------

    order_items["price"] = pd.to_numeric(
        order_items["price"],
        errors="coerce"
    )

    order_items["freight_value"] = pd.to_numeric(
        order_items["freight_value"],
        errors="coerce"
    )

    # --------------------------------------------------
    # 6. Translate product categories into English
    # --------------------------------------------------

    # Ensure each Portuguese category has at most one translation
    if translations["product_category_name"].duplicated().any():
        raise ValueError("Duplicate category names found in translation file.")

    products = products.merge(
        translations,
        on="product_category_name",
        how="left",
        validate="many_to_one"
    )

    # Use Unknown when a category has no English translation
    products["product_category_name_english"] = (
        products["product_category_name_english"].fillna("Unknown")
    )

    # Keep only the fields needed for product analysis
    products = products[
        [
            "product_id",
            "product_category_name_english"
        ]
    ].copy()

    # --------------------------------------------------
    # 7. Data quality checks
    # --------------------------------------------------

    print("\nRunning data quality checks...")

    # Check primary key uniqueness
    if orders["order_id"].duplicated().any():
        raise ValueError("Duplicate order IDs found.")

    if products["product_id"].duplicated().any():
        raise ValueError("Duplicate product IDs found.")

    # Check missing key fields
    if orders["order_id"].isna().any():
        raise ValueError("Missing order IDs found.")

    if order_items[
        ["order_id", "order_item_id", "product_id"]
    ].isna().any().any():
        raise ValueError("Missing key fields found in order items.")

    if products["product_id"].isna().any():
        raise ValueError("Missing product IDs found.")

    # Report unmatched product references
    unmatched_products = (
        ~order_items["product_id"].isin(products["product_id"])
    ).sum()

    # Report missing or invalid values
    invalid_timestamps = orders["order_purchase_timestamp"].isna().sum()
    missing_prices = order_items["price"].isna().sum()
    missing_freight = order_items["freight_value"].isna().sum()
    unknown_categories = (
        products["product_category_name_english"] == "Unknown"
    ).sum()

    print(f"Invalid or missing order timestamps: {invalid_timestamps}")
    print(f"Missing or invalid prices: {missing_prices}")
    print(f"Missing or invalid freight values: {missing_freight}")
    print(f"Products with unknown categories: {unknown_categories}")
    print(f"Order items referencing unmatched products: {unmatched_products}")

    # --------------------------------------------------
    # 8. Save transformed datasets
    # --------------------------------------------------

    orders.to_csv(
        processed_folder / "orders_cleaned.csv",
        index=False
    )

    order_items.to_csv(
        processed_folder / "order_items_cleaned.csv",
        index=False
    )

    products.to_csv(
        processed_folder / "products_cleaned.csv",
        index=False
    )

    # --------------------------------------------------
    # 9. Transformation summary
    # --------------------------------------------------

    print("\nTransformation completed successfully.")

    print("\nOutput datasets:")
    print(f"Orders: {len(orders):,} rows")
    print(f"Order items: {len(order_items):,} rows")
    print(f"Products: {len(products):,} rows")

    print(f"\nFiles saved in: {processed_folder}")


if __name__ == "__main__":
    transform_data()
