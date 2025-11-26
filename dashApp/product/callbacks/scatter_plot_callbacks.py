import plotly.express as px
from dash import callback, Output, Input
from shared.read_data import get_dataframe_from_store, CAT_COLORS
from ..helper.cached_data import figure_key, cache_figure_get, cache_figure_set


def build_scatter_plot(dff, year_for_title):
    key = figure_key(year_for_title, "scatter")
    # 1) FAST PATH: try cache
    fig = cache_figure_get(key)
    if fig is not None:
        return fig  # instant

    if dff.empty:
        return px.scatter(title="No data available for this year")

    fig = px.scatter(
        dff,
        x="Profit",
        y="Sales",
        color="Category",
        hover_data=[
            "Product Name",
            "Sub-Category",
            "Quantity",
            "Discount",
            "Month_Name"
        ],
        labels={
            "Sales": "Sales ($)",
            "Profit": "Profit ($)",
            "Category": "Category"
        },
        color_discrete_map=CAT_COLORS,
        title=f"Sales vs Profit by Category {year_for_title}",
    )

    # Styling markers (unchanged)
    fig.update_traces(
        marker=dict(size=9, line=dict(width=1, color="white"), opacity=0.8)
    )

    # Layout and readability (unchanged)
    fig.update_layout(
        plot_bgcolor="white",
        showlegend=False,
        margin=dict(l=60, r=40, t=60, b=60),
    )

    # --- Gridlines, Axis Lines, and ZEROLINES (MODIFIED) ---

    # X-Axis (Vertical Line at x=0)
    fig.update_xaxes(
        title="Sales ($)",
        showgrid=False,
        gridcolor="rgba(0,0,0,0.12)",
        griddash="dash",
        zeroline=True,
        zerolinecolor='black',  # Choose a distinct color
        zerolinewidth=1,  # Make it thicker than the border line
    )

    # Y-Axis (Horizontal Line at y=0)
    fig.update_yaxes(
        title="Profit ($)",
        showgrid=True,
        gridcolor="rgba(0,0,0,0.12)",
        griddash="dash",
        zeroline=True,
        zerolinecolor='black',  # Choose a distinct color
        zerolinewidth=1,  # Make it thicker than the border line
    )
    cache_figure_set(key, fig)
    return fig


@callback(Output('scatter-plot', 'figure'),
          Input('scatter-store', 'data'))
def update_scatter_plot(scatter_fig):
    if scatter_fig is None:
        return px.scatter(title="Waiting for bubbles...")
    return scatter_fig

    # selected_year = stored_data_dict.get('year')
    # year_for_title = str(selected_year)
    #
    # key = figure_key(year_for_title, "scatter")
    # # 1) FAST PATH: try cache
    # fig = cache_figure_get(key)
    # if fig is not None:
    #     return fig  # instant
    #
    # data_json = stored_data_dict.get('data')
    # dff = get_dataframe_from_store(data_json)
    #
    # # --- Build the figure if not cached ---
    # fig = build_scatter_plot(dff, year_for_title)
    #
    # # --- Store it in cache for next time ---
    # cache_figure_set(key, fig)
    #
    # return fig
