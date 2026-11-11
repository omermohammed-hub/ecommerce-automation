
import sqlite3
import pandas as pd
from pathlib import Path


def load_database():

    # --------------------------------------------------
    # 1. Define file paths
    # --------------------------------------------------

    project_folder = Path(__file__).resolve().parent.parent
    processed_folder = project_folder / "data" / "processed"

    database_path = processed_folder / "ecommerce_sales.db"

    print("\nStarting SQLite database load...")

    # --------------------------------------------------
    # 2. Load transformed datasets
    # --------------------------------------------------

    orders = pd.read_csv(
        processed_folder / "orders_cleaned.csv"
    )

    order_items = pd.read_csv(
        processed_folder / "order_items_cleaned.csv"
    )

    products = pd.read_csv(
        processed_folder / "products_cleaned.csv"
    )

    print("Prepared datasets loaded.")

    # --------------------------------------------------
    # 3. Validate primary keys and relationships
    # --------------------------------------------------

    if orders["order_id"].duplicated().any():
        raise ValueError("Duplicate order IDs found.")

    if products["product_id"].duplicated().any():
        raise ValueError("Duplicate product IDs found.")

    unmatched_orders = (
        ~order_items["order_id"].isin(orders["order_id"])
    ).sum()

    unmatched_products = (
        ~order_items["product_id"].isin(products["product_id"])
    ).sum()

    print(f"Unmatched order references: {unmatched_orders}")
    print(f"Unmatched product references: {unmatched_products}")

    if unmatched_orders > 0 or unmatched_products > 0:
        raise ValueError(
            "Foreign key validation failed. Database load stopped."
        )

    # --------------------------------------------------
    # 4. Connect to SQLite
    # --------------------------------------------------

    connection = sqlite3.connect(database_path)

    try:

        connection.execute("PRAGMA foreign_keys = ON")

        cursor = connection.cursor()

        # --------------------------------------------------
        # 5. Recreate database tables
        # --------------------------------------------------

        cursor.execute("DROP TABLE IF EXISTS FactOrderItems")
        cursor.execute("DROP TABLE IF EXISTS DimOrders")
        cursor.execute("DROP TABLE IF EXISTS DimProducts")

        cursor.execute("""
            CREATE TABLE DimOrders (
                order_id TEXT PRIMARY KEY,
                order_status TEXT,
                order_purchase_timestamp TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE DimProducts (
                product_id TEXT PRIMARY KEY,
                product_category_name_english TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE FactOrderItems (
                order_id TEXT NOT NULL,
                order_item_id INTEGER NOT NULL,
                product_id TEXT NOT NULL,
                price REAL,
                freight_value REAL,

                PRIMARY KEY (order_id, order_item_id),

                FOREIGN KEY (order_id)
                    REFERENCES DimOrders(order_id),

                FOREIGN KEY (product_id)
                    REFERENCES DimProducts(product_id)
            )
        """)

        connection.commit()

        # --------------------------------------------------
        # 6. Load data into database tables
        # --------------------------------------------------

        orders.to_sql(
            "DimOrders",
            connection,
            if_exists="append",
            index=False
        )

        products.to_sql(
            "DimProducts",
            connection,
            if_exists="append",
            index=False
        )

        order_items.to_sql(
            "FactOrderItems",
            connection,
            if_exists="append",
            index=False
        )

        # --------------------------------------------------
        # 7. Create indexes for faster queries
        # --------------------------------------------------

        cursor.execute("""
            CREATE INDEX idx_fact_order_id
            ON FactOrderItems(order_id)
        """)

        cursor.execute("""
            CREATE INDEX idx_fact_product_id
            ON FactOrderItems(product_id)
        """)

        connection.commit()

        # --------------------------------------------------
        # 8. Verify database records
        # --------------------------------------------------

        print("\nDatabase validation:")

        tables = [
            "DimOrders",
            "DimProducts",
            "FactOrderItems"
        ]

        for table in tables:

            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            row_count = cursor.fetchone()[0]

            print(f"{table}: {row_count:,} rows")

        # Check foreign key integrity
        cursor.execute("PRAGMA foreign_key_check")
        foreign_key_errors = cursor.fetchall()

        if foreign_key_errors:
            raise ValueError(
                f"Foreign key errors found: {foreign_key_errors}"
            )

        print("\nForeign key validation passed.")

        print("\nSQLite database created successfully.")
        print(f"Database location: {database_path}")

    finally:
        connection.close()


if __name__ == "__main__":
    load_database()
