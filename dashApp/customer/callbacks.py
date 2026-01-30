from dash import callback, Output, Input, State, html, ctx
from dash.exceptions import PreventUpdate
from pathlib import Path
import pandas as pd
import plotly.express as px
from us import states
from dash import dash_table

from shared.read_data import df
from dashApp.template.layouts.filter_options import SEGMENTS, REGIONS

from .figures import (
    empty_figure,
    build_top_customers_figure,
    build_customer_map_figure,
    build_sales_microbands_figure,
    build_profit_per_order_figure,
)


# =====================================================
# KPIs
# =====================================================

@callback(
    Output("kpi-total-customers", "children"),
    Input("customer-year", "value"),
    Input("customer-segment", "value"),
    Input("customer-region", "value"),
)
def update_kpi_total_customers(year, segments, regions):

    dff = _filter_customers(year, segments, regions)

    if dff.empty:
        return "—"

    return f"{dff['Customer Name'].nunique():,}"

@callback(
    Output("kpi-top-region", "children"),
    Input("customer-year", "value"),
    Input("customer-segment", "value"),
    Input("customer-region", "value"),
)
def update_kpi_top_region(year, segments, regions):

    dff = _filter_customers(year, segments, regions)

    if dff.empty:
        return "—"

    region_profit = (
        dff.groupby("Region", as_index=False)["Profit"]
        .sum()
        .sort_values("Profit", ascending=False)
    )

    top = region_profit.iloc[0]
    profit_k = round(top["Profit"] / 1_000)

    return f"{top['Region']}: ${profit_k}k"

@callback(
    Output("kpi-top-segment", "children"),
    Input("customer-year", "value"),
    Input("customer-segment", "value"),
    Input("customer-region", "value"),
)
def update_kpi_top_segment(year, segments, regions):

    dff = _filter_customers(year, segments, regions)

    if dff.empty:
        return "—"

    segment_profit = (
        dff.groupby("Segment", as_index=False)["Profit"]
        .sum()
        .sort_values("Profit", ascending=False)
    )

    top = segment_profit.iloc[0]
    profit_k = round(top["Profit"] / 1_000)

    return f"{top['Segment']}: ${profit_k}k"



# ====================================================
# LOAD CITY COORDINATES
# ====================================================

BASE_DIR = Path(__file__).resolve().parents[2]
city_coords = pd.read_csv(
    BASE_DIR / "shared" / "city_coordinates.csv",
    usecols=["City", "State", "lat", "lon"],
)

# ====================================================
# FILTER HELPER
# ====================================================

def _filter_customers(year, segments, regions):
    dff = df

    if year is not None:
        dff = dff[dff["Year"] == year]

    if segments:
        dff = dff[dff["Segment"].isin(segments)]

    if regions:
        dff = dff[dff["Region"].isin(regions)]

    return dff

SEGMENT_DROPDOWN_ID = "customer-segment"
REGION_DROPDOWN_ID = "customer-region"

@callback(
    Output(SEGMENT_DROPDOWN_ID, "value"),
    Input(SEGMENT_DROPDOWN_ID, "value"),
    prevent_initial_call=True,
)
def segment_empty_means_all(new_value):
    if not new_value:
        return SEGMENTS
    return new_value


@callback(
    Output(REGION_DROPDOWN_ID, "value"),
    Input(REGION_DROPDOWN_ID, "value"),
    prevent_initial_call=True,
)
def region_empty_means_all(new_value):
    if not new_value:
        return REGIONS
    return new_value


# ====================================================
# TOP CUSTOMERS
# ====================================================

TOPN_MAP = {
    0: 3,
    1: 5,
    2: 10,
}

@callback(
    Output("topn-value", "children"),
    Input("topn-slider", "value"),
)
def update_topn_label(slider_value):
    return str(TOPN_MAP[slider_value])

@callback(
    Output("profit-graph", "figure"),
    Input("customer-year", "value"),
    Input("customer-segment", "value"),
    Input("customer-region", "value"),
    Input("topn-slider", "value"),
)
def update_top_customers(year, segments, regions, slider_value):

    top_n = TOPN_MAP[slider_value]

    dff = _filter_customers(year, segments, regions)
    if dff.empty:
        return empty_figure()

    top = (
        dff.groupby("Customer Name", as_index=False)["Profit"]
        .sum()
        .sort_values("Profit", ascending=False)
        .head(top_n)
    )

    return build_top_customers_figure(top)


# ====================================================
# CHART ↔ TABLE TOGGLE
# ====================================================

@callback(
    Output("customers-chart-view", "style"),
    Output("customers-table-view", "style"),
    Output("customers-table-content", "children"),
    Input("profit-graph", "clickData"),
    Input("customers-back-btn", "n_clicks"),
    State("customer-year", "value"),
    State("customer-segment", "value"),
    State("customer-region", "value"),
    prevent_initial_call=True,
)
def toggle_customer_view(clickData, back_clicks, year, segments, regions):

    trigger = ctx.triggered_id

    if trigger == "customers-back-btn":
        return {"display": "flex"}, {"display": "none"}, None

    if trigger != "profit-graph" or not clickData:
        raise PreventUpdate

    customer = clickData["points"][0]["y"]

    dff = _filter_customers(year, segments, regions)
    dff = dff[dff["Customer Name"] == customer]

    if dff.empty:
        return {"display": "none"}, {"display": "flex"}, html.Div("No orders found.")

    columns = [
        "Order ID",
        "Category",
        "Sub-Category",
        "Sales",
        "Profit",
    ]

    table = dash_table.DataTable(
        data=dff[columns].to_dict("records"),
        columns=[{"name": c, "id": c} for c in columns],
        page_size=15,
        style_cell={
            "fontSize": "12px",
            "padding": "6px",
            "whiteSpace": "nowrap",
        },
        style_header={
            "fontWeight": "600",
            "backgroundColor": "#f8fafc",
        },
    )

    return {"display": "none"}, {"display": "flex"}, table

# ====================================================
# CUSTOMER MAP
# ====================================================
from dash import callback, Input, Output, ctx

@callback(
    Output("customer-min-store", "data"),
    Output("min-btn-1", "className"),
    Output("min-btn-5", "className"),
    Output("min-btn-10", "className"),
    Output("min-btn-25", "className"),
    Output("min-btn-50", "className"),
    Input("min-btn-1", "n_clicks"),
    Input("min-btn-5", "n_clicks"),
    Input("min-btn-10", "n_clicks"),
    Input("min-btn-25", "n_clicks"),
    Input("min-btn-50", "n_clicks"),
)
def select_min_customers(b1, b5, b10, b25, b50):

    button_map = {
        "min-btn-1": 1,
        "min-btn-5": 5,
        "min-btn-10": 10,
        "min-btn-25": 25,
        "min-btn-50": 50,
    }

    triggered = ctx.triggered_id or "min-btn-25"
    selected_value = button_map[triggered]

    classes = []
    for btn_id in button_map:
        classes.append("active" if btn_id == triggered else "")

    return selected_value, *classes

@callback(
    Output("customer-map", "figure"),
    Input("customer-year", "value"),
    Input("customer-segment", "value"),
    Input("customer-region", "value"),
    Input("customer-min-store", "data"),
)
def update_customer_map(year, segments, regions, min_count):

    dff = _filter_customers(year, segments, regions)
    if dff.empty:
        return empty_figure("No data for selected filters")

    city_metrics = (
        dff.groupby(["City", "State"])
        .agg(
            **{
                "Customer Count": ("Customer Name", "nunique"),
                "Total Sales": ("Sales", "sum"),
                "Total Profit": ("Profit", "sum"),
            }
        )
        .reset_index()
    )

    city_metrics = city_metrics.merge(
        city_coords,
        on=["City", "State"],
        how="inner",
    )

    state_counts = (
        city_metrics.groupby("State", as_index=False)["Customer Count"]
        .sum()
    )

    state_counts["StateCode"] = state_counts["State"].apply(
        lambda x: states.lookup(x).abbr if states.lookup(x) else None
    )
    state_counts = state_counts.dropna(subset=["StateCode"])

    return build_customer_map_figure(
        city_metrics=city_metrics,
        state_counts=state_counts,
        min_count=min_count,
    )



# ====================================================
# SALES MICROBANDS
# ====================================================

@callback(
    Output("combined-sales-chart", "figure"),
    Input("customer-year", "value"),
    Input("customer-segment", "value"),
    Input("customer-region", "value"),
)
def update_sales_microbands(year, segments, regions):

    dff = _filter_customers(year, segments, regions)
    if dff.empty:
        return empty_figure()

    agg = (
        dff.groupby(["Region", "Segment", "Category"], as_index=False)
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
        )
    )

    return build_sales_microbands_figure(agg)


# ====================================================
# PROFIT PER ORDER
# ====================================================
@callback(
    Output("profit-per-order-graph", "figure"),
    Input("customer-year", "value"),
    Input("customer-segment", "value"),
    Input("customer-region", "value"),
    Input("profit-show-yearly", "value"),
    Input("profit-show-values", "on"),   
)
def update_profit_per_order(
    year,
    segments,
    regions,
    yearly_flag,
    show_values,
):
    yearly = "yearly" in (yearly_flag or [])

    dff = _filter_customers(
        None if yearly else year,
        segments,
        regions,
    )

    if dff.empty:
        return empty_figure()

    dff = dff.copy()
    dff["Year"] = dff["Order Date"].dt.year.astype(str)

    orders = (
        dff.groupby(["Year", "Segment", "Order ID"], as_index=False)["Profit"]
        .sum()
        .groupby(["Year", "Segment"], as_index=False)["Profit"]
        .mean()
    )

    return build_profit_per_order_figure(
        orders,
        yearly=yearly,
        show_values=show_values,
    )