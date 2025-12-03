import dash_daq as daq

from dash import html, dcc
from .kpis_layer import kpis_layer

first_layer = html.Div(children=[
    html.Div(children=[kpis_layer,
                       html.Div(
                           dcc.Loading(
                               dcc.Graph(id='pie-chart', style={"height": "120px"}),
                               type="circle"
                           )
                       )], className="first-layer-p1"),

    html.Div(children=[

        dcc.Store(id='selected-category-store', data=[]),
        dcc.Loading(
            dcc.Graph(id='bubble-chart', style={"height": "205px"}, className="graph-shadow"),
            type="circle"
        ),
        dcc.Store(id="selected-indices-scatter-plot", data=[]),

        html.Div(
            children=[
                # 1. The Dynamic Title Area
                # NOTE: The actual title text is rendered by dcc.Graph.
                # The following components are placed immediately below that rendered title.

                # 2. THE BOOLEAN SWITCH
                daq.BooleanSwitch(
                    id="hover-details-switch",
                    on=True,
                    label="See Details on Hover",
                    labelPosition="top",
                    # Optional: Style to center the switch and add spacing above the graph
                    style={'display': 'flex', 'justifyContent': 'center', 'marginBottom': '10px', 'marginTop': '5px'}
                ),

                # 3. THE GRAPH
                dcc.Loading(
                    children=[
                        dcc.Graph(
                            id='scatter-plot',
                            # Reduced height slightly to accommodate the switch above it,
                            # while keeping the overall container size similar.
                            style={"height": "185px"},
                            className="graph-shadow"
                        )
                    ],
                    type="circle"
                )
            ],
            className="scatter-card"
        )
    ], className="first-layer-p2")

], className="first-layer")
