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

BG_PAGE = "#f5f5f5"
BG_CHART = "rgba(255, 255, 255, 0.7)"
GRID_COLOR = "rgba(15, 23, 42, 0.08)"


# =====================================================
# EMPTY FIGURE
# =====================================================

def empty_figure() -> go.Figure:
    fig = go.Figure()
    fig.update_layout(
        plot_bgcolor=BG_CHART,
        paper_bgcolor=BG_CHART,
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
        vertical_spacing=0.2,
        row_heights=[0.7, 0.3],
        subplot_titles=("Delivery Time", "Shipping Preference"),
    )

    # --- Box plots ---
    for mode in SHIP_MODE_ORDER:
        m = dff[dff["Ship Mode"] == mode]
        fig.add_box(
            x=[mode] * len(m),
            y=m["Ship_Duration"],
            name=mode,
            legendgroup=mode,
            marker_color=SHIP_MODE_COLORS[mode],
            boxpoints=False,
            hoverinfo="skip",
            row=1,
            col=1,
        )

    # --- Stacked bar ---
    for mode in SHIP_MODE_ORDER:
        v = share.loc[share["Ship Mode"] == mode, "share"].values[0]
        fig.add_bar(
            x=[v],
            y=["All Orders"],
            orientation="h",
            marker_color=SHIP_MODE_COLORS[mode],
            legendgroup=mode,
            text=f"{v:.0%}",
            textposition="inside",
            showlegend=False,
            width=0.4,
            hoverinfo="skip",
            row=2,
            col=1,
        )

    fig.update_layout(
        barmode="stack",
        dragmode=False,
        plot_bgcolor=BG_CHART,
        paper_bgcolor=BG_CHART,
        xaxis=dict(title=None, showticklabels=False),
        yaxis_title="Days",
        xaxis2=dict(range=[0, 1], tickformat=".0%"),
        yaxis2=dict(visible=False),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.18,
            xanchor="center",
            x=0.5,
        ),
        margin=dict(l=20, r=20, t=90, b=20),
    )

    fig.update_yaxes(
    showgrid=True,
    gridcolor=GRID_COLOR,
    zeroline=False,
    row=1,
    col=1,
)

    fig.update_xaxes(
        showgrid=False,
        row=1,
        col=1,
    )

    return fig


# =====================================================
# ROW 2B — SHIP MODE
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

    if not normalize:
        totals = agg.groupby(dimension)["value"].sum()
        for x_val, total in totals.items():
            fig.add_annotation(
                x=x_val,
                y=total,
                text=f"{int(total)}",
                showarrow=False,
                yanchor="bottom",
                font=dict(size=11, color="#374151"),
            )

    fig.update_layout(
        barmode="stack",
        dragmode=False,
        xaxis_title=dimension,
        yaxis_title=y_title,
        yaxis_tickformat=tickformat,
        plot_bgcolor=BG_CHART,
        paper_bgcolor=BG_CHART,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.08,
            xanchor="center",
            x=0.5,
        ),
        margin=dict(l=20, r=20, t=60, b=20),
    )

    fig.update_yaxes(showgrid=True, gridcolor=GRID_COLOR, zeroline=False)

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
            line=dict(color=SHIP_MODE_COLORS[mode]),
            marker=dict(color=SHIP_MODE_COLORS[mode]),
        )

    fig.update_layout(
        dragmode=False,
        xaxis_title="Year",
        yaxis_title=y_title,
        yaxis_tickformat=tickformat,
        xaxis=dict(tickmode="linear", dtick=1),
        plot_bgcolor=BG_CHART,
        paper_bgcolor=BG_CHART,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.08,
            xanchor="center",
            x=0.5,
        ),
        margin=dict(l=20, r=20, t=60, b=20),
    )

    fig.update_yaxes(showgrid=True, gridcolor=GRID_COLOR, zeroline=False)

    return fig


# =====================================================
# ROW 3B — TOP 5 SUB-CATEGORIES
# =====================================================

def build_topn_subcategories_figure(
    dff: pd.DataFrame,
    *,
    segment: str | None,
    ship_mode: str | None,
    metric: str,          
    show_values: bool,
) -> go.Figure:

    fig = go.Figure()

    if not segment or not ship_mode:
        fig.update_layout(
            plot_bgcolor=BG_CHART,
            paper_bgcolor=BG_CHART,
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            annotations=[
                dict(
                    text="Click a segment on shipping distribution on the left to explore sub-categories",
                    x=0.5,
                    y=0.5,
                    xref="paper",
                    yref="paper",
                    showarrow=False,
                    font=dict(size=14, color="#64748b"),
                    align="center",
                )
            ],
        )
        return fig

    filtered = dff[
        (dff["Segment"] == segment)
        & (dff["Ship Mode"] == ship_mode)
    ]

    total_orders = len(filtered)

    base = (
        filtered
        .groupby("Sub-Category")
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
        .head(5)
    )

    if metric == "share":
        base["value"] = base["count"] / total_orders
        x_title = "Share of Orders"
        tickformat = ".0%"
        x_range = [0, 1]
        text = (
            base["value"].map(lambda v: f"{v:.0%}")
            if show_values else None
        )
    else:
        base["value"] = base["count"]
        x_title = "Number of Orders"
        tickformat = None
        x_range = None
        text = base["count"] if show_values else None

    fig.add_bar(
        y=base["Sub-Category"],
        x=base["value"],
        orientation="h",
        marker_color="#c7c9d9",
        text=text,
        textposition="outside",
        textfont=dict(size=11),
        hoverinfo="skip",
        hovertemplate=None,
    )

    fig.update_layout(
        title=f"Top 5 Sub-Categories for {segment} / {ship_mode}",
        dragmode=False,
        xaxis_title=x_title,
        xaxis_tickformat=tickformat,
        xaxis_range=x_range,
        plot_bgcolor=BG_CHART,
        paper_bgcolor=BG_CHART,
        margin=dict(l=30, r=40, t=60, b=30),
        yaxis=dict(autorange="reversed"),
    )

    fig.update_xaxes(showgrid=True, gridcolor=GRID_COLOR, zeroline=False)
    fig.update_yaxes(showgrid=False)

    return fig
