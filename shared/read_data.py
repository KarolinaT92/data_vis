import pandas as pd
import numpy as np
from io import StringIO
from pathlib import Path


def load_data():

    base_dir = Path(__file__).resolve().parent.parent
    data_path = base_dir / "superstore_dataset" / "cleaned_Superstore.csv"

    df = pd.read_csv(
        data_path,
        parse_dates=["Order Date", "Ship Date"]
    )

    df["Ship_Duration"] = (df["Ship Date"] - df["Order Date"]).dt.days

    df = df[df["Ship_Duration"].notna()]

    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.month
    df["Month_Name"] = df["Order Date"].dt.strftime("%b")

    df["Profit Margin (%)"] = np.where(
        df["Sales"] > 0,
        (df["Profit"] / df["Sales"]) * 100,
        np.nan,
    ).round(2)

    df[["Sales", "Profit"]] = df[["Sales", "Profit"]].round(2)

    df["Product_Key"] = (
        df["Product ID"]
        + " | "
        + df["Product Name"]
        + " | "
        + df["Order Date"].astype(str)
    )

    df["Original Unit Price"] = (
        df["Sales"] / ((1 - df["Discount"]) * df["Quantity"])
    ).round(2)

    return df

df = load_data()


def get_dataframe_from_store(json_data):
    """
    Converts a stored JSON string back into a Pandas DataFrame.
    Uses StringIO to avoid FutureWarnings.
    """
    if json_data is None:
        return pd.DataFrame()

    try:
        return pd.read_json(StringIO(json_data), orient="split")
    except Exception as e:
        print(f"Error reading JSON from store: {e}")
        return pd.DataFrame()
