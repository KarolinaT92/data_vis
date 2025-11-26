from dash import callback, Output, Input
from shared.read_data import df, get_dataframe_from_store
from .scatter_plot_callbacks import build_scatter_plot
from .first_layer_callbacks import build_bubble_chart
from .second_layer_callbacks import build_time_series, build_heatmap
from .third_layer_p1_callbacks import build_bar_heatmap


# @callback(
#     Output('filtered-year-data', 'data'),
#     Input('year-dropdown', 'value')
# )
# def cache_filtered_data(selected_year):
#     # --- 1. Filter Logic (Unchanged) ---
#     if selected_year is None:
#         filtered_df = df.copy()
#         year_for_storage = "All"
#     else:
#         filtered_df = df[df['Year'] == selected_year]
#         year_for_storage = selected_year
#
#     # --- 2. Serialization ---
#     # Convert the DataFrame to JSON
#     data_json = filtered_df.to_json(date_format='iso', orient='split')
#
#     # --- 3. Return a Dictionary ---
#     # ⭐️ Return a dictionary containing both data and the year
#     return {
#         'data': data_json,
#         'year': year_for_storage}

# @callback(
#     Output('filtered-year-data', 'data'),
#     Output('bubble-store', 'data'),
#     Output('scatter-store', 'data'),
#     Output('time-series-store', 'data'),
#     Output('heatmap-store', 'data'),
#     Output('bar-heatmap-store', 'data'),
#     Input('year-dropdown', 'value')
# )
# def build_plots(selected_year):
#     filtered_df = df[df['Year'] == selected_year]
#     year = str(selected_year)
#
#     year_for_storage = selected_year
#     data_json = filtered_df.to_json(date_format='iso', orient='split')
#     filtered_year_df = {
#         'data': data_json,
#         'year': year_for_storage}
#
#     bubble_plot = build_bubble_chart(filtered_df, year)
#     scatter_plot = build_scatter_plot(filtered_df, year)
#     time_series_plot = build_time_series(filtered_df, year)
#     heatmap_plot = build_heatmap(filtered_df, year)
#     bar_heatmap_plot = build_bar_heatmap(filtered_df, year)
#
#     return filtered_year_df, bubble_plot, scatter_plot, time_series_plot, heatmap_plot, bar_heatmap_plot
