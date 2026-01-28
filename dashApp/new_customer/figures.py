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
        xaxis_title="Profit ($)",
        yaxis_title=None,
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=140, r=20, t=10, b=40),
        autosize=True,
    )

    fig.update_traces(
        marker_line_width=0,
        hovertemplate="$ %{x:,.0f}<extra></extra>"
    )

    fig.update_yaxes(automargin=True)


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
                    title=dict(
                        text="City profit",
                        font=dict(size=12),
                    ),
                    thickness=9,
                    len=0.45,
                    y=0.5,
                    tickfont=dict(size=10),),
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


def build_sales_microbands_figure(agg):

    if agg.empty:
        return empty_figure()

    # -------------------------------
    # Configuration
    # -------------------------------
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

    PROFIT_MICROBANDS_SCALE = [
        [0.0, "#d97706"],
        [0.5, "#fde047"],
        [1.0, "#16a34a"],
    ]

    regions = sorted(agg["Region"].unique())
    fig = go.Figure()
    legend_shown = set()

    # -------------------------------
    # Bars
    # -------------------------------
    for _, row in agg.iterrows():
        y = regions.index(row["Region"]) + OFFSETS[row["Segment"]]

        show_legend = row["Category"] not in legend_shown
        legend_shown.add(row["Category"])

        fig.add_bar(
            x=[row["Sales"]],
            y=[y],
            orientation="h",
            width=0.25,
            marker_color=CATEGORY_COLORS[row["Category"]],
            showlegend=show_legend,
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

    # -------------------------------
    # Axes
    # -------------------------------
    fig.update_yaxes(showticklabels=False, title=None)
    fig.update_xaxes(title="Sales ($)")

    # -------------------------------
    # LEFT labels
    # -------------------------------
    for region_index, region in enumerate(regions):

        fig.add_annotation(
            xref="paper",
            x=-0.40,
            yref="y",
            y=region_index,
            text=region,
            showarrow=False,
            xanchor="left",
            yanchor="middle",
            font=dict(size=12, color="#475569"),
        )

        visible_segments = (
            agg.loc[agg["Region"] == region, "Segment"]
            .drop_duplicates()
            .tolist()
        )

        for seg in visible_segments:
            fig.add_annotation(
                xref="paper",
                x=-0.20,
                yref="y",
                y=region_index + OFFSETS[seg],
                text=seg,
                showarrow=False,
                xanchor="left",
                yanchor="middle",
                font=dict(size=10, color="#6b7280"),
            )

    # -------------------------------
    # RIGHT labels: Total profit
    # -------------------------------
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
        color = pc.sample_colorscale(PROFIT_MICROBANDS_SCALE, t)[0]
        text = format_profit_k(row["Profit"])

        # --- halo (draw first) ---
        fig.add_annotation(
            xref="paper",
            x=1.02,
            yref="y",
            y=region_index + offset,
            text=text,
            showarrow=False,
            xanchor="left",
            yanchor="middle",
            font=dict(
                size=12,
                color="rgba(0,0,0,0.55)",
            ),
        )

        # --- foreground text ---
        fig.add_annotation(
            xref="paper",
            x=1.02,
            yref="y",
            y=region_index + offset,
            text=text,
            showarrow=False,
            xanchor="left",
            yanchor="middle",
            font=dict(
                size=12,
                color=color,
            ),
        )

    # Column header
    fig.add_annotation(
        xref="paper",
        x=1.02,
        yref="paper",
        y=1.06,
        text="Total profit ($)",
        showarrow=False,
        xanchor="left",
        font=dict(size=12, color="#374151"),
    )

    # -------------------------------
    # Layout
    # -------------------------------
    fig.update_layout(
        barmode="stack",
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=140, r=140, t=90, b=40),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.10,
            xanchor="center",
            x=0.5,
            font=dict(size=10),
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

    # --------------------------------
    # YEARLY
    # --------------------------------
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
            yaxis_title="Average profit per order",
            xaxis_title="Segment",
            plot_bgcolor="white",
            paper_bgcolor="white",
            hovermode=False,
            legend=dict(
                title_text="Year",
                yanchor="middle",
                y=0.5,          
            ),
        )

        fig.update_traces(
            marker_line_width=0,
            hoverinfo="skip",
            hovertemplate=None,
        )

        if show_values:
            fig.update_traces(
                texttemplate=VALUE_TEMPLATE,
                textposition="inside",
                textfont=dict(
                    size=10,
                    color="#475569",
                ),
            )
        else:
            fig.update_traces(text=None)

        return fig

    # --------------------------------
    # SINGLE YEAR
    # --------------------------------
    fig = px.bar(
        orders,
        x="Segment",
        y="Profit",
        color_discrete_sequence=[BASE_GREEN],
        template="none",
    )

    fig.update_layout(
        yaxis_title="Avg. Profit per Order ($)",
        xaxis_title="Segment",
        plot_bgcolor="white",
        paper_bgcolor="white",
        hovermode=False,
    )

    fig.update_traces(
        marker_line_width=0,
        hoverinfo="skip",
        hovertemplate=None,
    )

    if show_values:
        fig.update_traces(
            texttemplate=VALUE_TEMPLATE,
            textposition="outside",
            textfont=dict(
                size=11,
                color="#475569",
            ),
        )
    else:
        fig.update_traces(text=None)

    return fig
