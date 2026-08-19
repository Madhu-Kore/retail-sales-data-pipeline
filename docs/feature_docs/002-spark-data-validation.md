# Feature 002: Spark Data Validation

## Overview

This feature adds data quality validation to the Spark ingestion pipeline.

After the customer, product, and sales CSV files are loaded into Spark DataFrames, the pipeline validates the datasets before allowing downstream processing to continue.

If a validation rule fails, the pipeline raises a `ValueError` and stops processing.

---

## Customer Validation

The `validate_customers()` function validates the customer dataset.

### Rules

- `customer_id` must not contain null values.
- `customer_id` must be unique.

### Duplicate Detection

Duplicate customer IDs are identified by:

1. Grouping records by `customer_id`.
2. Counting the number of records for each ID.
3. Filtering IDs where the count is greater than 1.
4. Counting the resulting invalid records.

If any duplicate IDs exist, validation fails.

---

## Product Validation

The `validate_products()` function validates the product dataset.

### Rules

- `product_id` must not contain null values.
- `product_id` must be unique.
- `unit_cost` must be greater than 0.
- `unit_price` must be greater than or equal to 0.

A `unit_price` of 0 is allowed because a product could potentially be provided as a free item or sample.

---

## Sales Validation

The `validate_sales()` function validates the sales dataset.

### Rules

- `order_id` must not contain null values.
- `order_id` must be unique.
- `customer_id` must not contain null values.
- `product_id` must not contain null values.
- `quantity` must be greater than 0.
- `order_date` must not contain null values.
- Every `customer_id` in sales must exist in the customer dataset.
- Every `product_id` in sales must exist in the product dataset.

---

## Referential Integrity

Sales records contain foreign keys referencing the customer and product datasets.

The relationships are:

```text
sales.customer_id → customers.customer_id

sales.product_id → products.product_id

```

A `left_anti` join is used to identify sales records that do not have a matching customer or product.

Example:

```python
sales.join(
    customers,
    on="customer_id",
    how="left_anti"
)
```

A `left_anti` join returns rows from the left DataFrame that do not have a matching row in the right DataFrame.

If the resulting DataFrame contains any rows, at least one sales record references a customer that does not exist.

The same approach is used to validate `product_id`.

---

## Spark Transformations and Actions

The validation logic uses both Spark transformations and actions.

### Transformations

Examples used in validation:

- `filter()`
- `groupBy()`
- `join()`

These operations build Spark's execution plan.

### Actions

The primary action used during validation is:

```python
.count()
```

`count()` triggers Spark to execute the transformations needed to determine how many invalid records exist.

---

## Validation Failure Behavior

When invalid data is found, the validation function raises a `ValueError`.

Example:

```python
if sales.filter(F.col("quantity") <= 0).count() > 0:
    raise ValueError(
        "validation failed: quantity must be greater than 0"
    )
```

This stops the pipeline and prevents invalid data from continuing into downstream processing.

Each validation function returns `True` when all validation rules pass.

---

## Manual Validation Testing

The validation rules were tested using intentionally invalid Spark DataFrames.

### Customer Tests

- Null `customer_id`
- Duplicate `customer_id`

### Product Tests

- Null `product_id`
- Duplicate `product_id`
- `unit_cost <= 0`
- `unit_price < 0`

### Sales Tests

- Null `order_id`
- Duplicate `order_id`
- Null `customer_id`
- Null `product_id`
- `quantity <= 0`
- Null `order_date`
- Customer ID not found in customers
- Product ID not found in products

The manual test cases are preserved in:

```text
tests/test_validation.py
```

These test cases can later be converted into automated `pytest` tests.

---

## Result

The customer, product, and sales datasets successfully pass all implemented validation rules.

Current validation output:

```text
True
True
True
```

The datasets are ready for the next stage of the pipeline.
