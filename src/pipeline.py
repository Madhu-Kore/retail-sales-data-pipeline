
from pyspark.sql import SparkSession

from spark_validation import (
    validate_customers,
    validate_products,
    validate_sales
)

from schemas import (
    customer_schema,
    product_schema,
    sale_schema
)

spark = (
        SparkSession.builder
        .appName("Retail Sales Pipeline")
        .master("local[*]")
        .getOrCreate()
        )


customers = spark.read.schema(customer_schema).csv("data/raw/customers.csv", header=True)
products = spark.read.schema(product_schema).csv("data/raw/products.csv", header=True)
sales = spark.read.schema(sale_schema).csv("data/raw/sales.csv", header=True)


customers.printSchema()
products.printSchema()
sales.printSchema()

customers.show(5)
products.show(5)
sales.show(5)


print(validate_customers(customers))
print(validate_products(products))
print(validate_sales(sales, customers, products))

spark.stop()