from dash import callback, Output, Input
from shared.read_data import df


# @callback(Output('kpi-total-sales', 'children'),
#           Output('kpi-profit', 'children'),
#           Output('kpi-orders', 'children'),
#           Input('year-dropdown', 'value'),
#           Input('selected-category-store', 'data'),
#           Input("selected-indices-scatter-plot", "data"),
#           )
# def update_kpis(selected_year, selected_category_list, selected_ids):
#     df_selected_year = df[df["Year"] == selected_year]
#     if selected_category_list and len(selected_category_list) > 0:
#         df_selected_year = df_selected_year[df_selected_year['Category'].isin(selected_category_list)]
#     if selected_ids:
#         df_selected_year = df_selected_year[df_selected_year["Product_Key"].isin(selected_ids)]
#     sales_of_year = df_selected_year["Sales"].sum()
#     sales = f"${sales_of_year:,.0f}"
#     profit_of_year = df_selected_year["Profit"].sum()
#
#     profit = f"${profit_of_year:,.0f}"
#     orders_of_year = df_selected_year["Quantity"].sum()
#     orders = f"{orders_of_year:,}"
#     return sales, profit, orders
