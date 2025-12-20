from dash import Input, Output, callback


@callback(Output('slider-container', 'style'),
          Input('selected-indices-scatter-plot', 'data'))
def toggle_slider_visibility(selected_ids):
    """
    Toggles the slider visibility.
    1. Show the slider if NO points are selected (to control "Top N" global products).
    2. Hide the slider if a small selection (count < 20) is made.
    3. Show the slider if a large selection (count >= 20) is made.
    """
    number_of_selected = len(selected_ids) if selected_ids else 0

    if selected_ids is None:
        count = 0
    else:
        count = len(selected_ids)

    # Condition 1: No selection (count = 0)
    if count == 0:
        # Show the slider (default state)
        return {'display': 'block'}  # or 'flex'

    # Conditions 2 & 3: Selection was made
    elif count < 20:
        # Hide the slider (it's not useful to filter a small group)
        return {'display': 'none'}
    else:  # count >= 20
        # Show the slider (to let the user pick Top/Bottom N from their selection)
        return {'display': 'block'}


@callback(Output('effective-top-n-store', 'data'),
          Input("selected-indices-scatter-plot", "data"),
          Input('product-3th-layer-p1-slider', 'value'))
def update_effective_top_n(selected_ids, slider_value):
    """
    Calculates the final 'top_n' limit to be used by the plot:
    1. If no selection (count = 0), use the slider value (default 5).
    2. If selection is small (0 < count < 20), override to show ALL (use count).
    3. If selection is large (count >= 20), use the slider value.
    """

    if selected_ids is None:
        count = 0
    else:
        count = len(selected_ids)

    # 1. No selection (Initial load or clear selection)
    if count == 0:
        # Use the slider's value (e.g., 5, 10, 20)
        return slider_value

        # 2. Small selection
    elif count < 20:
        # Override and force top_n to be the total count (show all selected)
        return count

        # 3. Large selection
    else:  # count >= 20
        # Use the slider's value to filter the large selection
        return slider_value