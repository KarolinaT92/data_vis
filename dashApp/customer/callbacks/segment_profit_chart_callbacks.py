from dash import callback, Output, Input
import plotly.express as px
from shared.read_data import df


# ====================================================
# BASIC FILTER 
# ====================================================
def _filter_basic(year, segments, regions, apply_year=True):
    dff = df.copy()

    if isinstance(segments, str):
        segments = [segments]
    if isinstance(regions, str):
        regions = [regions]

    if apply_year and year:
        dff = dff[dff["Order Date"].dt.year == int(year)]

    if segments:
        dff = dff[dff["Segment"].isin(segments)]

    if regions:
        dff = dff[dff["Region"].isin(regions)]

    return dff


# ====================================================
# CALLBACK
# ====================================================
@callback(
    Output("profit-per-order-graph", "figure"),
    Input("customer-year-dropdown", "value"),
    Input("customer-segment-dropdown", "value"),
    Input("customer-region-dropdown", "value"),
    Input("profit-show-yearly", "value"),
)
def update_profit_per_order_chart(year, segments, regions, yearly_flag):

    show_yearly = "yearly" in (yearly_flag or [])

    # Ignore year filter when cumulative view is ON
    dff = _filter_basic(
        year=year,
        segments=segments,
        regions=regions,
        apply_year=not show_yearly,
    )

    if dff.empty:
        return px.bar(title="No data available", template="none")

    # --------------------------------------------------
    # PREPARE DATA
    # --------------------------------------------------
    dff = dff.copy()
    dff["Year"] = dff["Order Date"].dt.year.astype(str)

    # PROFIT PER ORDER
    orders = (
        dff
        .groupby(["Year", "Segment", "Order ID"], as_index=False)["Profit"]
        .sum()
    )

    # ==================================================
    # CUMULATED (STACKED) VIEW 
    # ==================================================
    if show_yearly:
        avg_profit_year = (
            orders
            .groupby(["Segment", "Year"], as_index=False)["Profit"]
            .mean()
        )

        year_order = sorted(avg_profit_year["Year"].unique())


        blue_shades = [
            "#cfe2f3",  
            "#9fc5e8",
            "#6fa8dc",
            "#3d85c6",  
        ]

        fig = px.bar(
            avg_profit_year,
            x="Segment",
            y="Profit",
            color="Year",
            barmode="stack",
            category_orders={"Year": year_order},
            color_discrete_sequence=blue_shades[: len(year_order)],
            title="Cumulative Average Profit",
            template="none",
        )

        fig.update_layout(
            yaxis_title="Average Profit ($)",
            xaxis_title="Segment",
            legend_title_text="Year",
        )

        return fig

    # ==================================================
    # SNAPSHOT VIEW 
    # ==================================================
    avg_profit = (
        orders
        .groupby("Segment", as_index=False)["Profit"]
        .mean()
    )

    fig = px.bar(
        avg_profit,
        x="Segment",
        y="Profit",
        text_auto=".2f",
        title= f"Average Profit per Order in {year}",
        template="none",
        color_discrete_sequence=["#3d85c6"],  
    )

    fig.update_layout(
        yaxis_title="Average Profit ($)",
        xaxis_title="Segment",
    )

    return fig
