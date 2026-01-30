import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.colors as pc

# ====================================================
# CONSTANTS
# ====================================================

POSITIVE = "#3b82f6"
NEGATIVE = "#ef4444"

PROFIT_SCALE = [
    [0.0, "#d97706"],
    [0.5, "#fde047"],
    [1.0, "#16a34a"],
]

# ====================================================
# EMPTY FIGURE
# ====================================================

def empty_figure(msg="No data available"):
    fig = go.Figure()
    fig.add_annotation(
        text=msg,
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        showarrow=False,
        font=dict(size=14, color="#64748b"),
    )
    fig.update_layout(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        plot_bgcolor="white",
        paper_bgcolor="white",
    )
    return fig


# ====================================================
# TOP CUSTOMERS
# ====================================================

def build_top_customers_figure(df_top):

    if df_top.empty:
        return empty_figure()

    RANK_GREEN = "#7bbbc4"

    df_top = df_top.sort_values("Profit", ascending=True)

    fig = px.bar(
        df_top,
        x="Profit",
        y="Customer Name",
        orientation="h",
        color_discrete_sequence=[RANK_GREEN],
        template="none",
    )


    fig.update_layout(
        autosize=True,
        dragmode=False,
        xaxis_title="Profit ($)",
        yaxis_title=None,
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=140, r=20, t=8, b=48),
    )

    fig.update_traces(
        marker_line_width=0,
        hovertemplate="$ %{x:,.0f}<extra></extra>",
        width=0.6,
    )

    fig.update_yaxes(
        automargin=True,
        categoryorder="total ascending",
    )

    return fig



# ====================================================
# CUSTOMER MAP
# ====================================================

def build_customer_map_figure(
    *,
    city_metrics,
    state_counts,
    min_count,
):
    fig = px.choropleth(
        state_counts,
        locations="StateCode",
        locationmode="USA-states",
        color="Customer Count",
        scope="usa",
        color_continuous_scale="Blues",
    )

    fig.update_layout(
        coloraxis_colorbar=dict(title="State Customers", x=-0.06, xpad=10),
        margin=dict(l=10, r=10, t=40, b=10),
        dragmode="pan",
        coloraxis_showscale=False,
    )

    min_count = max(1, int(min_count or 1))
    city_for_dots = city_metrics[
        city_metrics["Customer Count"] >= min_count
    ].copy()

    if not city_for_dots.empty:
        profit_abs = max(
            abs(city_for_dots["Total Profit"].min()),
            abs(city_for_dots["Total Profit"].max()),
            1,
        )

        city_for_dots["hover_text"] = (
            city_for_dots["City"]
            + ", "
            + city_for_dots["State"]
            + "<br>Customers: "
            + city_for_dots["Customer Count"].astype(int).astype(str)
            + "<br>Sales: $"
            + city_for_dots["Total Sales"].round(0).astype(int).astype(str)
            + "<br>Profit: $"
            + city_for_dots["Total Profit"].round(0).astype(int).astype(str)
        )

        sizes = 4 + 1.4 * np.sqrt(city_for_dots["Customer Count"])

        fig.add_annotation(
            text="Note: state color = customer concentration, dot size = number of customers",
            x=0.5,
            y=0.0,
            xref="paper",
            yref="paper",
            showarrow=False,
            font=dict(size=9, color="#64748b"),
            align="center",
        )

        fig.add_scattergeo(
            lat=city_for_dots["lat"],
            lon=city_for_dots["lon"],
            text=city_for_dots["hover_text"],
            hoverinfo="text",
            name="City (profit)",
            marker=dict(
                size=sizes,
                color=city_for_dots["Total Profit"],
                colorscale=PROFIT_SCALE,
                cmin=-profit_abs,
                cmax=profit_abs,
                opacity=0.9,
                line=dict(width=0.4, color="#333"),
                colorbar=dict(
                    title=dict(text="City profit", font=dict(size=12)),
                    thickness=9,
                    len=0.6,
                    y=0.5,
                    tickfont=dict(size=10),
                ),
            ),
        )

    fig.update_geos(
        projection_type="albers usa",
        showland=True,
        landcolor="#F8F8F8",
        subunitcolor="#D1D5DB",
        showsubunits=True,
        showcountries=False,
    )

    return fig


# ====================================================
# SALES MICROBANDS
# ====================================================


def format_profit_k(value: float) -> str:
    """
    Format profit using 'k' notation for dense charts.

    Rules:
    - < 1k       -> $0.8k
    - 1k-9.9k   -> $3.4k
    - >= 10k    -> $12k
    """
    value_k = value / 1000

    if value_k < 10:
        return f"{value_k:.1f}k".replace(".0k", "k")
    else:
        return f"{round(value_k):,.0f}k"


def add_profit_annotation(fig, *, x, y, text, color, size=10):
    # dark halo layer 
    fig.add_annotation(
        xref="paper",
        x=x,
        yref="y",
        y=y,
        text=text,
        showarrow=False,
        xanchor="left",
        yanchor="middle",
        font=dict(
            size=size,
            color="#0f172a", 
        ),
    )


    fig.add_annotation(
        xref="paper",
        x=x,
        yref="y",
        y=y,
        text=text,
        showarrow=False,
        xanchor="left",
        yanchor="middle",
        font=dict(
            size=size,
            color=color,
        ),
    )

def build_sales_microbands_figure(agg):

    if agg.empty:
        return empty_figure()

    OFFSETS = {
        "Consumer": 0.3,
        "Corporate": 0.0,
        "Home Office": -0.3,
    }

    CATEGORY_COLORS = {
        "Furniture": "#D2E0D3",
        "Technology": "#F0DDD6",
        "Office Supplies": "#F2C3B9",
    }

    SEGMENT_COLORS = {
        "Consumer": "#2563eb",     
        "Corporate": "#7c3aed",    
        "Home Office": "#059669",   
    }

    SEGMENT_SYMBOLS = {
        "Consumer": "circle",
        "Corporate": "square",
        "Home Office": "diamond",
    }

    PROFIT_SCALE = [
        [0.0, "#d97706"],
        [0.5, "#fde047"],
        [1.0, "#16a34a"],
    ]

    regions = sorted(agg["Region"].unique())
    fig = go.Figure()
    legend_categories = set()

    for _, row in agg.iterrows():
        y = regions.index(row["Region"]) + OFFSETS[row["Segment"]]

        show_cat_legend = row["Category"] not in legend_categories
        legend_categories.add(row["Category"])

        fig.add_bar(
            x=[row["Sales"]],
            y=[y],
            orientation="h",
            width=0.25,
            marker_color=CATEGORY_COLORS[row["Category"]],
            showlegend=show_cat_legend,
            legendgroup=row["Category"],
            name=row["Category"],
            customdata=[[row["Region"], row["Segment"], row["Category"], row["Profit"]]],
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "Segment: %{customdata[1]}<br>"
                "Category: %{customdata[2]}<br>"
                "Sales: %{x:,.0f}<br>"
                "Profit: %{customdata[3]:,.0f}"
                "<extra></extra>"
            ),
        )

        fig.add_scatter(
            x=[0],
            y=[y],
            mode="markers",
            marker=dict(
                symbol=SEGMENT_SYMBOLS[row["Segment"]],
                size=8,
                color=SEGMENT_COLORS[row["Segment"]],
                line=dict(width=0),
            ),
            showlegend=False,
            hoverinfo="skip",
        )

    fig.update_yaxes(showticklabels=False, title=None,fixedrange=True)
    fig.update_xaxes(title="Sales ($)",fixedrange=True)


    for i, region in enumerate(regions):
        fig.add_annotation(
            xref="paper",
            x=-0.10,
            yref="y",
            y=i,
            text=region,
            showarrow=False,
            xanchor="left",
            yanchor="middle",
            font=dict(size=11, color="#475569"),
        )

    profit_totals = (
        agg.groupby(["Region", "Segment"], as_index=False)["Profit"]
        .sum()
    )

    pmin = profit_totals["Profit"].min()
    pmax = profit_totals["Profit"].max()
    denom = max(pmax - pmin, 1)

    for _, row in profit_totals.iterrows():
        region_index = regions.index(row["Region"])
        offset = OFFSETS[row["Segment"]]

        t = (row["Profit"] - pmin) / denom
        color = pc.sample_colorscale(PROFIT_SCALE, t)[0]
        text = format_profit_k(row["Profit"])

        add_profit_annotation(
            fig,
            x=1.02,
            y=region_index + offset,
            text=text,
            color=color,
            size=10,
        )

    fig.add_annotation(
        xref="paper",
        x=1.0,
        yref="paper",
        y=1.06,
        text="Total profit($)",
        showarrow=False,
        xanchor="left",
        font=dict(size=11, color="#374151"),
    )

    SEGMENT_KEY = (
        "<span style='color:#2563eb'>●</span> Consumer&nbsp;&nbsp;"
        "<span style='color:#7c3aed'>■</span> Corporate&nbsp;&nbsp;"
        "<span style='color:#059669'>◆</span> Home Office"
    )

    fig.add_annotation(
        xref="paper",
        yref="paper",
        x=0.5,
        y=1.06,
        text=SEGMENT_KEY,
        showarrow=False,
        xanchor="center",
        font=dict(size=10),
    )

    fig.update_layout(
        barmode="stack",
        dragmode=False,
        uirevision="sales-microbands",
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=80, r=80, t=60, b=40),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.12,
            xanchor="center",
            x=0.5,
            traceorder="normal",
            font=dict(size=8),
            itemwidth=40,       
        ),
        legend_title_text=None,
    )

    return fig


# ====================================================
# PROFIT PER ORDER
# ====================================================

BASE_GREEN = "#4f9a94"

GREEN_SCALE = [
    "#e6f2f1",
    "#cfe6e3",
    "#b5d7d2",
    "#8fc1bb",
    "#6faeaa",
]

def build_profit_per_order_figure(orders, *, yearly, show_values):

    if orders.empty:
        return empty_figure()

    VALUE_TEMPLATE = "%{y:,.0f}"

    # ====================================================
    # YEARLY COMPARISON
    # ====================================================
    if yearly:
        years = sorted(orders["Year"].unique())
        color_map = {
            year: GREEN_SCALE[min(i, len(GREEN_SCALE) - 1)]
            for i, year in enumerate(years)
        }

        fig = px.bar(
            orders,
            x="Segment",
            y="Profit",
            color="Year",
            barmode="stack",
            color_discrete_map=color_map,
            template="none",
        )

        fig.update_layout(
            yaxis_title="Avg. Profit ($)",
            xaxis_title="Segment",
            plot_bgcolor="white",
            paper_bgcolor="white",
            dragmode=False,
            hovermode=False,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5,
                font=dict(size=10),
            ),
            legend_title_text="Year",
        )

        fig.update_traces(
            marker_line_width=0,
            hoverinfo="skip",
        )

        if show_values:
            fig.update_traces(
                texttemplate=VALUE_TEMPLATE,
                textposition="inside",
                textfont=dict(size=10, color="#475569"),
            )
        else:
            fig.update_traces(text=None)

        return fig

    # ====================================================
    # NON-YEARLY 
    # ====================================================
    fig = px.bar(
        orders,
        x="Segment",
        y="Profit",
        color_discrete_sequence=[BASE_GREEN],
        template="none",
    )

    max_profit = orders["Profit"].max()

    fig.update_layout(
        yaxis_title="Avg. Profit ($)",
        xaxis_title="Segment",
        plot_bgcolor="white",
        paper_bgcolor="white",
        hovermode=False,
        dragmode=False,
    )

    fig.update_yaxes(
        range=[0, max_profit * 1.15],
    )

    fig.update_traces(
        marker_line_width=0,
        hoverinfo="skip",
        cliponaxis=False,
    )

    if show_values:
        fig.update_traces(
            texttemplate=VALUE_TEMPLATE,
            textposition="outside",
            textfont=dict(size=11, color="#475569"),
        )
    else:
        fig.update_traces(text=None)

    return fig
