from dash import callback, Output, Input
from shared.read_data import df
import numpy as np


def _filter_customers(year, segments, regions):
    dff = df.copy()

    if isinstance(segments, str):
        segments = [segments]
    if isinstance(regions, str):
        regions = [regions]

    if year is not None:
        dff = dff[dff["Year"] == year]

    if segments:
        dff = dff[dff["Segment"].isin(segments)]

    if regions:
        dff = dff[dff["Region"].isin(regions)]

    return dff


@callback(
    Output("customer-year-display", "children"),
    Input("customer-year-dropdown", "value"),
)
def update_current_year(year):
    if year is None:
        return "Current year: –"
    return f"Current year: {year}"


@callback(
    Output("kpi-total-customers", "children"),
    Output("kpi-avg-sales", "children"),
    Output("kpi-avg-profit", "children"),
    Input("customer-year-dropdown", "value"),
    Input("customer-segment-dropdown", "value"),
    Input("customer-region-dropdown", "value"),
)
def update_customer_kpis(year, segments, regions):
    dff = _filter_customers(year, segments, regions)

    if dff.empty:
        return "0", "$0.00", "$0.00"

    n_customers = dff["Customer Name"].nunique()

    total_sales = dff["Sales"].sum()
    total_profit = dff["Profit"].sum()

    avg_sales_per_customer = total_sales / n_customers if n_customers > 0 else 0
    avg_profit_per_customer = total_profit / n_customers if n_customers > 0 else 0

    total_customers_str = f"{n_customers:,.0f}"
    avg_sales_str = f"${avg_sales_per_customer:,.2f}"
    avg_profit_str = f"${avg_profit_per_customer:,.2f}"

    return total_customers_str, avg_sales_str, avg_profit_str
