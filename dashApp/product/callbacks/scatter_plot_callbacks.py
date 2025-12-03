import plotly.express as px
from dash import callback, Output, Input
from shared.read_data import CAT_COLORS
from ..helper.cached_data import PlotRenderer
from ..helper.standard_design import TOP_LEFT_TITLE


@callback(
    Output("selected-indices-scatter-plot", "data"),
    Input("scatter-plot", "selectedData"),
    prevent_initial_call=True
)
def update_selected_points(selectedData):
    # Nothing selected → clear filter
    if not selectedData or "points" not in selectedData:
        return []

    # Extract the unique key from custom_data
    selected_ids = [p["customdata"][0] for p in selectedData["points"]]
    return selected_ids


@callback(Output('scatter-plot', 'figure'),
          Input('year-dropdown', 'value'),
          Input('selected-category-store', 'data'),
          Input('hover-details-switch', 'on'),
          )
def update_scatter_plot(selected_year, selected_category_list, show_hover):
    return PlotRenderer.render_scatter_plot(selected_year, "scatter", build_scatter_plot,
                                            selected_category_list, show_hover)


def build_scatter_plot(dff, year_for_title, selected_category_list, show_hover):
    if selected_category_list and len(selected_category_list) > 0:
        dff = dff[dff['Category'].isin(selected_category_list)]

    fig = px.scatter(
        dff,
        x="Profit",
        y="Sales",
        color="Category",
        custom_data=["Product_Key"],
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
        # title=f"Sales vs Profit by Category {year_for_title}",
    )

    # Styling markers (unchanged)
    fig.update_traces(
        marker=dict(size=9, line=dict(width=1, color="white"), opacity=0.8)
    )
    # If switch is OFF → hide hover details
    if not show_hover:
        fig.update_traces(
            hoverinfo="skip",
            hovertemplate=None
        )

    # Layout and readability (unchanged)
    fig.update_layout(
        plot_bgcolor="white",
        showlegend=False,
        margin=dict(l=60, r=40, t=0, b=60),
        dragmode="select",
        # title_text=f"Sales, Profit & Quantity {year_for_title}",
        # title={**TOP_LEFT_TITLE},
        # clickmode="event+select",
    )

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
