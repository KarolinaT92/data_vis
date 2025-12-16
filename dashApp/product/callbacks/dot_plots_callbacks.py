from dash import Input, Output, callback


@callback(
    # Output to your dcc.Store component
    Output('dot-plot-click-data-store', 'data'),
    # Input from the graph's clickData property
    Input('product-3th-layer-p1', 'clickData'),
    prevent_initial_call=True
)
def store_dot_plot_click_data(clickData):
    """
    Handles click events on the main product plot, extracts the unique
    Product_Key from the clicked dot, and stores it in a dcc.Store.
    """
    # 1. Check for valid click data
    if clickData is None or not clickData.get('points'):
        return None

    point = clickData['points'][0]

    # 2. Check if the click was on the dot plot trace (curveNumber: 2)
    if point.get('curveNumber') == 2:
        # The customdata structure is:
        # ['Product_Key', 'Full Product Name', 'Count']

        # 3. Extract the Product_Key (index 0 of customdata)
        # Using .get() with a default list to safely access customdata
        product_key = point.get('customdata', [None])[0]

        if product_key:
            # 4. Store the key in the dcc.Store
            return {'product_key': product_key}

    # If the click was on a bar trace (0 or 1) or the key was missing,
    # we return None to clear the store.
    return None