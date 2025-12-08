import plotly.express as px
from dash import Input, Output, callback
from ..helper.cached_data import PlotRenderer
from ..helper.standard_design import TOP_LEFT_TITLE, MONTH_ORDER
import pandas as pd


@callback(Output('heatmap', 'figure'),
          Input('year-dropdown', 'value'),
          Input("selected-indices-scatter-plot", "data"),
          Input('selected-category-store', 'data'),
          Input('heat-map-show-value-switch', 'on'),
          Input('heatmap-metric-dropdown', 'value'),
          )
def update_graph(selected_year, selected_ids, selected_category_list, show_heatmap_values, metric):
    heatmap_fig = PlotRenderer.render_from_scatter_selection(selected_year,
                                                             selected_ids,
                                                             "heatmap",
                                                             build_heatmap,
                                                             selected_category_list,
                                                             show_heatmap_values,
                                                             metric)

    return heatmap_fig


def build_heatmap(
        df,
        year_for_title,
        selected_category_list,
        show_heatmap_values=False,
        metric="Profit"):
    # 1. Filter the DataFrame by selected categories (if any)
    if selected_category_list and len(selected_category_list) > 0:
        df = df[df["Category"].isin(selected_category_list)]

    # Determine the grouping column based on the selection
    group_col = "Category"
    if selected_category_list and len(selected_category_list) == 1:
        # If only one category is selected, group by Sub-Category instead
        group_col = "Sub-Category"

    if metric == "Profit Margin (%)":
        value_col = "Profit Margin (%)"
        color_label = "Profit Margin (%)"
        title_metric = "Profit Margin (%)"

        # Use existing rounded column, do NOT recompute margin
        heat_data = (
            df.groupby([group_col, "Month_Name"], as_index=False)[value_col]
            .mean()
        )
        # keep 2 decimals, same as your original df
        heat_data[value_col] = heat_data[value_col].round(2)

    else:
        # Sales or Profit
        value_col = metric  # "Sales" or "Profit"
        color_label = f"Total {metric} ($)" if metric != "Profit Margin (%)" else "Total Profit ($)"
        title_metric = metric

        heat_data = (
            df.groupby([group_col, "Month_Name"], as_index=False)[value_col]
            .sum()
        )

    # pivot
    heat_matrix = heat_data.pivot(index=group_col, columns="Month_Name", values=value_col)
    heat_matrix = heat_matrix.reindex(columns=MONTH_ORDER)

    # 4. Create formatted text for display
    if metric == "Profit Margin (%)":
        # show as percentage with 1 decimal place
        heat_matrix_formatted = heat_matrix.apply(
            lambda col: col.map(
                lambda x: f"{x:.1f}" if pd.notnull(x) else ""
            )
        )
    else:
        # money values: show K with 1 decimal place
        heat_matrix_formatted = heat_matrix.apply(
            lambda col: col.map(
                lambda x: f"{x / 1000:.3f}" if pd.notnull(x) else ""
            )
        )

    # 5. Create the heatmap figure
    fig_heatmap = px.imshow(
        heat_matrix,
        aspect="auto",
        color_continuous_scale="Blues",
        labels=dict(color=color_label),
        title=f"Monthly {title_metric} made by {group_col} {year_for_title}",
    )

    if show_heatmap_values:
        fig_heatmap.update_traces(
            text=heat_matrix_formatted.values,  # 2D array of strings
            texttemplate="%{text}",  # show the text as-is
            # textfont=dict(size=10),
        )

    # 6. Update layout
    fig_heatmap.update_layout(
        xaxis_title="Month",
        yaxis_title=group_col,
        margin=dict(l=60, r=40, t=60, b=60),
        coloraxis_colorbar=dict(title=color_label),
        title_text=f"Monthly {title_metric} made by {group_col} {year_for_title}",
        title={**TOP_LEFT_TITLE},
    )

    return fig_heatmap
