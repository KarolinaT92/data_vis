import plotly.graph_objects as go
from dash import Input, Output, callback
from plotly.subplots import make_subplots
from ..helper.cached_data import PlotRenderer
from ..helper.standard_design import TOP_LEFT_TITLE, SALES_COLOR, PROFIT_COLOR, MONTH_ABBR


@callback(Output('time-series', 'figure'),
          Input('year-dropdown', 'value'),
          Input("selected-indices-scatter-plot", "data"),
          Input("sales-switch-vis", "value"),
          Input("profit-switch-vis", "value"),
          Input('selected-category-store', 'data')
          )
def update_graph(selected_year, selected_ids, sales_chart_type, profit_chart_type, selected_category_list):
    time_series_fig = (PlotRenderer.layer2_render_selected_plot_type(
        selected_year,
        selected_ids,
        "time_series",
        build_time_series,
        sales_chart_type,
        profit_chart_type,
        selected_category_list))
    return time_series_fig


def _create_sales_trace(monthly, chart_type):
    """Helper to create Sales trace based on chart_type ('line' or 'bar')."""
    if chart_type == 'bar':
        return go.Bar(
            x=monthly["Month_Name"],
            y=monthly["Sales"],
            name="Total Sales",
            marker_color=SALES_COLOR,
            hovertemplate="Month: %{x}<br>Sales: $%{y:,.0f}<extra></extra>",
            width=0.3
        )
    elif chart_type == 'line':
        return go.Scatter(
            x=monthly["Month_Name"],
            y=monthly["Sales"],
            name="Total Sales",
            mode="lines+markers",
            line=dict(color=SALES_COLOR, width=2.5),
            hovertemplate="Month: %{x}<br>Sales: $%{y:,.0f}<extra></extra>",
        )
    else:
        # Default to bar if invalid type is passed
        return _create_sales_trace(monthly, 'bar')


def _create_profit_trace(monthly, chart_type):
    """Helper to create Profit trace based on chart_type ('line' or 'bar')."""
    if chart_type == 'bar':
        return go.Bar(
            x=monthly["Month_Name"],
            y=monthly["Profit"],
            name="Total Profit",
            marker_color=PROFIT_COLOR,
            hovertemplate="Month: %{x}<br>Profit: $%{y:,.0f}<extra></extra>",
            width=0.3
        )
    elif chart_type == 'line':
        return go.Scatter(
            x=monthly["Month_Name"],
            y=monthly["Profit"],
            name="Total Profit",
            mode="lines+markers",
            line=dict(color=PROFIT_COLOR, width=2.5),
            hovertemplate="Month: %{x}<br>Profit: $%{y:,.0f}<extra></extra>",
        )
    else:
        # Default to line if invalid type is passed
        return _create_profit_trace(monthly, 'line')


def build_time_series(df, year_for_title, sales_chart_type, profit_chart_type, selected_category_list):
    """
    Builds a dual-axis time series chart for Sales and Profit,
    allowing user choice between 'line' or 'bar' for each.
    """
    if selected_category_list and len(selected_category_list) > 0:
        df = df[df['Category'].isin(selected_category_list)]
    # --- Data Aggregation ---
    monthly = (
        df.groupby("Month", as_index=False)[["Sales", "Profit", "Month_Name"]]
        .sum()
        .sort_values("Month")
    )
    monthly["Month_Name"] = monthly["Month"].map(MONTH_ABBR)

    # --- Create dual-axis chart ---
    fig_time_series = make_subplots(specs=[[{"secondary_y": True}]])
    ## Sales Trace (Primary Y-Axis)
    # Use the helper function to create the trace based on user's choice
    sales_trace = _create_sales_trace(monthly, sales_chart_type)

    # Note: If both are bars, 'barmode' will handle the overlap/grouping.
    fig_time_series.add_trace(sales_trace, secondary_y=False)

    ## Profit Trace (Secondary Y-Axis)
    # Use the helper function to create the trace based on user's choice
    profit_trace = _create_profit_trace(monthly, profit_chart_type)
    fig_time_series.add_trace(profit_trace, secondary_y=True)

    # --- Layout ---
    fig_time_series.update_layout(
        title_text=f"Monthly Sales and Profit in {year_for_title}",
        title={**TOP_LEFT_TITLE},
        # Set barmode to 'group' to ensure bars are side-by-side if both are bars
        barmode="group",
        bargap=0.3,
        plot_bgcolor="white",
        legend=dict(
            orientation="h",
            y=1.4,
            x=0.05,
        ),
        margin=dict(l=60, r=40, t=80, b=60),
    )

    # --- Axes ---
    fig_time_series.update_xaxes(title_text="Month", showgrid=False)

    ## 🟦 Primary Y-Axis (Sales) -> Color-matched
    # Use solid color for axis font
    sales_axis_color = SALES_COLOR.replace('0.8', '1.0').replace('rgba', 'rgb')

    fig_time_series.update_yaxes(
        title_text="Sales ($)",
        tickformat="$,.0f",
        gridcolor="lightgrey",
        griddash="dash",
        secondary_y=False,
        title_font_color=sales_axis_color,
        tickfont_color=sales_axis_color
    )

    ## 🟧 Secondary Y-Axis (Profit) -> Color-matched
    fig_time_series.update_yaxes(
        title_text="Profit ($)",
        tickformat="$,.0f",
        gridcolor="lightgrey",
        secondary_y=True,
        title_font_color=PROFIT_COLOR,
        tickfont_color=PROFIT_COLOR
    )

    return fig_time_series
