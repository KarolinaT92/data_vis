import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, callback
from dashApp.new_Products.colors import SALES_COLOR
from dashApp.new_Products.constants import SELECT_ON_SCATTER_PLOT, ROW_3B_ID, ROW_3A_ID, MONTH_LABELS, \
    CATEGORY_DROPDOWN_ID, REGION_DROPDOWN_ID, METRIC_OPTIONS_TOP_HEATMAP_ID, SWITCH_HEATMAP
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
    Input(METRIC_OPTIONS_TOP_HEATMAP_ID, "value"),
    Input(SWITCH_HEATMAP, "on"),
)
def update_heatmap(year, selected_category, selected_regions, metric, show_text):
    dff = react_to_category_dropdown(df, year, selected_category, selected_regions)

    # ---- Dynamic Y-axis dimension
    if selected_category and len(selected_category) == 1:
        y_dim = "Sub-Category"
        y_title = "Sub-Category"
    else:
        y_dim = "Category"
        y_title = "Category"

    # ---- Metric logic
    if metric == "Sales":
        pivot = pd.pivot_table(
            dff,
            values="Sales",
            index=y_dim,
            columns="Month",
            aggfunc="sum",
            fill_value=0,
        )
        text_auto = ".0f" if show_text else False

    elif metric == "Profit":
        pivot = pd.pivot_table(
            dff,
            values="Profit",
            index=y_dim,
            columns="Month",
            aggfunc="sum",
            fill_value=0,
        )
        text_auto = ".0f" if show_text else False

    else:  # Profit Margin
        g = (
            dff.groupby([y_dim, "Month"], as_index=False)
            .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
        )
        g["Profit Margin"] = g["Profit"] / g["Sales"].replace(0, pd.NA)
        pivot = g.pivot(index=y_dim, columns="Month", values="Profit Margin").fillna(0)

        text_auto = ".1%" if show_text else False

    # ---- Ensure month order
    pivot = pivot.reindex(columns=sorted(pivot.columns))

    fig = px.imshow(
        pivot,
        text_auto=text_auto,
        color_continuous_scale="RdBu",
        aspect="auto",
    )

    fig.update_layout(
        title=None,
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis_title="Month",
        yaxis_title=y_title,
    )

    if all(isinstance(c, (int, float)) for c in pivot.columns):
        fig.update_xaxes(
            tickmode="array",
            tickvals=list(range(1, 13)),
            ticktext=MONTH_LABELS,
        )

    return fig
