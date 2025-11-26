import calendar
import plotly.graph_objects as go
from dash import Input, Output, callback
from plotly.subplots import make_subplots
import plotly.express as px
from ..helper.cached_data import figure_key, cache_figure_get, cache_figure_set

from shared.read_data import get_dataframe_from_store

MONTH_ORDER = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Define colors for clarity
SALES_COLOR = "rgba(110, 150, 180, 0.8)"  # Muted Blue/Teal
PROFIT_COLOR = "#FF9966"  # Soft Coral/Orange
MONTH_ABBR = {i: calendar.month_abbr[i] for i in range(1, 13)}


@callback(Output('heatmap', 'figure'),
          Output('time-series', 'figure'),
          Input("filtered-year-data", "data")
          )
def update_graph(stored_data_dict):
    if not stored_data_dict or 'data' not in stored_data_dict:
        # Return two placeholder figures for both outputs
        return (
            px.imshow([[0]], title="Waiting for heatmap..."),
            px.line(title="Waiting for time series...")
        )

    selected_year = stored_data_dict.get('year')
    year_for_title = str(selected_year)

    heatmap_key = figure_key(year_for_title, "heatmap")
    heatmap_fig = cache_figure_get(heatmap_key)

    time_series_key = figure_key(year_for_title, "time_series")
    time_series_fig = cache_figure_get(time_series_key)

    if heatmap_fig is not None and time_series_fig is not None:
        return heatmap_fig, time_series_fig  # FAST PATH

    data_json = stored_data_dict.get('data')
    dff = get_dataframe_from_store(data_json)

    # --- Load dataframe ---
    data_json = stored_data_dict.get('data')
    dff = get_dataframe_from_store(data_json)

    # --- Build figures if not cached ---
    if heatmap_fig is None:
        heatmap_fig = build_heatmap(dff, year_for_title)
        cache_figure_set(heatmap_key, heatmap_fig)

    if time_series_fig is None:
        time_series_fig = build_time_series(dff, year_for_title)
        cache_figure_set(time_series_key, time_series_fig)

    return heatmap_fig, time_series_fig


def build_heatmap(df, year_for_title):
    heat_data = (
        df.groupby(["Category", "Month_Name"], as_index=False)["Profit"]
        .sum()
    )

    # Pivot to heatmap matrix
    heat_matrix = heat_data.pivot(index="Category", columns="Month_Name", values="Profit")

    # ✅ Plot Heatmap
    fig_heatmap = px.imshow(
        heat_matrix,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="Blues",
        labels=dict(color="Total Profit ($)"),
        title=f"Monthly Profit made by Categories {year_for_title}",
    )

    fig_heatmap.update_layout(
        xaxis_title="Month",
        yaxis_title="Category",
        margin=dict(l=60, r=40, t=60, b=60),
        coloraxis_colorbar=dict(title="Profit ($)")
    )
    return fig_heatmap


def build_time_series(df, year_for_title):
    key = figure_key(year_for_title, "time_series")
    # 1) FAST PATH: try cache
    fig = cache_figure_get(key)
    if fig is not None:
        return fig  # instant

    monthly = (
        df.groupby("Month", as_index=False)[["Sales", "Profit", "Month_Name"]]
        .sum()
        .sort_values("Month")
    )
    monthly["Month_Name"] = monthly["Month"].map(MONTH_ABBR)

    # --- Create dual-axis chart ---
    fig_time_series = make_subplots(specs=[[{"secondary_y": True}]])

    # 🎨 Mild Color 1 (Sales Bars)
    fig_time_series.add_trace(
        go.Bar(
            x=monthly["Month_Name"],
            y=monthly["Sales"],
            name="Total Sales",
            marker_color=SALES_COLOR,
            hovertemplate="Month: %{x}<br>Sales: $%{y:,.0f}<extra></extra>",
            width=0.3
        ),
        secondary_y=False
    )

    # 🎨 Mild Color 2 (Profit Line)
    fig_time_series.add_trace(
        go.Scatter(
            x=monthly["Month_Name"],
            y=monthly["Profit"],
            name="Total Profit",
            mode="lines+markers",
            line=dict(color=PROFIT_COLOR, width=2.5),
            hovertemplate="Month: %{x}<br>Profit: $%{y:,.0f}<extra></extra>",
        ),
        secondary_y=True
    )

    # --- Layout ---
    fig_time_series.update_layout(
        title=f"Monthly Sales and Profit in {year_for_title}",
        barmode="group",
        bargap=0.3,
        plot_bgcolor="white",
        legend=dict(
            orientation="h",
            y=1.1,
            x=0.05,
            bgcolor="rgba(255, 255, 255, 0.5)",
            bordercolor="lightgrey",
            borderwidth=1
        ),
        margin=dict(l=60, r=60, t=80, b=50),
    )

    # --- Axes ---
    fig_time_series.update_xaxes(title_text="Month", showgrid=False)

    # 🟦 Primary Y-Axis (Sales) -> Color-matched to Bars
    fig_time_series.update_yaxes(
        title_text="Sales ($)",
        tickformat="$,.0f",
        gridcolor="lightgrey",
        griddash="dash",
        secondary_y=False,
        # Apply bar color to axis title and ticks
        title_font_color=SALES_COLOR.replace('0.8', '1.0').replace('rgba', 'rgb'),  # Use solid color for font
        tickfont_color=SALES_COLOR.replace('0.8', '1.0').replace('rgba', 'rgb')
    )

    # 🟧 Secondary Y-Axis (Profit) -> Color-matched to Line
    fig_time_series.update_yaxes(
        title_text="Profit ($)",
        tickformat="$,.0f",
        gridcolor="lightgrey",
        secondary_y=True,
        # Apply line color to axis title and ticks
        title_font_color=PROFIT_COLOR,
        tickfont_color=PROFIT_COLOR
    )
    return fig_time_series
