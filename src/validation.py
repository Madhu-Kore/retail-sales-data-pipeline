
def validate_customers(df):

    # check for null customer ID's
    if df["customer_id"].isnull().any():
        raise ValueError("validation failed: customer_id contains null values.")
    
    # check for duplicate customer ID's
    if not df["customer_id"].is_unique:
        raise ValueError("validation failed: duplicate customer_id's found.")
    
    return True
