# Spark Data Ingestion with Explicit Schemas

## 1. Feature Summary

This feature implements the ingestion layer for the Retail Sales Data Pipeline using PySpark.

The pipeline reads three raw CSV datasets:

- `customers.csv`
- `products.csv`
- `sales.csv`

Each dataset is loaded into a Spark DataFrame using an explicitly defined schema instead of relying on automatic schema inference.

The completed ingestion flow is:

```text
Raw CSV Files
      ↓
Explicit Spark Schemas
      ↓
Spark DataFrameReader
      ↓
Typed Spark DataFrames
```

---

## 2. Business Problem

Retail data pipelines depend on consistent and predictable data types.

Allowing Spark to infer schemas automatically can make pipeline behavior dependent on the values present in a particular input file. Unexpected source data could therefore result in incorrect or inconsistent inferred types.

For a repeatable data pipeline, the expected structure of each source dataset should be defined explicitly.

The ingestion layer therefore defines the expected schema before processing the source data.

---

## 3. Technical Design

A `SparkSession` is created as the entry point for interacting with Spark.

```python
spark = (
    SparkSession.builder
    .appName("Retail Sales Pipeline")
    .master("local[*]")
    .getOrCreate()
)
```

The application currently runs locally and allows Spark to utilize the CPU cores available on the development machine.

Spark's `DataFrameReader` is then used to load each CSV:

```text
SparkSession
      ↓
spark.read
      ↓
DataFrameReader
      ↓
schema(...)
      ↓
csv(...)
      ↓
Spark DataFrame
```

Explicit schemas are created using:

- `StructType`
- `StructField`
- `IntegerType`
- `StringType`
- `DateType`
- `DecimalType`

---

## 4. Customer Schema

The customer dataset contains:

| Column          | Spark Type      |
| --------------- | --------------- |
| `customer_id`   | `IntegerType()` |
| `customer_name` | `StringType()`  |
| `segment`       | `StringType()`  |
| `city`          | `StringType()`  |
| `state`         | `StringType()`  |
| `region`        | `StringType()`  |

The schema is applied while reading the CSV:

```python
customers = (
    spark.read
    .schema(customer_schema)
    .csv("data/raw/customers.csv", header=True)
)
```

This produces a typed Spark DataFrame instead of asking Spark to infer the column types.

---

## 5. Product Schema

The product dataset contains:

| Column         | Spark Type           |
| -------------- | -------------------- |
| `product_id`   | `IntegerType()`      |
| `product_name` | `StringType()`       |
| `category`     | `StringType()`       |
| `unit_cost`    | `DecimalType(10, 2)` |
| `unit_price`   | `DecimalType(10, 2)` |

`DecimalType` was selected for monetary values instead of integer or floating-point types.

The precision and scale:

```python
DecimalType(10, 2)
```

allow up to ten total digits with two digits after the decimal point.

This gives the pipeline predictable fixed-decimal representation for monetary values.

---

## 6. Sales Schema

The sales dataset contains:

| Column         | Spark Type           |
| -------------- | -------------------- |
| `order_id`     | `IntegerType()`      |
| `order_date`   | `DateType()`         |
| `customer_id`  | `IntegerType()`      |
| `product_id`   | `IntegerType()`      |
| `quantity`     | `IntegerType()`      |
| `discount`     | `DecimalType(4, 2)`  |
| `sales_amount` | `DecimalType(10, 2)` |

`order_date` is parsed directly as a Spark date.

`discount` uses:

```python
DecimalType(4, 2)
```

because the generated source data contains values such as:

```text
0.00
0.05
0.10
0.15
```

`sales_amount` uses:

```python
DecimalType(10, 2)
```

to support larger monetary transaction values.

---

## 7. Why Explicit Schemas Were Used

During development, schema inference was tested using:

```python
inferSchema=True
```

Spark correctly inferred `customer_id` as an integer while treating the remaining customer fields as strings.

However, explicit schemas were selected for the pipeline because they provide:

- Predictable column types
- A documented source-data contract
- Less dependence on the contents of a particular input file
- Better control over dates and decimal values
- A stronger foundation for validation

Schema inference remains useful during exploratory work when the structure of a dataset is not yet known.

---

## 8. Schema vs Data Validation

An important distinction discovered during implementation is that defining a schema does not replace data-quality validation.

Although fields were defined with settings such as:

```python
StructField("customer_id", IntegerType(), nullable=False)
```

the DataFrames created from CSV files still displayed:

```text
nullable = true
```

The ingestion schema defines the expected structure and datatype of the data, but the pipeline will separately validate business rules such as:

- Required identifiers must not be null
- IDs must be unique where applicable
- Quantities must be greater than zero
- Product costs and prices must follow business rules
- Customer and product references in sales must exist

The next pipeline feature will implement these checks using PySpark.

---

## 9. Verification

The ingestion layer was tested locally.

The following schemas were successfully produced:

```text
customer_id: integer
customer_name: string
segment: string
city: string
state: string
region: string
```

```text
product_id: integer
product_name: string
category: string
unit_cost: decimal(10,2)
unit_price: decimal(10,2)
```

```text
order_id: integer
order_date: date
customer_id: integer
product_id: integer
quantity: integer
discount: decimal(4,2)
sales_amount: decimal(10,2)
```

`show(5)` was also executed against all three DataFrames to verify that actual records could be successfully read using the defined schemas.

Sample sales data confirmed that:

- Dates were parsed correctly.
- Decimal discount values were preserved.
- Monetary sales values were represented correctly.
- Customer and product IDs were read as integers.

---

## 10. Spark Concepts Learned

This feature introduced and reinforced several Spark concepts:

### SparkSession

The primary interface used by the Python application to interact with Spark.

### Builder Pattern

`SparkSession.builder` is used to configure the SparkSession before `getOrCreate()` returns the session object.

### DataFrameReader

`spark.read` returns a `DataFrameReader`, which provides APIs for reading formats such as CSV, JSON, and Parquet.

### Spark DataFrame

Reading a CSV returns a Spark DataFrame representing structured data and the operations required to produce it.

### Lazy Evaluation

Spark transformations build execution plans instead of immediately executing every operation.

### Actions

Operations such as `show()` require Spark to produce a result and therefore trigger execution.

### Explicit Schemas

`StructType` describes the complete DataFrame schema, while individual `StructField` objects describe each column.

---

## 11. Design Decisions

### Explicit schemas instead of inference

Chosen to make source expectations predictable and explicit.

### Decimal types for financial values

Chosen instead of integer types because prices and sales amounts contain fractional values.

Fixed decimal types were preferred over floating-point types for monetary fields.

### DateType for order dates

`order_date` is parsed directly into a date representation so downstream transformations do not need to begin from a raw string value.

### Local Spark execution

The current application uses:

```python
.master("local[*]")
```

This allows development and testing on a local machine while using available CPU cores.

The same Spark programming model can later be moved to a cluster environment.

---

## 12. Git Information

Implemented in commit:

```text
2e70d9d
Build Spark data ingestion with explicit schemas
```

Files changed:

```text
src/pipeline.py
src/validation.py
```

`validation.py` was also updated so that the validation terminology matches the actual sales dataset by using `order_date` instead of the earlier hypothetical `sale_date` name.

---

## 13. Interview Talking Points

### Why did you use an explicit schema instead of `inferSchema=True`?

I tested schema inference while developing the pipeline, but used explicit schemas for the final ingestion layer so that column types are predictable and aren't determined dynamically from each incoming CSV. This also provides a clear data contract for downstream validation and transformations.

### Why use `DecimalType` for prices?

Prices and sales amounts require fractional values and predictable decimal precision. Fixed decimal types are therefore more appropriate for the monetary fields than integer types.

### What is the role of `SparkSession`?

`SparkSession` is the main interface the PySpark application uses to interact with Spark. It provides access to functionality such as reading data, creating DataFrames, running SQL, and controlling the Spark application.

### What does `spark.read` return?

`spark.read` returns a `DataFrameReader`. The reader supports formats such as CSV, JSON, and Parquet and produces Spark DataFrames.

### What is the difference between a transformation and an action?

Transformations describe changes to a DataFrame and contribute to Spark's execution plan. Actions require a result and trigger execution of that plan.

---

## 14. Lessons Learned

The most important lessons from this feature were:

- A Spark DataFrame is different from a pandas DataFrame because Spark uses lazy execution.
- SparkSession and the underlying Spark application are related but different concepts.
- `spark.read` is a `DataFrameReader`, not the DataFrame itself.
- Reading a data source creates a DataFrame representation that Spark can later execute.
- Schema inference is convenient but should not automatically be treated as a production design.
- `StructType` represents an entire schema.
- `StructField` represents one field within that schema.
- Schema definitions and data-quality validation solve different problems.
- Financial values need careful datatype selection.

---

## 15. Next Feature

The next milestone is:

**Spark Data Quality Validation**

The existing validation business rules will be implemented using Spark DataFrame operations.

The planned flow is:

```text
CSV
 ↓
Explicit Schema
 ↓
Spark DataFrame
 ↓
Data Quality Validation
 ↓
Valid?
 ├── No → Fail Pipeline
 └── Yes
       ↓
Transformation Layer
```

Validation will include:

- Customer primary-key validation
- Product primary-key validation
- Sales transaction validation
- Null checks
- Duplicate checks
- Positive-value business rules
- Customer referential integrity
- Product referential integrity
