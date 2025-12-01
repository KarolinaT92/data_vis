import plotly.express as px
from dash import Input, Output, callback
from ..helper.cached_data import PlotRenderer
from ..helper.standard_design import TOP_LEFT_TITLE


@callback(Output('heatmap', 'figure'),
          Input('year-dropdown', 'value'),
          Input("selected-indices-scatter-plot", "data"),
          )
def update_graph(selected_year, selected_ids):
    heatmap_fig = PlotRenderer.render_from_scatter_selection(selected_year,
                                                             selected_ids,
                                                             "heatmap",
                                                             build_heatmap)

    return heatmap_fig


def build_heatmap(df, year_for_title):
    heat_data = (
        df.groupby(["Category", "Month_Name"], as_index=False)["Profit"]
        .sum()
    )

    # Pivot to heatmap matrix
    heat_matrix = heat_data.pivot(index="Category", columns="Month_Name", values="Profit")

    fig_heatmap = px.imshow(
        heat_matrix,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="Blues",
        labels=dict(color="Total Profit ($)"),
        title=f"Monthly Profit made by Categories {year_for_title}",
    )

    fig_heatmap.update_layout(
        xaxis_title="Month",
        yaxis_title="Category",
        margin=dict(l=60, r=40, t=60, b=60),
        coloraxis_colorbar=dict(title="Profit ($)"),
        title_text=f"Monthly Profit made by Categories {year_for_title}",
        title={**TOP_LEFT_TITLE},
    )
    return fig_heatmap
