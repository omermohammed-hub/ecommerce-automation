
import sqlite3
from pathlib import Path
import pandas as pd


def validate_database():

    # Locate database
    project_folder = Path(__file__).resolve().parent.parent
    database_path = (
        project_folder / "data" / "processed" / "ecommerce_sales.db"
    )

    connection = sqlite3.connect(database_path)

    try:

        print("\n" + "=" * 55)
        print("ECOMMERCE SALES DATABASE - SQL VALIDATION")
        print("=" * 55)

        # --------------------------------------------------
        # 1. Order status breakdown
        # --------------------------------------------------

        print("\n1. ORDER STATUS BREAKDOWN")

        query = """
            SELECT
                order_status,
                COUNT(*) AS total_orders
            FROM DimOrders
            GROUP BY order_status
            ORDER BY total_orders DESC
        """

        result = pd.read_sql_query(query, connection)
        print(result.to_string(index=False))

        # --------------------------------------------------
        # 2. Overall delivered sales KPIs
        # --------------------------------------------------

        print("\n2. DELIVERED SALES PERFORMANCE")

        query = """
            SELECT
                COUNT(DISTINCT o.order_id) AS delivered_orders,
                COUNT(*) AS items_sold,
                ROUND(SUM(i.price), 2) AS item_revenue,
                ROUND(SUM(i.freight_value), 2) AS freight_value,
                ROUND(
                    SUM(i.price) / COUNT(DISTINCT o.order_id),
                    2
                ) AS average_order_value

            FROM DimOrders o

            INNER JOIN FactOrderItems i
                ON o.order_id = i.order_id

            WHERE o.order_status = 'delivered'
        """

        result = pd.read_sql_query(query, connection)
        print(result.to_string(index=False))

        # --------------------------------------------------
        # 3. Monthly delivered sales
        # --------------------------------------------------

        print("\n3. MONTHLY DELIVERED SALES")

        query = """
            SELECT
                strftime(
                    '%Y-%m',
                    o.order_purchase_timestamp
                ) AS sales_month,

                COUNT(DISTINCT o.order_id) AS total_orders,
                COUNT(*) AS items_sold,
                ROUND(SUM(i.price), 2) AS item_revenue,
                ROUND(SUM(i.freight_value), 2) AS freight_value

            FROM DimOrders o

            INNER JOIN FactOrderItems i
                ON o.order_id = i.order_id

            WHERE o.order_status = 'delivered'

            GROUP BY sales_month
            ORDER BY sales_month
        """

        result = pd.read_sql_query(query, connection)
        print(result.to_string(index=False))

        # --------------------------------------------------
        # 4. Revenue by product category
        # --------------------------------------------------

        print("\n4. REVENUE BY PRODUCT CATEGORY")

        query = """
            SELECT
                p.product_category_name_english AS category,
                COUNT(*) AS items_sold,
                ROUND(SUM(i.price), 2) AS item_revenue

            FROM FactOrderItems i

            INNER JOIN DimOrders o
                ON i.order_id = o.order_id

            INNER JOIN DimProducts p
                ON i.product_id = p.product_id

            WHERE o.order_status = 'delivered'

            GROUP BY p.product_category_name_english
            ORDER BY item_revenue DESC
        """

        result = pd.read_sql_query(query, connection)
        print(result.to_string(index=False))

        # --------------------------------------------------
        # 5. Top 10 categories by revenue
        # --------------------------------------------------

        print("\n5. TOP 10 PRODUCT CATEGORIES")

        query = """
            SELECT
                p.product_category_name_english AS category,
                ROUND(SUM(i.price), 2) AS item_revenue

            FROM FactOrderItems i

            INNER JOIN DimOrders o
                ON i.order_id = o.order_id

            INNER JOIN DimProducts p
                ON i.product_id = p.product_id

            WHERE o.order_status = 'delivered'

            GROUP BY p.product_category_name_english
            ORDER BY item_revenue DESC
            LIMIT 10
        """

        result = pd.read_sql_query(query, connection)
        print(result.to_string(index=False))

        print("\n" + "=" * 55)
        print("SQL VALIDATION COMPLETED")
        print("=" * 55)

    finally:
        connection.close()


if __name__ == "__main__":
    validate_database()
