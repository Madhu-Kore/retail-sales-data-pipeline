from pyspark.sql import functions as F


def validate_customers(customers):
    if customers.filter(F.col("customer_id").isNull()).count() > 0:
        raise ValueError("validation failed: customer_id contains null values")

    if customers.groupBy("customer_id").count().filter(F.col("count") > 1).count() > 0:
        raise ValueError("validation failed: customer_id contains duplicates")
    
    return True


def validate_products(products):

    if products.filter(F.col("product_id").isNull()).count() > 0:
        raise ValueError("validation failed: product_id contains null values")
    
    if products.groupby("product_id").count().filter(F.col("count") > 1).count() > 0:
        raise ValueError("validation failed: product_id contains duplicates")
    
    if products.filter(F.col("unit_cost") <= 0).count() > 0:
        raise ValueError("validation failed: unit_cost must be greater than 0")
    
    if products.filter(F.col("unit_price") < 0).count() > 0:
        raise ValueError("validation failed: unit_price must be greater than or equal to 0")
    
    return True


def validate_sales(sales, customers, products):

    if sales.filter(F.col("order_id").isNull()).count() > 0:
        raise ValueError("validation failed: order_id contains null values")
    
    if sales.groupby("order_id").count().filter(F.col("count") > 1).count() > 0:
        raise ValueError("validation failed: order_id contains duplicates")

    if sales.filter(F.col("customer_id").isNull()).count() > 0:
        raise ValueError("validation failed: customer_id contains null values")

    if sales.filter(F.col("product_id").isNull()).count() > 0:
        raise ValueError("validation failed: product_id contains null values")

    if sales.filter(F.col("quantity") <= 0 ).count() > 0:
        raise ValueError("validation failed: quantity must be greater than 0")
    
    if sales.filter(F.col("order_date").isNull()).count() > 0:
        raise ValueError("validation failed: order_date cannot contain null values")
    
    if sales.join(customers, on="customer_id", how="left_anti").count() > 0:
        raise ValueError("validation failed: one or more customer_ids do not exist in customers")
    
    if sales.join(products, on="product_id", how="left_anti").count() > 0:
        raise ValueError("validation failed: one or more product_ids do not exist in products")

    return True
