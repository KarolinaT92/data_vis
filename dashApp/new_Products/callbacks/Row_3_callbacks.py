import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, callback

from dashApp.new_Products.constants import SELECT_ON_SCATTER_PLOT, ROW_3B_ID, ROW_3A_ID
from shared.read_data import df


# ROW 3A — TIME SERIES
@callback(
    Output(ROW_3A_ID, "figure"),
    Input("shipment-year", "value"),
    Input(SELECT_ON_SCATTER_PLOT, "data"),
)
def update_graph(year, selected_ids):
    year = int(year)
    dff = df[df["Year"] == year].copy()

    if selected_ids:
        dff = dff[dff["Product_Key"].isin(selected_ids)]

    monthly_profit = (
        dff.groupby("Month", as_index=False)["Profit"]
        .sum()
        .sort_values("Month")
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
        title=None,
        xaxis_title="Month",
        yaxis_title="Total Profit",
        margin=dict(l=10, r=10, t=30, b=10),
        height=400,
    )

    return fig


# =====================================================
# ROW 3B — HEATMAP

@callback(
    Output(ROW_3B_ID, "figure"),
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
