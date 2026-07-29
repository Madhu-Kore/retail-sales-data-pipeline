# Retail Sales Data Pipeline

CSV files → Python → PySpark → Parquet → DuckDB → Power BI

## Run

```bash
uv sync
uv run python src/generate_data.py
uv run python src/pipeline.py
uv run python src/load_duckdb.py
```

## Tables

- dim_customer
- dim_product
- dim_date
- fact_sales
