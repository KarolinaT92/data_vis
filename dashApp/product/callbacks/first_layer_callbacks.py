import plotly.express as px
from dash import callback, Output, Input, State
from shared.read_data import CAT_COLORS
from ..helper.cached_data import PlotRenderer
from ..helper.standard_design import TOP_LEFT_TITLE, MODE_BAR


@callback(
    Output("category-selection", 'children'),
    Input('selected-category-store', 'data'),  # Get selection from store
)
def update_category_selection_text(selected):
    if selected:
        return f"Show category: {selected}"
    else:
        return "Show category: All"


@callback(
    Output('bubble-chart', 'figure'),
    Input('year-dropdown', 'value'),
    Input('selected-category-store', 'data'),  # Get selection from store
)
def update_first_layer(selected_year, selected):
    return PlotRenderer.render_bubble_chart(selected_year, "bubble_chart",
                                            build_bubble_chart, selected)


def build_bubble_chart(df, year_for_title, selected_categories=None):
    CAT_ORDER = ["Furniture", "Office Supplies", "Technology"]

    # Ensure selected_categories is treated as a list, even if None is passed
    if selected_categories is None:
        selected_categories = []

    df_grouped = (
        df.groupby("Category", as_index=False)
        .agg({
            "Sales": "sum",
            "Profit": "sum",
            "Quantity": "sum"
        })
    )

    fig = px.scatter(
        df_grouped,
        x="Sales",
        y="Profit",
        color="Category",
        size="Quantity",
        # hover_name="Category",
        text="Category",
        custom_data=["Category"],  # Explicitly set custom_data to ensure Category is available in clickData
        size_max=50,
        title=None,
        labels={"Sales": "Total Sales", "Profit": "Total Profit", "Quantity": "Total Quantity"},
        category_orders={"Category": CAT_ORDER},
        color_discrete_map=CAT_COLORS,
    )

    # --- FIX: Iterate over traces for correct multi-trace highlighting ---
    if selected_categories:
        for trace in fig.data:
            category = trace.name  # Get the category name for this trace (from the 'color' mapping)

            if category in selected_categories:
                # Highlight: full opacity, thick border
                trace.marker.opacity = 1.0
                trace.marker.line = dict(width=2, color='red')
            else:
                # Dim: low opacity, no border
                trace.marker.opacity = 0.4
                trace.marker.line = dict(width=0)
    else:
        # Default state: ensure all traces are visible and have no border
        for trace in fig.data:
            trace.marker.opacity = 0.55
            trace.marker.line = dict(width=0)

    # Update text positioning for all traces
    fig.update_traces(
        textposition="middle center",
        textfont=dict(size=12, color="black"),
    )
    # --- END FIX ---

    fig.update_layout(
        title_text=f"Sales, Profit & Quantity {year_for_title}",
        title={**TOP_LEFT_TITLE},
        showlegend=False,
        plot_bgcolor="white",
        margin=dict(l=60, r=10, t=30, b=30),
        modebar=MODE_BAR,
        # Setting uirevision ensures the graph state (like zoom) is maintained
        uirevision='bubble_chart_rev'
    )

    fig.update_xaxes(automargin=True)
    fig.update_yaxes(automargin=True)

    return fig

# 1. NEW LOGIC: Manages the LIST of selected categories
@callback(
    Output('selected-category-store', 'data'),
    Input('bubble-chart', 'clickData'),
    State('selected-category-store', 'data'),
    prevent_initial_call=True
)
def handle_bubble_click(click_data, current_selection):
    """
    Toggles the selected category. Adds to the list if new, removes if already present.
    """
    if not click_data or not click_data.get('points'):
        # No click data or invalid structure, keep current selection
        return current_selection

    # Ensure current_selection is a mutable list (copy it from the State)
    selected_categories = list(current_selection)

    # Access customdata
    clicked_category = click_data['points'][0]['customdata'][0]

    if clicked_category in selected_categories:
        # Deselect: If the category is already in the list, remove it
        selected_categories.remove(clicked_category)
    else:
        # Select: Add the new category to the list
        selected_categories.append(clicked_category)

    return selected_categories

