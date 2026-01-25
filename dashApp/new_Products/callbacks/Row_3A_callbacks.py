import plotly.graph_objects as go
from dash import Input, Output, callback

from dashApp.new_Products.colors import SALES_COLOR, PROFIT_COLOR
from dashApp.new_Products.constants import (
    SELECT_ON_SCATTER_PLOT, ROW_3A_ID, MONTH_LABELS,
    CATEGORY_DROPDOWN_ID, REGION_DROPDOWN_ID, PLOT_TYPE_DROPDOWN_ID
)
from dashApp.new_Products.helper import react_to_category_dropdown
from shared.read_data import df


@callback(
    Output(ROW_3A_ID, "figure"),
    Input("shipment-year", "value"),
    Input(SELECT_ON_SCATTER_PLOT, "data"),
    Input(CATEGORY_DROPDOWN_ID, "value"),
    Input(REGION_DROPDOWN_ID, "value"),
    Input(PLOT_TYPE_DROPDOWN_ID, "value"),
)
def update_graph(year, selected_ids, selected_category, selected_regions, plot_type):
    dff = react_to_category_dropdown(df, year, selected_category, selected_regions)

    if selected_ids:
        dff = dff[dff["Product_Key"].isin(selected_ids)]

    monthly = (
        dff.groupby("Month", as_index=False)
           .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
           .sort_values("Month")
    )
    monthly["MonthName"] = monthly["Month"].apply(lambda m: MONTH_LABELS[int(m) - 1])

    x = monthly["MonthName"]
    sales = monthly["Sales"]
    profit = monthly["Profit"]

    fig = go.Figure()

    # =========================
    # SWITCH: Bar vs Line
    # =========================
    if plot_type == "Line chart":
        # Line chart version (same axis)
        fig.add_trace(
            go.Scatter(
                x=x,
                y=sales,
                mode="lines+markers",
                name="Sales",
                line=dict(color=SALES_COLOR, width=2),
                hovertemplate="Month: %{x}<br>Sales: $%{y:,.0f}<extra></extra>",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=x,
                y=profit,
                mode="lines+markers",
                name="Profit",
                line=dict(color=PROFIT_COLOR, width=2),
                hovertemplate="Month: %{x}<br>Profit: $%{y:,.0f}<extra></extra>",
            )
        )

    else:
        # Default: Bar chart (your original design)
        profit_base = [0 if p >= 0 else p for p in profit]
        profit_y = [p if p >= 0 else -p for p in profit]  # magnitude, always positive

        fig.add_trace(
            go.Bar(
                x=x,
                y=sales,
                base=0,
                name="Sales",
                marker_color=SALES_COLOR,
                width=0.45,
                hovertemplate="Month: %{x}<br>Sales: $%{y:,.0f}<extra></extra>",
            )
        )

        fig.add_trace(
            go.Bar(
                x=x,
                y=profit_y,
                base=profit_base,
                name="Profit",
                marker_color=PROFIT_COLOR,
                width=0.25,
                hovertemplate="Month: %{x}<br>Profit: $%{customdata:,.0f}<extra></extra>",
                customdata=profit,
            )
        )

        fig.update_layout(
            barmode="overlay",
            bargap=0.25,
        )

    # Shared layout (both modes)
    fig.update_layout(
        title=None,
        xaxis_title="Month",
        yaxis_title="Amount ($)",
        plot_bgcolor="white",
        margin=dict(l=60, r=40, t=40, b=60),
        height=240,
        legend=dict(orientation="h", y=1.12, x=0.05),
    )

    # Shared y-axis styling (both modes)
    fig.update_yaxes(
        tickformat="$,.0f",
        zeroline=True,
        zerolinecolor="black",
        zerolinewidth=2,
        gridcolor="lightgrey",
        griddash="dash",
    )

    return fig
