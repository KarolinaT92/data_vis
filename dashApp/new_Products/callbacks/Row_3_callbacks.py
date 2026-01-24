import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, callback
from dashApp.new_Products.colors import SALES_COLOR
from dashApp.new_Products.constants import SELECT_ON_SCATTER_PLOT, ROW_3B_ID, ROW_3A_ID, MONTH_LABELS, \
    CATEGORY_DROPDOWN_ID, REGION_DROPDOWN_ID
from dashApp.new_Products.helper import react_to_category_dropdown
from shared.read_data import df


# ROW 3A — TIME SERIES
@callback(
    Output(ROW_3A_ID, "figure"),
    Input("shipment-year", "value"),
    Input(SELECT_ON_SCATTER_PLOT, "data"),
    Input(CATEGORY_DROPDOWN_ID, "value"),
    Input(REGION_DROPDOWN_ID, "value"),
)
def update_graph(year, selected_ids, selected_category, selected_regions):
    dff = react_to_category_dropdown(df, year, selected_category, selected_regions)

    if selected_ids:
        dff = dff[dff["Product_Key"].isin(selected_ids)]

    monthly_profit = (
        dff.groupby("Month", as_index=False)["Sales"]
        .sum()
        .sort_values("Month")
    )
    monthly_profit["MonthName"] = monthly_profit["Month"].apply(
        lambda m: MONTH_LABELS[m - 1]
    )

    fig = go.Figure(
        data=[
            go.Bar(
                x=monthly_profit["MonthName"],
                y=monthly_profit["Sales"],
                marker_color=SALES_COLOR,
                width=0.5
            )
        ]
    )

    fig.update_layout(
        title=None,
        xaxis_title="Month",
        yaxis_title="Total Sales ($)",
        margin=dict(l=10, r=10, t=30, b=10),
        height=400,
    )

    return fig


# =====================================================
# ROW 3B — HEATMAP

@callback(
    Output(ROW_3B_ID, "figure"),
    Input("shipment-year", "value"),
    Input(CATEGORY_DROPDOWN_ID, "value"),
    Input(REGION_DROPDOWN_ID, "value"),
)
def update(year, selected_category, selected_regions):
    dff = react_to_category_dropdown(df, year, selected_category, selected_regions)

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
