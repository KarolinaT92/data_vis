from dash import html, dcc
from .filter import filter_layout
from .first_layer import scatter_plot_layout, bubble_chart_layout
from .kpis_layer import kpis_layer
from .second_layer import heatmap_layout, time_series_chart_layout
from .table_layout import product_table_layout
from .third_layer import bar_heatmap_layout
from ..helper.standard_design import PIE_CHART_HEIGHT

right_layout = html.Div(
    [
        # dcc.Store(id='selected-category-store', data=[]),
        dcc.Store(id="selected-indices-scatter-plot", data=[]),
        html.Div(children=[
            html.Div(
                [
                    kpis_layer,

                    html.Div(children=[
                        html.Div(
                            dcc.Loading(
                                dcc.Graph(id='pie-chart', style=PIE_CHART_HEIGHT),
                                type="circle"
                            )
                        )
                    ], className="border-2"),
                ],
                className="flex flex-col gap-2",
            )
        ], className="border-2"),
        # bubble chart
        html.Div(children=bubble_chart_layout, className="border-2"),
        # sctatter plot
        html.Div(children=scatter_plot_layout, className="border-2 xl:col-span-2"),
        # time series chart
        html.Div(children=time_series_chart_layout, className="border-2 xl:col-span-2"),
        # heatmap
        html.Div(children=heatmap_layout, className="border-2 xl:col-span-2"),
        # bar and heatmap
        html.Div(children=bar_heatmap_layout, className="border-2 xl:col-span-3"),
        # table
        html.Div(children=product_table_layout, className="border-2 p-4"),
    ],
    className="grid grid-cols-1 xl:grid-cols-4 gap-4",
)

layout = html.Div(
    [
        filter_layout,
        html.Div(
            [
                right_layout
            ],
            className=(
                "right-panel "
                "overflow-y-auto xl:overflow-y-visible "
                # "overflow-auto lg:overflow-visible "  # width logic
                # "[@media(max-height:768px)]:overflow-y-auto "  # height logic
                # "[@media(max-height:768px)]:max-h-[85vh]"  # height limit
            )
            # className="right-panel max-h-[85vh] overflow-y-auto lg:max-h-none lg:overflow-y-visible"
        )
    ],
    className="container"
)
