import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# =====================================================
# CONSTANTS
# =====================================================

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
# EMPTY FIGURE
# =====================================================

def empty_figure() -> go.Figure:
    fig = go.Figure()
    fig.update_layout(
        plot_bgcolor=BG_GREY,
        paper_bgcolor=BG_GREY,
        margin=dict(l=20, r=20, t=50, b=20),
    )
    return fig


# =====================================================
# ROW 2A — SPEED + SHARE
# =====================================================

def build_speed_share_figure(dff: pd.DataFrame) -> go.Figure:
    medians = (
        dff.groupby("Ship Mode")["Ship_Duration"]
        .median()
        .round(1)
        .to_dict()
    )

    share = (
        dff.groupby("Ship Mode")
        .size()
        .reindex(SHIP_MODE_ORDER)
        .reset_index(name="count")
    )
    share["share"] = share["count"] / share["count"].sum()

    fig = make_subplots(
        rows=2,
        cols=1,
        vertical_spacing=0.12,
        subplot_titles=("Delivery Time (days)", "Share of Orders"),
    )

    for mode in SHIP_MODE_ORDER:
        m = dff[dff["Ship Mode"] == mode]
        fig.add_box(
            x=[mode] * len(m),
            y=m["Ship_Duration"],
            name=mode,
            marker_color=SHIP_MODE_COLORS[mode],
            boxpoints=False,
            hovertemplate=(
                f"<b>{mode}</b><br>"
                f"Median: {medians.get(mode, '–')} days"
                "<extra></extra>"
            ),
            row=1,
            col=1,
        )

    for mode in SHIP_MODE_ORDER:
        v = share.loc[share["Ship Mode"] == mode, "share"].values[0]
        fig.add_bar(
            x=[v],
            y=["All Orders"],
            orientation="h",
            marker_color=SHIP_MODE_COLORS[mode],
            text=f"{v:.0%}",
            textposition="inside",
            showlegend=False,
            row=2,
            col=1,
        )

    fig.update_layout(
        barmode="stack",
        plot_bgcolor=BG_GREY,
        paper_bgcolor=BG_GREY,
        xaxis2=dict(range=[0, 1], tickformat=".0%"),
        yaxis2=dict(visible=False),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.08,
            xanchor="center",
            x=0.5,
        ),
        margin=dict(l=20, r=20, t=60, b=20),
    )

    return fig


# =====================================================
# ROW 2B — SHIP MODE DRIVER
# =====================================================

def build_shipmode_driver_figure(
    dff: pd.DataFrame,
    *,
    dimension: str,
    normalize: bool,
) -> go.Figure:

    agg = (
        dff.groupby([dimension, "Ship Mode"])
        .size()
        .reset_index(name="count")
    )

    if normalize:
        agg["value"] = agg.groupby(dimension)["count"].transform(
            lambda x: x / x.sum()
        )
        y_title = "Share of Orders"
        tickformat = ".0%"
    else:
        agg["value"] = agg["count"]
        y_title = "Number of Orders"
        tickformat = None

    fig = go.Figure()

    for mode in SHIP_MODE_ORDER:
        m = agg[agg["Ship Mode"] == mode]
        fig.add_bar(
            x=m[dimension],
            y=m["value"],
            name=mode,
            marker_color=SHIP_MODE_COLORS[mode],
        )

    fig.update_layout(
        barmode="stack",
        xaxis_title=dimension,
        yaxis_title=y_title,
        yaxis_tickformat=tickformat,
        plot_bgcolor=BG_GREY,
        paper_bgcolor=BG_GREY,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.08,
            xanchor="center",
            x=0.5,
        ),
        margin=dict(l=20, r=20, t=60, b=20),
    )

    return fig


# =====================================================
# ROW 3A — YEAR DISTRIBUTION
# =====================================================

def build_year_distribution_figure(
    dff: pd.DataFrame,
    *,
    normalize: bool,
) -> go.Figure:

    agg = (
        dff.groupby(["Year", "Ship Mode"])
        .size()
        .reset_index(name="count")
    )

    if normalize:
        agg["value"] = agg.groupby("Year")["count"].transform(
            lambda x: x / x.sum()
        )
        y_title = "Share of Orders"
        tickformat = ".0%"
    else:
        agg["value"] = agg["count"]
        y_title = "Number of Orders"
        tickformat = None

    fig = go.Figure()

    for mode in SHIP_MODE_ORDER:
        m = agg[agg["Ship Mode"] == mode]
        fig.add_scatter(
            x=m["Year"],
            y=m["value"],
            mode="lines+markers",
            name=mode,
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
            y=1.08,
            xanchor="center",
            x=0.5,
        ),
        margin=dict(l=20, r=20, t=60, b=20),
    )

    return fig


# =====================================================
# ROW 3B — TOP N SUB-CATEGORIES
# =====================================================

def build_topn_subcategories_figure(
    dff: pd.DataFrame,
    *,
    segment: str | None,
    ship_mode: str | None,
    top_n: int,
    show_values: bool,
) -> go.Figure:

    fig = go.Figure()

    if not segment or not ship_mode:
        fig.update_layout(
            title="Click a ship mode above to explore product details.",
            plot_bgcolor=BG_GREY,
            paper_bgcolor=BG_GREY,
            margin=dict(l=20, r=20, t=60, b=20),
        )
        return fig

    subcat = (
        dff[
            (dff["Segment"] == segment)
            & (dff["Ship Mode"] == ship_mode)
        ]
        .groupby("Sub-Category")
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
        .head(top_n)
    )

    fig.add_bar(
        y=subcat["Sub-Category"],
        x=subcat["count"],
        orientation="h",
        marker_color="#c7c9d9",
        text=subcat["count"] if show_values else None,
        textposition="inside",
    )

    fig.update_layout(
        title=f"Top {top_n} Sub-Categories — {segment} / {ship_mode}",
        xaxis_title="Number of Orders",
        plot_bgcolor=BG_GREY,
        paper_bgcolor=BG_GREY,
        margin=dict(l=30, r=20, t=60, b=20),
        yaxis=dict(autorange="reversed"),
    )

    return fig
