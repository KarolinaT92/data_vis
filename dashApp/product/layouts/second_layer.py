from dash import html, dcc


def create_chart_dropdown(component_id, placeholder_text):
    return dcc.Dropdown(
        id=component_id,
        options=['bar', 'line'],
        placeholder=placeholder_text,
        clearable=False,
        style={'width': '65px', 'font-size': 12}
    )


second_layer = html.Div(
    children=[
        html.Div(
            children=[

                dcc.Loading(dcc.Graph(id='time-series', style={"height": "235px", "width": "100%"}),
                            type="circle",
                            ),
                html.Div(children=[
                    html.Div(children=[
                        html.P("Sales: "),
                        create_chart_dropdown("sales-switch-vis", "bar")
                    ], className="control-group"),

                    html.Div(children=[
                        html.P("Profit: "), create_chart_dropdown("profit-switch-vis", "line")
                    ], className="control-group")

                ], className="vis-options")
            ],
            className="third-layer-p2 relative-div",
        ),
        html.Div(
            dcc.Loading(
                id="loading-heatmap",
                type="circle",
                children=dcc.Graph(id="heatmap", style={"height": "235px", "width": "100%"}),
            ),
            className="third-layer-p1",
        )
    ],
    className="second-layer"
)
