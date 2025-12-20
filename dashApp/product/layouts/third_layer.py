import dash_daq as daq
from dash import html, dcc
from ..helper.standard_design import THIRD_LAYER_HEIGHT

bar_heatmap_layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P("details on hover", className="mr-2 text-sm"),
                daq.BooleanSwitch(
                    id="dots-hover-details-switch",
                    on=False,
                    size=25
                ),
            ],
            className=(
                "absolute top-2 right-8 "
                "flex items-center px-3 py-1 rounded shadow z-10"
            )
        ),
        # Slider column
        dcc.Store(id='effective-top-n-store', data=5),  # Initialize with the default minimum
        html.Div(
            id='slider-container',
            children=[
                html.Div(
                    dcc.Slider(
                        min=5,
                        max=20,
                        step=5,
                        marks={i: str(i) for i in range(5, 21, 5)},
                        value=5,
                        updatemode='drag',
                        vertical=True,
                        verticalHeight=190,
                        id='product-3th-layer-p1-slider'
                    ),
                    className="flex-shrink-0 h-[200px] mr-1 flex items-center"
                )
            ]
        ),

        # Graph wrapper
        html.Div(
            html.Div(
                dcc.Loading(
                    dcc.Graph(id='product-3th-layer-p1'),
                    type="circle"
                ),
                className="w-full overflow-y-auto",
                style=THIRD_LAYER_HEIGHT
            ),
            className="flex-1 min-w-0"
        ),
        dcc.Store(id='dot-plot-click-data-store'),  # To store the raw click data
    ],
    className="flex flex-row items-start w-full relative"
)
