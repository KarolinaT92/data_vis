from dash import Input, Output, callback
from dash import html
from dashApp.product.constants import CATEGORY_DROPDOWN_ID, SELECT_ON_SCATTER_PLOT
from dashApp.product.helper import react_to_category_dropdown
from shared.read_data import df


# ROW 1 — KPI UPDATES

@callback(
    Output('kpi-total-sales', 'children'),
    Output('kpi-profit', 'children'),
    Output('kpi-orders', 'children'),
    Input("shipment-year", "value"),
    Input(CATEGORY_DROPDOWN_ID, "value"),
    Input(SELECT_ON_SCATTER_PLOT, "data"),
    # Input("shipment-region", "value"),
)
def update_kpis(year, selected_categories, selected_ids):
    dff = react_to_category_dropdown(df, year, selected_categories)
    if selected_ids:
        dff = dff[dff["Product_Key"].isin(selected_ids)]

    sales_of_year = dff["Sales"].sum()
    sales = f"${sales_of_year:,.0f}"
    profit_of_year = dff["Profit"].sum()

    profit_class = "text-red-600 font-bold m-2" if profit_of_year < 0 else "font-bold m-2"
    profit = html.Span(f"${profit_of_year:,.0f}", className=profit_class)
    orders_of_year = dff["Quantity"].sum()
    orders = f"{orders_of_year:,}"
    return sales, profit, orders
