from dash import Input, Output, callback
from .constants import row_2A_id, row_2B_id, row_3A_id, row_3B_id
from shared.read_data import df
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# ROW 1 — KPI UPDATES

@callback(
    Output('kpi-total-sales', 'children'),
    Output('kpi-profit', 'children'),
    Output('kpi-orders', 'children'),
    Input("shipment-year", "value"),
    # Input("shipment-segment", "value"),
    # Input("shipment-region", "value"),
)
def update_kpis(year):
    df_selected_year = df[
        (df["Year"] == year)
        # & (df["Segment"].isin(segments))
        # & (df["Region"].isin(regions))
    ]
    sales_of_year = df_selected_year["Sales"].sum()
    sales = f"${sales_of_year:,.0f}"
    profit_of_year = df_selected_year["Profit"].sum()

    profit = f"${profit_of_year:,.0f}"
    orders_of_year = df_selected_year["Quantity"].sum()
    orders = f"{orders_of_year:,}"
    return sales, profit, orders


# =====================================================
# ROW 2A — Bubble Chart
@callback(
    Output(row_2A_id, 'figure'),
    Input("shipment-year", "value"),
)
def update_bubble_chart(year):
    dff = df[(df["Year"] == year)]
    category_summary = (
        dff.groupby("Category", as_index=False)
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Quantity=("Quantity", "sum"),
        )
    )

    fig = px.scatter(
        category_summary,
        x="Sales",
        y="Profit",
        size="Quantity",
        color="Category",
        hover_name="Category",
        size_max=60,
        # title=f"Sales vs Profit by Category ({year})",
        labels={"Sales": "Total Sales", "Profit": "Total Profit", "Quantity": "Total Quantity"},
    )

    fig.update_layout(
        margin=dict(l=10, r=10, t=50, b=10),
        xaxis_title="Total Sales",
        yaxis_title="Total Profit",
    )

    return fig


# =====================================================
# ROW 2B — Top Products
TOP_N = 10

@callback(
    Output(row_2B_id, "figure"),
    Input("shipment-year", "value"),
)
def update_top_products(year):
    year = int(year)
    dff = df[df["Year"] == year].copy()

    top = (
        dff.groupby(["Product Name"], as_index=False)
           .agg(Profit=("Profit", "sum"))
           .sort_values("Profit", ascending=False)
           .head(TOP_N)
    )

    if top.empty:
        return go.Figure()

    fig = go.Figure(
        data=[
            go.Bar(
                x=top["Profit"],
                y=top["Product Name"],
                orientation="h",
            )
        ]
    )

    fig.update_layout(
        xaxis_title="Total Profit",
        yaxis_title="",
        margin=dict(l=10, r=10, t=50, b=10),
        height=400,
    )

    return fig


# =====================================================
# ROW 3A — TIME SERIES
@callback(
    Output(row_3A_id, "figure"),
    Input("shipment-year", "value"),
)
def update_graph(year):
    year = int(year)
    dff = df[df["Year"] == year].copy()

    monthly_profit = (
        dff.groupby("Month", as_index=False)["Profit"]
           .sum()
    )

    fig = go.Figure(
        data=[
            go.Bar(
                x=monthly_profit["Month"],
                y=monthly_profit["Profit"],
            )
        ]
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Total Profit",
        margin=dict(l=10, r=10, t=50, b=10),
        height=400,
    )

    return fig


# =====================================================
# ROW 3B — HEATMAP

@callback(
    Output(row_3B_id, "figure"),
    Input("shipment-year", "value"),
)
def update(year):
    year = int(year)
    dff = df[df["Year"] == year].copy()

    pivot = pd.pivot_table(
        dff,
        values="Profit",
        index="Category",
        columns="Month",
        aggfunc="sum",
        fill_value=0
    )

    fig = px.imshow(
        pivot,
        text_auto=".1f",
        color_continuous_scale="RdBu",
        aspect="auto",
    )

    fig.update_layout(
        margin=dict(l=10, r=10, t=50, b=10),
        xaxis_title="Month",
        yaxis_title="Category",
    )

    return fig