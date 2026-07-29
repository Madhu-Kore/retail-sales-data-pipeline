from pathlib import Path
import duckdb

def main():
    con = duckdb.connect("retail_warehouse.duckdb")
    for table in ["dim_customer", "dim_product", "dim_date", "fact_sales"]:
        con.execute(f"""
            CREATE OR REPLACE TABLE {table} AS
            SELECT * FROM read_parquet('data/processed/{table}/*.parquet')
        """)
        count = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"Loaded {table}: {count} rows")

    con.execute(Path("sql/analytics_views.sql").read_text())
    con.close()
    print("Created retail_warehouse.duckdb")

if __name__ == "__main__":
    main()
