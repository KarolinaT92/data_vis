import plotly.express as px
from dash import callback, Output, Input, State, callback_context
from shared.read_data import get_dataframe_from_store, df

blue_theme_colors = [
    '#6A9AC4',  # Light Steel Blue
    '#9BBFE0',  # Powder Blue
    '#B4CDE6',  # Pale Blue
    '#8FAADC',  # Lavender Blue (slightly purple-ish)
    '#A7D9E7',  # Sky Blue (lighter, more cyan)
    '#C0DFF0',  # Lighter Blue
    '#D7EDF9'  # Very Light Blue
]


@callback(
    Output('active-kpi-store', 'data'),  # 1. Output to store the active metric
    Output('kpi-sales-click', 'className'),  # 2. Output to update Sales container class
    Output('kpi-profit-click', 'className'),  # 3. Output to update Profits container class
    Output('kpi-orders-click', 'className'),  # 4. Output to update Orders container class
    Input('kpi-sales-click', 'n_clicks'),  # Input for Sales clicks
    Input('kpi-profit-click', 'n_clicks'),  # Input for Profits clicks
    Input('kpi-orders-click', 'n_clicks'),  # Input for Orders clicks
    State('active-kpi-store', 'data'),  # State of the current active metric
    prevent_initial_call=True
)
def handle_kpi_click(n_sales, n_profit, n_orders, current_active_kpi):
    # Determine which KPI was most recently clicked
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]

    # 1. Determine the new active KPI name
    if 'kpi-sales-click' in changed_id:
        new_active_kpi = 'Sales'
    elif 'kpi-profit-click' in changed_id:
        new_active_kpi = 'Profits'
    elif 'kpi-orders-click' in changed_id:
        new_active_kpi = 'Orders'
    else:
        # Should not happen, but return current state if initial call is not prevented
        return current_active_kpi, 'kpi-container', 'kpi-container', 'kpi-container'

    # Define the base class string
    base_class = 'kpi-container'
    active_class = 'kpi-container active'

    # 2. Return the updated store data and the new class names
    return (
        new_active_kpi,
        active_class if new_active_kpi == 'Sales' else base_class,
        active_class if new_active_kpi == 'Profits' else base_class,
        active_class if new_active_kpi == 'Orders' else base_class
    )


@callback(Output('pie-chart', 'figure'),
          Input('active-kpi-store', 'data'),
          Input('year-dropdown', 'value'),
          Input('selected-category-store', 'data'),
          Input("selected-indices-scatter-plot", "data"),
          )

def update_pie(selected_metric, selected_year, selected_category_list, selected_ids):
    filtered_df = df[df['Year'] == selected_year]
    if selected_category_list and len(selected_category_list) > 0:
        filtered_df = filtered_df[filtered_df['Category'].isin(selected_category_list)]

    if selected_ids:
        filtered_df = filtered_df[filtered_df["Product_Key"].isin(selected_ids)]

    # 1. Get the column name corresponding to the metric
    if selected_metric == 'Sales':
        column_name = 'Sales'
        hover_template = "Sales: %{value:$,.0f}<extra></extra>"
    elif selected_metric == 'Profits':
        column_name = 'Profit'
        hover_template = "Profit: %{value:$,.0f}<extra></extra>"
    else:  # Orders
        print(df['Quantity'].dtype)
        column_name = 'Quantity'
        hover_template = "Quantity: %{value:,}<extra></extra>"

    agg_df = filtered_df.groupby('Region', as_index=False)[column_name].sum()
    fig = px.pie(
        agg_df,
        names='Region',
        hover_name='Region',
        values=column_name,
        hole=.7,
        color_discrete_sequence=blue_theme_colors  # Use your theme colors
    )

    # 3. Apply your desired trace/layout customizations again
    fig.update_traces(textposition='outside', textinfo='percent+label',
                      hovertemplate=hover_template),

    background_color = '#ffffff'

    fig.update_layout(showlegend=False, uniformtext_minsize=12, plot_bgcolor=background_color,
                      paper_bgcolor=background_color, margin=dict(t=20, b=20, l=20, r=20))

    return fig
