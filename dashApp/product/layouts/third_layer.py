import dash_daq as daq
from dash import html, dcc
from ..helper.standard_design import THIRD_LAYER_HEIGHT

bar_heatmap_layout = html.Div(
    children=[
        # Hover toggle (unchanged)
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

        dcc.Store(id='effective-top-n-store', data=5),

        # Slider column (VERTICALLY CENTERED)
        html.Div(
            id='slider-container',
            className="flex items-center justify-center",
            style=THIRD_LAYER_HEIGHT,   # 👈 same height as graph
            children=[
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

        dcc.Store(id='dot-plot-click-data-store'),
    ],

    # 👇 important change here
    className="flex flex-row items-center w-full relative"
)
