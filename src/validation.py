
def validate_customers(df):

    # check for null customer ID's
    if df["customer_id"].isnull().any():
        raise ValueError("validation failed: customer_id contains null values.")
    
    # check for duplicate customer ID's
    if not df["customer_id"].is_unique:
        raise ValueError("validation failed: duplicate customer_id's found.")
    
    return True

def validate_products(df):

    # check for null product ID's
    if df["product_id"].isnull().any():
        raise ValueError("validation failed: product_id contains null values")
    
    # check for duplicate product ID's
    if not df["product_id"].is_unique:
        raise ValueError("validation failed: product_id contains duplicates")
    
    # check for negative unit costs
    if (df["unit_cost"] <= 0).any():
        raise ValueError("validation failed: unit_cost must be greater than 0")
    
    # check for negative unit price
    if (df["unit_price"] < 0).any():
        raise ValueError("validation failed: unit_price cannot be negative")
    
    return True

def validate_sales(sales_df, customers_df, products_df):
    # check if all customer_id's exist in customer table 
    if (~(sales_df["customer_id"].isin(customers_df["customer_id"]))).any():
        raise ValueError("validation failed: one or more customer_ids do not exist in the customer table")
    
    # check if all product_id's exist in product table
    if (~(sales_df["product_id"].isin(products_df["product_id"]))).any():
        raise ValueError("validation failed: one or more product_ids do not exist in the product table")

    # # Check whether sale_id contains null values
    if (sales_df["sale_id"].isnull()).any():
        raise ValueError("validation failed: one or more sale_ids are null. sale_id cannot be null")
    
    # check if sale_ids are unique
    if not sales_df["sale_id"].is_unique:
        raise ValueError("validation failed: duplicate sale_ids exist. sale_ids must be unique")
    
    # check if any of the customer_ids are null
    if (sales_df["customer_id"].isnull()).any():
        raise ValueError("validation failed: customer_id's cannot be null")
    
    # check if any of the product_ids are null
    if (sales_df["product_id"].isnull()).any():
        raise ValueError("validation failed: product_id's cannot be null")
    
    # check if sale quantity is greater than 0
    if (sales_df["quantity"] <= 0).any():
        raise ValueError("validation failed: quantity must be greater than 0")
    
    # check if any of the sale_date are null
    if (sales_df["order_date"].isnull()).any():
        raise ValueError("validation failed: order_date cannot contain null values")
    
    return True

