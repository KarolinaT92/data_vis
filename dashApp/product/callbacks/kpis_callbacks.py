from dash import callback, Output, Input
from shared.read_data import df


@callback(Output('kpi-total-sales', 'children'),
          Output('kpi-profit', 'children'),
          Output('kpi-orders', 'children'),
          Input('year-dropdown', 'value'))

def update_kpis(selected_year):
    df_selected_year = df[df["Year"] == selected_year]
    sales_of_year = df_selected_year["Sales"].sum()
    sales = f"${sales_of_year:,.0f}"
    profit_of_year = df_selected_year["Profit"].sum()

    profit = f"${profit_of_year:,.0f}"
    orders_of_year = df_selected_year["Order ID"].nunique()
    orders = f"{orders_of_year:,}"
    return sales, profit, orders
