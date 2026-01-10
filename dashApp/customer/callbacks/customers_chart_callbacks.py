from dash import callback, Output, Input, State, html
import plotly.express as px
import pandas as pd
import numpy as np
from shared.read_data import df


# ============================================================
# Filter helper
# ============================================================
def _filter_customers(year, segments, regions):
    dff = df.copy()

    if isinstance(segments, str):
        segments = [segments]
    if isinstance(regions, str):
        regions = [regions]

    if year:
        dff = dff[dff["Year"] == year]
    if segments:
        dff = dff[dff["Segment"].isin(segments)]
    if regions:
        dff = dff[dff["Region"].isin(regions)]

    return dff


# ============================================================
# Build order table
# ============================================================
def make_order_table(df_orders):
    if df_orders.empty:
        return html.Div("No orders for this customer.")

    cols = [
        "Order ID", "Order Date", "Ship Date", "Ship Mode",
        "Customer Name", "Segment", "City", "State", "Postal Code", "Region",
        "Product ID", "Category", "Sub-Category", "Product Name",
        "Sales", "Quantity", "Discount", "Profit", "Ship_Duration"
    ]

    df_orders = df_orders[cols].copy()

    for col in ["Order Date", "Ship Date"]:
        df_orders[col] = pd.to_datetime(df_orders[col]).dt.strftime("%Y-%m-%d")

    header = html.Thead(
        html.Tr([
            html.Th(
                c,
                style={
                    "fontWeight": 600,
                    "textAlign": "center",
                    "fontSize": "11px",      
                    "lineHeight": "1.2",
                    "whiteSpace": "normal",  
                    "wordBreak": "break-word",
                }
            )
            for c in cols
        ])
    )

    body = html.Tbody(
        [
            html.Tr(
                [
                    html.Td(
                        df_orders.iloc[i][c],
                        style={
                            "border": "1px solid #e5e7eb",
                            "padding": "6px",
                            "textAlign": "right"
                            if c in ["Sales", "Profit", "Discount", "Quantity", "Ship_Duration"]
                            else "left",
                            "verticalAlign": "top",
                            "wordBreak": "break-word", 
                        },
                    )
                    for c in cols
                ]
            )
            for i in range(len(df_orders))
        ]
    )

    return html.Table(
        [header, body],
        style={
            "width": "100%",
            "borderCollapse": "collapse",
            "fontSize": "12px",
            "tableLayout": "fixed", 
        },
    )


# ============================================================
# TOP PROFITABLE CUSTOMERS CHART
# ============================================================
@callback(
    Output("profit-graph", "figure"),
    Input("customer-year-dropdown", "value"),
    Input("customer-segment-dropdown", "value"),
    Input("customer-region-dropdown", "value"),
    Input("profit-view", "value"),
    Input("topn-slider", "value"),
)
def update_top_customers(year, segments, regions, profit_view, top_n):

    dff = _filter_customers(year, segments, regions)

    if dff.empty:
        return px.scatter(title="No data available.")

    df_top = (
        dff.groupby("Customer Name", as_index=False)["Profit"]
           .sum()
           .sort_values("Profit", ascending=False)
           .head(top_n)
    )

    if profit_view == "bar":
        fig = px.bar(
            df_top.sort_values("Profit"),
            x="Profit",
            y="Customer Name",
            orientation="h",
            title="Top Most Profitable Customers"
        )
    else:
        sorted_df = df_top.sort_values("Profit")
        fig = px.scatter(
            sorted_df,
            x="Profit",
            y="Customer Name",
            title="Most Profitable Customers (Lollipop)"
        )
        fig.update_traces(mode="markers")

        for _, row in sorted_df.iterrows():
            fig.add_shape(
                type="line",
                x0=0,
                x1=row["Profit"],
                y0=row["Customer Name"],
                y1=row["Customer Name"],
                line=dict(width=2),
            )

    fig.update_layout(
        xaxis_title="Profit ($)",
        yaxis_title="Customer",
        margin=dict(l=20, r=20, t=40, b=10)
    )

    return fig


# ============================================================
# CLICK ON CHART : FILL AUTOCOMPLETE DROPDOWN
# ============================================================
@callback(
    Output("customer-search-box", "value"),
    Input("profit-graph", "clickData"),
    prevent_initial_call=True
)
def fill_search_from_chart(clickData):
    if clickData is None:
        return ""
    return clickData["points"][0]["y"]


# ============================================================
# SEARCH BOX : POPULATE TABLE
# ============================================================
@callback(
    Output("customer-order-table", "children"),
    Input("customer-search-box", "value"),
    State("customer-year-dropdown", "value"),
    State("customer-segment-dropdown", "value"),
    State("customer-region-dropdown", "value"),
)
def update_customer_detail_table(customer_name, year, segments, regions):

    if not customer_name:
        return "Select or type a customer name to view their orders."

    dff = df.copy()

    if year:
        dff = dff[dff["Year"] == year]
    if segments:
        dff = dff[dff["Segment"].isin(segments)]
    if regions:
        dff = dff[dff["Region"].isin(regions)]

    dff = dff[dff["Customer Name"].str.lower() == customer_name.lower()]

    if dff.empty:
        return f"No orders found for customer: {customer_name}"

    dff["Order Date"] = pd.to_datetime(dff["Order Date"])
    dff["Ship Date"] = pd.to_datetime(dff["Ship Date"])
    dff["Ship_Duration"] = (dff["Ship Date"] - dff["Order Date"]).dt.days

    return make_order_table(dff)
