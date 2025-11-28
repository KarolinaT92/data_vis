import pandas as pd
import numpy as np
from io import StringIO


def load_data():
    data_path = "..\\superstore_dataset\\cleaned_Superstore.csv"
    df = pd.read_csv(data_path, parse_dates=['Order Date', 'Ship Date'])

    df["ProfitMargin"] = np.where(df["Sales"] > 0, (df["Profit"] / df["Sales"]) * 100, np.nan)
    df[["Sales", "Profit"]] = df[["Sales", "Profit"]].round(2)
    df['Month'] = df['Order Date'].dt.month
    df['Year'] = df['Order Date'].dt.year
    df["Product_Key"] = df["Product ID"] + " | " + df["Product Name"]
    # Original Unit Price
    df["Original Unit Price"] = df["Sales"] / ((1 - df["Discount"]) * df["Quantity"])
    df["Original Unit Price"] = df["Original Unit Price"].round(2)
    df['Month_Name'] = pd.to_datetime(df['Month'], format='%m').dt.strftime('%b')

    df["Profit Margin (%)"] = (df["Profit"] / df["Sales"]) * 100
    df["Profit Margin (%)"] = df["Profit Margin (%)"].round(2)
    return df


df = load_data()

# --- Define the Color Mapping ---
CAT_COLORS = {
    "Furniture": "#007bff",
    "Office Supplies": "#ffa600",
    "Technology": "#2ca02c"
}


# --- Functions to serialize/deserialize DataFrames for storage in Dash Stores ---
def get_dataframe_from_store(json_data):
    """
    Converts a stored JSON string back into a Pandas DataFrame,
    using StringIO to suppress the FutureWarning.
    """
    if json_data is None:
        return pd.DataFrame()

    try:
        # ⭐️ Wrap the string in StringIO()
        return pd.read_json(StringIO(json_data), orient='split')
    except Exception as e:
        # Optional: Log the error if deserialization fails
        print(f"Error reading JSON from store: {e}")
        return pd.DataFrame()
