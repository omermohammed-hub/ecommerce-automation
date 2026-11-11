
import subprocess
from pathlib import Path


def extract_data():

    # Kaggle dataset details
    dataset = "olistbr/brazilian-ecommerce"

    # Project directories
    project_folder = Path(__file__).resolve().parent.parent
    raw_folder = project_folder / "data" / "raw"

    # Create raw folder if it doesn't exist
    raw_folder.mkdir(parents=True, exist_ok=True)

    # Check whether our four required source files already exist
    required_files = [
        "olist_orders_dataset.csv",
        "olist_order_items_dataset.csv",
        "olist_products_dataset.csv",
        "product_category_name_translation.csv"
    ]

    missing_files = [
        file for file in required_files
        if not (raw_folder / file).exists()
    ]

    if not missing_files:
        print("Required Kaggle source files already exist.")
        print("Skipping download.")
        return

    print("Downloading Olist dataset from Kaggle...")

    command = [
        "kaggle",
        "datasets",
        "download",
        "-d", dataset,
        "-p", str(raw_folder),
        "--unzip",
        "--force"
    ]

    subprocess.run(command, check=True)

    print("\nKaggle extraction completed.")

    # Verify required files
    for file in required_files:

        file_path = raw_folder / file

        if file_path.exists():
            print(f"Found: {file}")
        else:
            raise FileNotFoundError(
                f"Required dataset file missing: {file}"
            )

    print("\nData extraction successful!")


if __name__ == "__main__":
    extract_data()
