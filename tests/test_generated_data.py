from pathlib import Path
import pandas as pd

def test_sales_data():
    path = Path("data/raw/sales.csv")
    if not path.exists():
        return
    sales = pd.read_csv(path)
    assert len(sales) == 5000
    assert (sales["quantity"] > 0).all()
