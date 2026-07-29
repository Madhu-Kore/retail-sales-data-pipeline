from datetime import date, timedelta
from pathlib import Path
import random
import pandas as pd

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)
random.seed(42)

def main():
    cities = [
        ("Tampa", "FL", "South"), ("Orlando", "FL", "South"),
        ("Atlanta", "GA", "South"), ("Dallas", "TX", "South"),
        ("Chicago", "IL", "Central"), ("Seattle", "WA", "West"),
        ("New York", "NY", "East")
    ]
    categories = {
        "Electronics": ["Laptop", "Monitor", "Keyboard", "Mouse"],
        "Office Supplies": ["Notebook", "Pen Set", "Printer Paper"],
        "Furniture": ["Desk", "Chair", "Bookshelf", "Lamp"]
    }

    customers = []
    for customer_id in range(1, 501):
        city, state, region = random.choice(cities)
        customers.append({
            "customer_id": customer_id,
            "customer_name": f"Customer {customer_id}",
            "segment": random.choice(["Consumer", "Corporate", "Home Office"]),
            "city": city, "state": state, "region": region
        })
    customers = pd.DataFrame(customers)

    products = []
    for product_id in range(1, 81):
        category = random.choice(list(categories))
        unit_cost = round(random.uniform(5, 700), 2)
        products.append({
            "product_id": product_id,
            "product_name": f"{random.choice(categories[category])} {product_id}",
            "category": category,
            "unit_cost": unit_cost,
            "unit_price": round(unit_cost * random.uniform(1.15, 1.75), 2)
        })
    products = pd.DataFrame(products)

    sales = []
    start_date = date(2024, 1, 1)
    for order_id in range(1, 5001):
        customer_id = random.randint(1, 500)
        product_id = random.randint(1, 80)
        product = products.loc[products["product_id"] == product_id].iloc[0]
        quantity = random.randint(1, 6)
        discount = random.choice([0, 0, 0.05, 0.10, 0.15])
        sales.append({
            "order_id": order_id,
            "order_date": (start_date + timedelta(days=random.randint(0, 729))).isoformat(),
            "customer_id": customer_id,
            "product_id": product_id,
            "quantity": quantity,
            "discount": discount,
            "sales_amount": round(quantity * product["unit_price"] * (1 - discount), 2)
        })
    sales = pd.DataFrame(sales)

    customers.to_csv(RAW_DIR / "customers.csv", index=False)
    products.to_csv(RAW_DIR / "products.csv", index=False)
    sales.to_csv(RAW_DIR / "sales.csv", index=False)
    print("Generated 500 customers, 80 products, and 5,000 sales rows.")

if __name__ == "__main__":
    main()
