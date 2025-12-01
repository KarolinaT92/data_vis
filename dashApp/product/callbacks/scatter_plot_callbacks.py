import plotly.express as px
import plotly.graph_objects as go
from dash import callback, Output, Input, State
from shared.read_data import CAT_COLORS, df
from ..helper.cached_data import PlotRenderer


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
          Input('year-dropdown', 'value')
          )
def update_scatter_plot(selected_year):
    return PlotRenderer.render_plot(selected_year, "scatter", build_scatter_plot)


def build_scatter_plot(dff, year_for_title):
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
        dragmode="select",
        # clickmode="event+select",
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

# # --- Helper to build the figure given a list of selected indices ---
# def make_figure(selected_year, selected_indices=None):
#     dff = df[df['Year'] == selected_year]
#     if selected_indices is None:
#         selected_indices = []
#     selected_color = "red"
#     # Define a single size for ALL markers
#     marker_size = 10
#     marker_opacity = 0.7
#
#     x = dff["Profit"]
#     y = dff["Sales"]
#     product_names = dff["Product Name"].tolist()
#
#     colors = []
#     sizes = []
#     for i in range(len(x)):
#         if i in selected_indices:
#             colors.append(selected_color)
#
#         else:
#             # If not selected, determine the color based on the point's 'Category'
#             category = dff.iloc[i]["Category"]
#             # Look up the color from the CAT_COLORS dictionary
#             base_color = CAT_COLORS.get(category, "#808080")  # Use a default grey if category is missing
#             colors.append(base_color)
#
#     fig = go.Figure(
#         data=[
#             go.Scatter(
#                 x=x,
#                 y=y,
#                 mode="markers",
#                 marker=dict(color=colors, size=marker_size, opacity=marker_opacity),
#                 hovertext=product_names,
#                 hoverinfo='text'
#             )
#         ]
#     )
#
#     fig.update_layout(
#         hovermode="closest",
#         margin=dict(l=40, r=40, t=40, b=40),
#     )
#     return fig
#
#
# # --- Callback: update selected points on click ---
# @callback(
#     Output('scatter-plot', "figure"),
#     Output("selected-indices-scatter-plot", "data"),
#     Input('year-dropdown', 'value'),
#     Input("scatter-plot", "clickData"),
#     State("selected-indices-scatter-plot", "data"),
# )
# def update_scatter_on_click(selected_year, clickData, selected_indices):
#     if selected_indices is None:
#         selected_indices = []
#
#     # No click yet → keep the current selection and figure
#     if clickData is None:
#         return make_figure(selected_year, selected_indices), selected_indices
#
#     # pointIndex from clickData
#     point_idx = clickData["points"][0]["pointIndex"]
#
#     # Toggle behavior: click to select/deselect
#     if point_idx in selected_indices:
#         selected_indices = [i for i in selected_indices if i != point_idx]
#     else:
#         selected_indices.append(point_idx)
#
#     fig = make_figure(selected_year, selected_indices)
#     return fig, selected_indices
