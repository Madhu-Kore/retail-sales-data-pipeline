
from pyspark.sql import SparkSession

from pyspark.sql.types import(
    StructType,
    StructField,
    IntegerType,
    StringType,
    DecimalType,
    DateType
)

spark = (
        SparkSession.builder
        .appName("Retail Sales Pipeline")
        .master("local[*]")
        .getOrCreate()
        )



customer_schema = StructType(
    [
    StructField("customer_id", IntegerType(), nullable=False),
    StructField("customer_name", StringType(), nullable= False),
    StructField("segment", StringType(), nullable=False),
    StructField("city", StringType(), nullable=False),
    StructField("state", StringType(), nullable=False),
    StructField("region", StringType(), nullable=False)
    ]
)

product_schema = StructType(
    [
        StructField("product_id", IntegerType(), nullable=False),
        StructField("product_name", StringType(), nullable=False),
        StructField("category", StringType(), nullable=False),
        StructField("unit_cost", DecimalType(10,2), nullable=False),
        StructField("unit_price", DecimalType(10,2), nullable=False)
    ]
)

sale_schema = StructType(
    [
        StructField("order_id", IntegerType(), nullable=False),
        StructField("order_date", DateType(), nullable=False),
        StructField("customer_id", IntegerType(), nullable=False),
        StructField("product_id", IntegerType(), nullable=False),
        StructField("quantity", IntegerType(), nullable=False),
        StructField("discount", DecimalType(4,2), nullable=False),
        StructField("sales_amount", DecimalType(10,2), nullable=False)
    ]
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

spark.stop()