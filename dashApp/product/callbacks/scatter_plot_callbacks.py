import plotly.express as px
from dash import callback, Output, Input
from shared.read_data import get_dataframe_from_store, CAT_COLORS
from ..helper.cached_data import figure_key, cache_figure_get, cache_figure_set, render_plot


@callback(Output('scatter-plot', 'figure'),
          Input('year-dropdown', 'value')
          )
def update_scatter_plot(selected_year):
    return render_plot(selected_year, "scatter", build_scatter_plot)


def build_scatter_plot(dff, year_for_title):
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

    return fig
