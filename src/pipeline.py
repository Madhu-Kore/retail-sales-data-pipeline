from pathlib import Path
from pyspark.sql import SparkSession, functions as F

RAW = Path("data/raw")
OUT = Path("data/processed")

def main():
    spark = (
        SparkSession.builder
        .appName("RetailSalesPipeline")
        .master("local[*]")
        .getOrCreate()
    )

    customers = spark.read.option("header", True).option("inferSchema", True).csv(str(RAW / "customers.csv"))
    products = spark.read.option("header", True).option("inferSchema", True).csv(str(RAW / "products.csv"))
    sales = spark.read.option("header", True).option("inferSchema", True).csv(str(RAW / "sales.csv"))

    dim_customer = customers.dropDuplicates(["customer_id"]).filter(F.col("customer_id").isNotNull())
    dim_product = products.dropDuplicates(["product_id"]).filter(F.col("product_id").isNotNull())

    fact_sales = (
        sales.withColumn("order_date", F.to_date("order_date"))
        .filter((F.col("quantity") > 0) & (F.col("sales_amount") >= 0))
        .join(dim_product.select("product_id", "unit_cost"), "product_id", "left")
        .withColumn("cost_amount", F.round(F.col("quantity") * F.col("unit_cost"), 2))
        .withColumn("profit_amount", F.round(F.col("sales_amount") - F.col("cost_amount"), 2))
        .withColumn("date_key", F.date_format("order_date", "yyyyMMdd").cast("int"))
        .drop("unit_cost")
    )

    dim_date = (
        fact_sales.select("order_date").distinct()
        .withColumn("date_key", F.date_format("order_date", "yyyyMMdd").cast("int"))
        .withColumn("year", F.year("order_date"))
        .withColumn("quarter", F.quarter("order_date"))
        .withColumn("month", F.month("order_date"))
        .withColumn("month_name", F.date_format("order_date", "MMMM"))
    )

    for name, df in {
        "dim_customer": dim_customer,
        "dim_product": dim_product,
        "dim_date": dim_date,
        "fact_sales": fact_sales
    }.items():
        df.write.mode("overwrite").parquet(str(OUT / name))
        print(f"Wrote {name}: {df.count()} rows")

    spark.stop()

if __name__ == "__main__":
    main()
