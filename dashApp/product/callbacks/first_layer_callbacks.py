import plotly.express as px
from dash import callback, Output, Input, State
from dash.exceptions import PreventUpdate
from ..helper.cached_data import PlotRenderer
from ..helper.standard_design import TOP_LEFT_TITLE, CAT_COLORS


@callback(
    Output('bubble-chart', 'figure'),
    Input('year-dropdown', 'value'),
    Input('selected-category-store', 'data'),  # Get selection from store
    Input('bubble-hover-details-switch', 'on'),
)
def update_first_layer(selected_year, selected, show_hover):
    return PlotRenderer.render_bubble_chart(
        selected_year, build_bubble_chart, selected, show_hover)


def build_bubble_chart(df, year_for_title, selected_categories=None, show_hover=False):
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
        text="Category",
        custom_data=["Category"],
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
                trace.marker.line = dict(width=2, color='blue')
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
    # If switch is OFF → hide hover details
    if not show_hover:
        fig.update_traces(
            hoverinfo="none",
            hovertemplate=None
        )

    fig.update_layout(
        title_text=f"Sales, Profit & Quantity {year_for_title}",
        title={**TOP_LEFT_TITLE},
        showlegend=False,
        plot_bgcolor="white",
        margin=dict(l=60, r=10, t=30, b=30)
    )

    fig.update_xaxes(automargin=True)
    fig.update_yaxes(automargin=True)

    return fig


# Manages the LIST of selected categories
@callback(
    Output('selected-category-store', 'data'),
    Output('bubble-chart', 'config'),
    Output('bubble-chart', 'clickData'),  # <- reset this
    Input('bubble-chart', 'clickData'),
    State('selected-category-store', 'data'),
    State('bubble-chart', 'config'),
    prevent_initial_call=True
)
def handle_bubble_click(click_data, current_selection, current_config):
    if not click_data or not click_data.get('points'):
        # nothing clicked → don't touch anything
        raise PreventUpdate

    # Ensure it's always a list
    if not isinstance(current_selection, list):
        current_selection = []

    selected_categories = current_selection.copy()
    clicked_category = click_data['points'][0]['customdata'][0]

    if clicked_category in selected_categories:
        selected_categories.remove(clicked_category)
    else:
        selected_categories.append(clicked_category)

    # third return value resets clickData -> allows clicking same bubble again
    return selected_categories, current_config or {}, None
