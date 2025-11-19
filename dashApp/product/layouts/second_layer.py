from dash import html, dcc

second_layer = html.Div(
    children=[
        html.Div(
            dcc.Graph(id='heatmap'),
            className="flex-[0.35] min-w-0 overflow-hidden"
        ),
        html.Div(dcc.Graph(id='time-series'), className="flex-[0.65]  min-w-0 overflow-hidden")

    ], className="flex gap-4 h-96")
