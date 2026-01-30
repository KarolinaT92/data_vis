from dash import Input, Output, callback
from dashApp.product.constants import CATEGORY_DROPDOWN_ID, REGION_DROPDOWN_ID
from dashApp.template.layouts.filter_options import CATEGORIES, REGIONS


# prevent empty selection in category dropdown
@callback(
    Output(CATEGORY_DROPDOWN_ID, "value"),
    Input(CATEGORY_DROPDOWN_ID, "value"),
    prevent_initial_call=True,
)
def empty_means_all(new_value):
    if not new_value:
        return CATEGORIES
    return new_value


# prevent empty selection in region dropdown
@callback(
    Output(REGION_DROPDOWN_ID, "value"),
    Input(REGION_DROPDOWN_ID, "value"),
    prevent_initial_call=True,
)
def empty_means_all(new_value):
    if not new_value:
        return REGIONS
    return new_value