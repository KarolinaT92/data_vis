from dash import html, dcc

second_layer = html.Div(
    children=[
        html.Div(
            dcc.Loading(dcc.Graph(id='time-series', style={"height": "260px", "width": "100%"}),
                        type="circle",
                        ),
            className="flex-[0.35] min-w-0 flex flex-col border-1 rounded-[5px] shadow-xl",
        ),
        html.Div(
            dcc.Loading(
                id="loading-heatmap",
                type="circle",
                children=dcc.Graph(id="heatmap", style={"height": "260px", "width": "100%"}),
            ),
            className="flex-[0.65] min-w-0 border-1 rounded-[5px] shadow-xl flex flex-col",
        )
    ],
    className="second-layer"
)
