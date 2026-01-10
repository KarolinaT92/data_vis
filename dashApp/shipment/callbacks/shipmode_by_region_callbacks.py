from dash import callback, Output, Input
import plotly.graph_objects as go

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


# =====================================================
# REGION DISTRIBUTION (STACKED BARS)
# =====================================================
@callback(
    Output("shipment-region-shipmode-stacked", "figure"),
    Input("shipment-year-radio", "value"),
)
def update_shipmode_by_region(year):

    dff = df[df["Year"] == year]

    agg = (
        dff.groupby(["Region", "Ship Mode"])
           .size()
           .reset_index(name="count")
    )

    agg["percentage"] = (
        agg.groupby("Region")["count"]
           .transform(lambda x: x / x.sum())
    )

    fig = go.Figure()

    for mode in SHIP_MODE_ORDER:
        mode_df = agg[agg["Ship Mode"] == mode]

        fig.add_bar(
            x=mode_df["Region"],
            y=mode_df["percentage"],
            name=mode,
            marker_color=SHIP_MODE_COLORS[mode],
            text=[f"{v:.0%}" for v in mode_df["percentage"]],
            textposition="inside",
        )

    fig.update_layout(
        barmode="stack",
        xaxis_title="Region",  
        yaxis_tickformat=".0%",
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


# =====================================================
# TREND OVER YEARS (LINES)
# =====================================================
@callback(
    Output("shipment-shipmode-trend", "figure"),
    Input("shipment-show-trend-checkbox", "value"),
)
def update_shipmode_trend(_):

    agg = (
        df.groupby(["Year", "Ship Mode"])
          .size()
          .reset_index(name="count")
    )

    agg["percentage"] = (
        agg.groupby("Year")["count"]
           .transform(lambda x: x / x.sum())
    )

    fig = go.Figure()

    for mode in SHIP_MODE_ORDER:
        mode_df = agg[agg["Ship Mode"] == mode]

        fig.add_trace(
            go.Scatter(
                x=mode_df["Year"],
                y=mode_df["percentage"],
                mode="lines+markers",
                name=mode,
                line=dict(color=SHIP_MODE_COLORS[mode], width=2),
            )
        )

    fig.update_layout(
        yaxis_tickformat=".0%",
        xaxis_title="Year",  
        xaxis=dict(tickmode="linear", dtick=1),
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


# =====================================================
# TOGGLE TREND VISIBILITY
# =====================================================
@callback(
    Output("shipment-trend-wrapper", "style"),
    Input("shipment-show-trend-checkbox", "value"),
)
def toggle_trend_visibility(value):
    if "show" in value:
        return {"display": "block"}
    return {"display": "none"}
