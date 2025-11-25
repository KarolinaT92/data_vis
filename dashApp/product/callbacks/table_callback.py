from dash import Input, Output, callback
from shared.read_data import get_dataframe_from_store
from ..layouts.table_layout import DISPLAY_COLS
import pandas as pd


def _prep_records(df: pd.DataFrame):
    """Use this in your callbacks to prepare data for the table."""
    # ... (Your logic for selecting DISPLAY_COLS, formatting dates, and profit margin) ...
    # Removed from output for brevity, but use your original implementation.

    df = df.copy()
    df = df[DISPLAY_COLS]
    # ... date/margin formatting logic ...

    return df.to_dict("records")


# -------------------------------------------------------------------

@callback(
    Output("cannon-table", "data"),
    # ⭐️ Input 1: The dictionary from the caching store
    Input("filtered-year-data", "data"),
    # Input 2: The user's search query
    Input("cannon-search-input", "value"),
)
def filter_cannon_table(stored_data_dict, query):
    # 1. Input Safety Check
    if not stored_data_dict or stored_data_dict.get('data') is None:
        return []

    # 2. Deserialize Data using the Helper Function
    data_json = stored_data_dict.get('data')
    dff = get_dataframe_from_store(data_json)  # ⭐️ Uses your robust helper

    if dff.empty:
        return []

    # 3. Apply Search Query Filtering
    df_local = dff.copy()  # Work on a copy of the filtered data

    if query:
        # Define the column to search (e.g., 'Product Name')
        col = "Product Name" if "Product Name" in df_local.columns else None

        if col:
            # Create a mask to filter the rows containing the query (case-insensitive)
            mask = df_local[col].str.contains(query, case=False, na=False)
            df_local = df_local[mask]

    # 4. Final Formatting and Return
    # Call your data preparation function to format dates/margins and convert to records
    return _prep_records(df_local)

# def _prep_records(df: pd.DataFrame):
#     """Use this in your callbacks to prepare data for the table."""
#     df = df.copy()
#     df = df[DISPLAY_COLS]
#
#     # Dates → strings
#     for c in ["Order Date", "Ship Date"]:
#         if pd.api.types.is_datetime64_any_dtype(df[c]):
#             df[c] = df[c].dt.strftime("%Y-%m-%d")
#
#     # Profit Margin (%) is ALREADY in 0–100 scale → render as "xx.xx%"
#     if "Profit Margin (%)" in df:
#         df["Profit Margin (%)"] = df["Profit Margin (%)"].apply(
#             lambda v: "" if pd.isna(v) else f"{float(v):.2f}%"
#         )
#     return df.to_dict("records")
#
# # 1) Load data into Store
# @callback(
#     Output("cannon-store", "data"),
#     Input("url", "pathname"),  # or some other trigger
# )
# def load_cannon_data(_):
#     records = _prep_records(df)
#     return records
#
#
# # 2) Filter DataTable by search input
# @callback(
#     Output("cannon-table", "data"),
#     Input("cannon-store", "data"),
#     Input("cannon-search-input", "value"),
# )
# def filter_cannon_table(records, query):
#     if not records:
#         return []
#
#     df_local = pd.DataFrame(records)
#
#     if query:
#         # If you want to filter on Product Name or something else:
#         col = "Product Name" if "Product Name" in df_local.columns else None
#         if col:
#             mask = df_local[col].str.contains(query, case=False, na=False)
#             df_local = df_local[mask]
#
#     return df_local.to_dict("records")
