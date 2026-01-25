import plotly.graph_objects as go
from dash import Input, Output, callback
from dashApp.new_Products.constants import CATEGORY_DROPDOWN_ID, ROW_2B_ID, REGION_DROPDOWN_ID, PRODUCT_SLIDER, \
    METRIC_OPTIONS_TOP_PRODUCTS_ID, SELECT_ON_SCATTER_PLOT
from dashApp.new_Products.helper import react_to_category_dropdown
from shared.read_data import df
import pandas as pd


# ROW 2B — Top Products
def truncate_name(name, max_len=30):
    return name if len(name) <= max_len else name[:max_len] + "…"

@callback(
    Output(ROW_2B_ID, "figure"),
    Input("shipment-year", "value"),
    Input(CATEGORY_DROPDOWN_ID, "value"),
    Input(REGION_DROPDOWN_ID, "value"),
    Input(PRODUCT_SLIDER, "value"),
    Input(METRIC_OPTIONS_TOP_PRODUCTS_ID, "value"),
    Input(SELECT_ON_SCATTER_PLOT, "data"),
)
def update_top_products(year, selected_categories, selected_regions, top_n, metric, selected_ids):

    dff = react_to_category_dropdown(df, year, selected_categories, selected_regions)

    # optional: filter by selected points from scatter plot
    if selected_ids:
        dff = dff[dff["Product_Key"].isin(selected_ids)]


    # aggregate by Product Name ONLY → guarantees exactly ONE bar per product
    agg = (
        dff.groupby("Product Name", as_index=False)
           .agg(
               Sales=("Sales", "sum"),
               Profit=("Profit", "sum"),
           )
    )

    if agg.empty:
        return go.Figure()

    # choose metric
    if metric == "Sales":
        agg["Value"] = agg["Sales"]
        x_title = "Sales ($)"
        hover_label = "Sales"
        is_percent = False

    elif metric == "Profit":
        agg["Value"] = agg["Profit"]
        x_title = "Profit ($)"
        hover_label = "Profit"
        is_percent = False

    else:  # Profit Margin
        sales = agg["Sales"].replace(0, pd.NA)
        agg["Value"] = (agg["Profit"] / sales).fillna(0)
        x_title = "Profit Margin (%)"
        hover_label = "Profit Margin"
        is_percent = True

    # top N
    top = (
        agg.sort_values("Value", ascending=False)
           .head(int(top_n))
           .copy()
    )

    # truncate labels for y-axis
    top["Product Name Short"] = top["Product Name"].apply(truncate_name)

    # x values + hover format
    if is_percent:
        x_vals = top["Value"] * 100
        hover_fmt = "%{x:.1f}%"
    else:
        x_vals = top["Value"]
        hover_fmt = "%{x:,.0f} $"

    # single-trace bar chart → guaranteed no segmentation
    fig = go.Figure(
        data=[
            go.Bar(
                x=x_vals,
                y=top["Product Name Short"],
                orientation="h",
                customdata=top["Product Name"],
                width=0.4,
                hovertemplate=(
                    "<b>%{customdata}</b><br>"
                    f"{hover_label}: {hover_fmt}"
                    "<extra></extra>"
                ),
            )
        ]
    )

    fig.update_layout(
        title=None,
        xaxis_title=x_title,
        yaxis_title="",
        margin=dict(l=10, r=10, t=5, b=5),
        height=220,
    )

    # highest value at top
    fig.update_yaxes(categoryorder="total ascending")

    if is_percent:
        fig.update_xaxes(ticksuffix="%")

    return fig