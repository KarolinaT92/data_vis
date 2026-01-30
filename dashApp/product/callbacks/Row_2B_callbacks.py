import plotly.graph_objects as go
from dash import Input, Output, callback

from dashApp.product.colors import TOP_PRODUCT_COLOR
from dashApp.product.constants import CATEGORY_DROPDOWN_ID, ROW_2B_ID, REGION_DROPDOWN_ID, PRODUCT_SLIDER, \
    METRIC_OPTIONS_TOP_PRODUCTS_ID, SELECT_ON_SCATTER_PLOT, PRODUCT_TITLE
from dashApp.product.helper import react_to_category_dropdown
from shared.read_data import df
import pandas as pd


# ROW 2B — Top Products
def truncate_name(name, max_len=30):
    return name if len(name) <= max_len else name[:max_len] + "…"


@callback(
    Output(ROW_2B_ID, "figure"),
    Output(PRODUCT_TITLE, "children"),
    Input("shipment-year", "value"),
    Input(CATEGORY_DROPDOWN_ID, "value"),
    Input(REGION_DROPDOWN_ID, "value"),
    Input(PRODUCT_SLIDER, "value"),
    Input(METRIC_OPTIONS_TOP_PRODUCTS_ID, "value"),
    Input(SELECT_ON_SCATTER_PLOT, "data"),
)
def update_top_products(year, selected_categories, selected_regions, top_n, metric, selected_ids):
    top_n = int(top_n)

    # ---- title
    if metric == "Profit":
        title = f"Top {top_n} Most Profitable Products"
    elif metric == "Sales":
        title = f"Top {top_n} Leading Products by Sales Value"
    else:
        title = f"Top {top_n} Products"

    # ---- data
    dff = react_to_category_dropdown(df, year, selected_categories, selected_regions)

    if selected_ids:
        dff = dff[dff["Product_Key"].isin(selected_ids)]

    agg = (
        dff.groupby("Product Name", as_index=False)
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    )

    if agg.empty:
        return go.Figure(), title  # ✅ return BOTH outputs

    # ---- metric
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
    else:
        sales = agg["Sales"].replace(0, pd.NA)
        agg["Value"] = (agg["Profit"] / sales).fillna(0)
        x_title = "Profit Margin (%)"
        hover_label = "Profit Margin"
        is_percent = True

    top = agg.sort_values("Value", ascending=False).head(top_n).copy()
    top["Product Name Short"] = top["Product Name"].apply(truncate_name)

    if is_percent:
        x_vals = top["Value"] * 100
        hover_fmt = "%{x:.1f}%"
    else:
        x_vals = top["Value"]
        hover_fmt = "%{x:,.0f} $"

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
                marker_color=TOP_PRODUCT_COLOR,
            )
        ]
    )

    fig.update_layout(
        title=None,
        xaxis_title=x_title,
        yaxis_title="",
        margin=dict(l=60, r=40, t=10, b=110),
    )

    fig.update_yaxes(categoryorder="total ascending")

    if is_percent:
        fig.update_xaxes(ticksuffix="%")

    return fig, title
