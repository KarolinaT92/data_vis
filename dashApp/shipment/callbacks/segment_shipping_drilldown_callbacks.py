from dash import callback, Output, Input
import plotly.graph_objects as go
import pandas as pd

from shared.read_data import df


SHIP_MODE_ORDER = [
    "Same Day",
    "First Class",
    "Second Class",
    "Standard Class",
]

SHIP_MODE_COLORS = {
    "Same Day": "#e8b7c8",
    "First Class": "#a9c3df",
    "Second Class": "#c3b6db",
    "Standard Class": "#9fd3c7",
}

DRILLDOWN_BAR_COLOR = "#c7c9d9"


# ====================================================
# MAIN CHART — SEGMENT × SHIP MODE (HORIZONTAL)
# ====================================================
@callback(
    Output("shipment-segment-shipmode", "figure"),
    Input("shipment-year-radio", "value"),
)
def update_segment_shipmode(year):

    dff = df[df["Year"] == year]

    agg = (
        dff.groupby(["Segment", "Ship Mode"])
           .size()
           .reset_index(name="count")
    )

    agg["percentage"] = (
        agg.groupby("Segment")["count"]
           .transform(lambda x: x / x.sum())
    )

    fig = go.Figure()

    for mode in SHIP_MODE_ORDER:
        mode_df = agg[agg["Ship Mode"] == mode]

        fig.add_bar(
            y=mode_df["Segment"],
            x=mode_df["percentage"],
            orientation="h",
            name=mode,
            marker_color=SHIP_MODE_COLORS[mode],
            text=[f"{v:.0%}" for v in mode_df["percentage"]],
            textposition="inside",
        )

    fig.update_layout(
        barmode="stack",
        xaxis_tickformat=".0%",
        xaxis_title="Share of Orders",  
        plot_bgcolor="#f5f5f5",
        paper_bgcolor="#f5f5f5",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.05,
            xanchor="center",
            x=0.5,
        ),
    )

    return fig


# ====================================================
# DRILL-DOWN — TOP N SUB-CATEGORIES
# ====================================================
@callback(
    Output("shipment-drilldown-chart", "figure"),
    Input("shipment-segment-shipmode", "clickData"),
    Input("shipment-topn-dropdown", "value"),
    Input("shipment-drilldown-show-values", "on"),
    Input("shipment-year-radio", "value"),
)
def update_drilldown(clickData, top_n, show_values, year):

    fig = go.Figure()

    if clickData is None:
        fig.update_layout(
            title="Click a segment above to explore product details.",
            plot_bgcolor="#f5f5f5",
            paper_bgcolor="#f5f5f5",
        )
        return fig

    segment = clickData["points"][0]["y"]
    ship_mode = clickData["points"][0]["curveNumber"]
    ship_mode = SHIP_MODE_ORDER[ship_mode]

    dff = df[
        (df["Year"] == year) &
        (df["Segment"] == segment) &
        (df["Ship Mode"] == ship_mode)
    ]

    subcat = (
        dff.groupby("Sub-Category")
           .size()
           .reset_index(name="count")
           .sort_values("count", ascending=False)
           .head(top_n)
    )

    fig.add_bar(
        y=subcat["Sub-Category"],
        x=subcat["count"],
        orientation="h",
        marker_color=DRILLDOWN_BAR_COLOR,
        text=subcat["count"] if show_values else None,
        textposition="inside",
        insidetextanchor="middle",
    )

    fig.update_layout(
        plot_bgcolor="#f5f5f5",
        paper_bgcolor="#f5f5f5",
        xaxis_title="Number of Orders",  
        title=f"Top {top_n} Sub-Categories — {segment} / {ship_mode}",
    )

    return fig
