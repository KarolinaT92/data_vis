import plotly.express as px
from dash import callback, Output, Input, State, callback_context
from shared.read_data import get_dataframe_from_store

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
          Input('filtered-year-data', 'data'))
def update_pie(selected_metric, stored_data_dict):
    data_json = stored_data_dict.get('data')
    dff = get_dataframe_from_store(data_json)

    # 1. Get the column name corresponding to the metric
    if selected_metric == 'Sales':
        column_name = 'Sales'
    elif selected_metric == 'Profits':
        column_name = 'Profit'
    else:  # Orders
        column_name = 'Quantity'

    fig = px.pie(
        dff,  # Use your actual DataFrame here
        names='Region',
        values=column_name,  # ⭐️ Dynamically set the values column
        hole=.7,
        color_discrete_sequence=blue_theme_colors  # Use your theme colors
    )

    # 3. Apply your desired trace/layout customizations again
    fig.update_traces(textposition='outside', textinfo='percent+label',
                      hovertemplate="%{label}<br>Sales: %{value:$,.2f}<br>Percentage: %{percent}<extra></extra>"),

    background_color = '#ffffff'

    fig.update_layout(showlegend=False, uniformtext_minsize=12, plot_bgcolor=background_color,
                      paper_bgcolor=background_color)

    return fig
