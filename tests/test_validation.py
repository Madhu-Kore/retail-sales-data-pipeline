# from decimal import Decimal

# from datetime import date


# test_customer_schema = StructType(
#     [
#         StructField("customer_id", IntegerType(), nullable=True),
#         StructField("customer_name", StringType(), nullable=True),
#         StructField("segment", StringType(), nullable=True),
#         StructField("city", StringType(), nullable=True),
#         StructField("state", StringType(), nullable=True),
#         StructField("region", StringType(), nullable=True)
#     ]
# )

# test_products_schema = StructType(
#     [
#         StructField("product_id", IntegerType(), nullable=True),
#         StructField("product_name", StringType(), nullable=True),
#         StructField("category", StringType(), nullable=True),
#         StructField("unit_cost", DecimalType(10,2), nullable=True),
#         StructField("unit_price", DecimalType(10,2), nullable=True)
#     ]
# )

# test_sales_schema = StructType(
#     [
#     StructField("order_id", IntegerType(), nullable=True),
#     StructField("order_date", DateType(), nullable=True),
#     StructField("customer_id", IntegerType(), nullable=True),
#     StructField("product_id", IntegerType(), nullable=True),
#     StructField("quantity", IntegerType(), nullable=True),
#     StructField("discount", DecimalType(4, 2), nullable=True),
#     StructField("sales_amount", DecimalType(10, 2), nullable=True),
#     ]
# )



# bad_customers = spark.createDataFrame(
#     [
#         (1, "Customer 1", "Consumer", "Tampa", "FL", "South"),
#         (None, "Customer 2", "Consumer", "Miami", "FL", "South"),
#     ],
#     test_customer_schema
# )

# print(validate_customers(bad_customers))

# duplicate_customers = spark.createDataFrame(
#     [
#         (1, "Customer 1", "Consumer", "Tampa", "FL", "South"),
#         (1, "Customer 2", "Consumer", "Miami", "FL", "South"),
#     ],
#     test_customer_schema
# )

# print(validate_customers(duplicate_customers))


# bad_products = spark.createDataFrame(
#     [
#         (1, "Notebook", "Office Supplies", Decimal("10.00"), Decimal("15.00")),
#         (None, "Keyboard", "Electronics", Decimal("20.00"), Decimal("30.00"))
#     ],
#     test_products_schema
# )
# print(validate_products(bad_products))

# duplicate_products = spark.createDataFrame(
#     [
#         (1, "Notebook", "Office Supplies", Decimal("10.00"), Decimal("15.00")),
#         (1, "Keyboard", "Electronics", Decimal("20.00"), Decimal("30.00")),
#     ],
#     test_products_schema
# )
# print(validate_products(duplicate_products))

# bad_cost_products = spark.createDataFrame(
#     [
#         (1, "Notebook", "Office Supplies", Decimal("0.00"), Decimal("15.00")),
#         (2, "Keyboard", "Electronics", Decimal("20.00"), Decimal("30.00")),
#     ],
#     test_products_schema
# )
# print(validate_products(bad_cost_products))

# bad_price_products = spark.createDataFrame(
#     [
#         (1, "Notebook", "Office Supplies", Decimal("10.00"), Decimal("-1.00")),
#         (2, "Keyboard", "Electronics", Decimal("20.00"), Decimal("30.00")),
#     ],
#     test_products_schema
# )
# print(validate_products(bad_price_products))

# bad_sales_null_order = spark.createDataFrame(
#     [
#         (1, date(2026, 8, 19), 1, 1, 2, Decimal("0.00"), Decimal("30.00")),
#         (None, date(2026, 8, 19), 2, 2, 1, Decimal("0.05"), Decimal("20.00"))
#     ],
#     test_sales_schema
# )

# print(validate_sales(bad_sales_null_order, customers, products))

# duplicate_sales = spark.createDataFrame(
#     [
#         (1, date(2026, 8, 19), 1, 1, 2, Decimal("0.00"), Decimal("30.00")),
#         (1, date(2026, 8, 19), 2, 2, 1, Decimal("0.05"), Decimal("20.00")),
#     ],
#     test_sales_schema
# )

# print(validate_sales(duplicate_sales, customers, products))

# sales_null_customer_id = spark.createDataFrame(
#     [
#         (1, date(1997, 6, 11), 123, 23, 5, Decimal("10.0"), Decimal("40.0")),
#         (2, date(1997, 6,12), None, 23, 5, Decimal("5.0"), Decimal("30.0"))
#     ],
#     test_sales_schema
# )

# print(validate_sales(sales_null_customer_id, customers, products))

# sales_null_product_id = spark.createDataFrame(
#     [
#         (1, date(1997, 6, 11), 123, 23, 5, Decimal("10.0"), Decimal("40.0")),
#         (2, date(1997, 6,12), 124, None, 5, Decimal("5.0"), Decimal("30.0"))
#     ],
#     test_sales_schema
# )

# print(validate_sales(sales_null_product_id, customers, products))

# sales_invalid_quantity = spark.createDataFrame(
#     [
#         (1, date(1997, 6, 11), 123, 23, 5, Decimal("0.10"), Decimal("40.00")),
#         (2, date(1997, 6, 12), 124, 24, 0, Decimal("0.05"), Decimal("30.00")),
#     ],
#     test_sales_schema
# )

# print(validate_sales(sales_invalid_quantity, customers, products))

# sales_null_order_date = spark.createDataFrame(
#     [
#         (1, date(1997, 6, 11), 123, 23, 5, Decimal("0.10"), Decimal("40.00")),
#         (2, None, 124, 24, 5, Decimal("0.05"), Decimal("30.00")),
#     ],
#     test_sales_schema
# )

# print(validate_sales(sales_null_order_date, customers, products))

# sales_invalid_customer_fk = spark.createDataFrame(
#     [
#         (1, date(1997, 6, 11), 123, 23, 5, Decimal("0.10"), Decimal("40.00")),
#         (2, date(1997, 6, 12), 99999, 24, 5, Decimal("0.05"), Decimal("30.00")),
#     ],
#     test_sales_schema
# )

# print(validate_sales(sales_invalid_customer_fk, customers, products))

# sales_invalid_product_fk = spark.createDataFrame(
#     [
#         (1, date(1997, 6, 11), 123, 23, 5, Decimal("0.10"), Decimal("40.00")),
#         (2, date(1997, 6, 12), 124, 99999, 5, Decimal("0.05"), Decimal("30.00")),
#     ],
#     test_sales_schema
# )

# print(validate_sales(sales_invalid_product_fk, customers, products))
