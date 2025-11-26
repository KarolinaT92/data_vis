# callbacks.py
import pandas as pd
import numpy as np
from dash import callback, Output, Input, html
import dash_mantine_components as dmc
from shared.read_data import df

DISPLAY_COLS = [
    'Product Name', 'Order Date', 'Discount', 'Quantity', 'Sales', 'Profit', 'Profit Margin (%)',
    'Original Unit Price', 'Ship Date', 'Ship Mode', 'Ship_Duration', 'Customer Name',
    'Segment', 'City', 'State', 'Postal Code', 'Region'
]


@callback(
    Output("top10-table-container", "children"),
    Input('year-dropdown', 'value')
)
def filter_cannon_table(selected_year):
    if selected_year is None:
        return dmc.Text("Select a year to display the table.")

    # --- find top10 product names by aggregated Profit ---
    df_year = df[df['Year'] == selected_year].copy()
    grouped = (
        df_year
        .groupby(["Product Name", "Category", "Sub-Category"], as_index=False)
        .agg({"Sales": "sum", "Profit": "sum"})
    )
    top10_names = grouped.sort_values("Profit", ascending=False).head(10)["Product Name"].tolist()

    # --- keep all rows for the top10 products ---
    top10_all_rows = df_year[df_year["Product Name"].isin(top10_names)].reset_index(drop=True)
    df_display = top10_all_rows[DISPLAY_COLS].copy()

    # --- convert to strings for dmc.Table body ---
    head = list(df_display.columns)
    body = df_display.astype(str).values.tolist()

    return (
        dmc.TableScrollContainer(
            dmc.Table(
                data={
                    "caption": f"Top 10 profitable products — {len(df_display)} rows",
                    "head": head,
                    "body": body,
                },
                striped="odd",
                highlightOnHover=True,
                withTableBorder=True,
                withColumnBorders=True,
                withRowBorders=True,
                horizontalSpacing="md",
                verticalSpacing="sm",
                stickyHeader=True,
            ),
            maxHeight=250,
            minWidth=600,
            type="scrollarea",
        )
    )
