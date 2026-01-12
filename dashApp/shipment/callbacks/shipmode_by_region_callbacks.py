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

BG_GREY = "#f5f5f5"

# =====================================================
# REGION DISTRIBUTION
# =====================================================
@callback(
    Output("shipment-region-shipmode-stacked", "figure"),
    
    Input("shipment-year-radio", "value"),
    Input("shipment-normalize-toggle", "value"),
)
def update_shipmode_by_region(year, normalize):

    dff = df[df["Year"] == year]

    agg = (
        dff.groupby(["Region", "Ship Mode"])
           .size()
           .reset_index(name="count")
    )

    is_pct = "pct" in normalize

    if is_pct:
        agg["value"] = agg.groupby("Region")["count"].transform(lambda x: x / x.sum())
        y_title = "Share of Orders"
        tickformat = ".0%"
        labels = [f"{v:.0%}" for v in agg["value"]]
    else:
        agg["value"] = agg["count"]
        y_title = "Number of Orders"
        tickformat = None
        labels = [f"{int(v):,}" for v in agg["value"]]

    fig = go.Figure()

    for mode in SHIP_MODE_ORDER:
        m = agg[agg["Ship Mode"] == mode]

        fig.add_bar(
            x=m["Region"],
            y=m["value"],
            name=mode,
            marker_color=SHIP_MODE_COLORS[mode],
            text=[
                f"{v:.0%}" if is_pct else f"{int(v):,}"
                for v in m["value"]
            ],
            textposition="inside",
        )

    fig.update_layout(
        barmode="stack",
        xaxis_title="Region",
        yaxis_title=y_title,
        yaxis_tickformat=tickformat,

        plot_bgcolor=BG_GREY,
        paper_bgcolor=BG_GREY,

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.05,
            xanchor="center",
            x=0.5,
        ),
        margin=dict(l=40, r=40, t=50, b=40),
    )

    return fig


# =====================================================
# TREND OVER YEARS
# =====================================================
@callback(
    Output("shipment-shipmode-trend", "figure"),
    Input("shipment-normalize-toggle", "value"),
)
def update_shipmode_trend(normalize):

    agg = (
        df.groupby(["Year", "Ship Mode"])
          .size()
          .reset_index(name="count")
    )

    is_pct = "pct" in normalize

    if is_pct:
        agg["value"] = agg.groupby("Year")["count"].transform(lambda x: x / x.sum())
        y_title = "Share of Orders"
        tickformat = ".0%"
    else:
        agg["value"] = agg["count"]
        y_title = "Number of Orders"
        tickformat = None

    fig = go.Figure()

    for mode in SHIP_MODE_ORDER:
        m = agg[agg["Ship Mode"] == mode]

        fig.add_trace(
            go.Scatter(
                x=m["Year"],
                y=m["value"],
                mode="lines+markers",
                name=mode,
                line=dict(color=SHIP_MODE_COLORS[mode], width=2),
            )
        )

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title=y_title,
        yaxis_tickformat=tickformat,
        xaxis=dict(tickmode="linear", dtick=1),

        plot_bgcolor=BG_GREY,
        paper_bgcolor=BG_GREY,

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.05,
            xanchor="center",
            x=0.5,
        ),
        margin=dict(l=40, r=40, t=50, b=40),
    )

    return fig
