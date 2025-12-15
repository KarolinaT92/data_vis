from dash import html, dcc
import dash_daq as daq
from ..helper.standard_design import SALES_COLOR, PROFIT_COLOR


def create_chart_dropdown(component_id, placeholder_text):
    return dcc.Dropdown(
        id=component_id,
        options=['bar', 'line'],
        placeholder=placeholder_text,
        clearable=False,
        style={'width': '65px', 'font-size': 12}
    )


time_series_chart_layout = html.Div(
    children=[

        dcc.Loading(dcc.Graph(id='time-series', style={"height": "235px", "width": "100%"}),
                    type="circle",
                    ),
        html.Div(children=[
            html.Div(children=[
                html.P("Sales: ", style={'color': SALES_COLOR}),
                create_chart_dropdown("sales-switch-vis", "bar")
            ], className="control-group"),

            html.Div(children=[
                html.P("Profit: ", style={'color': PROFIT_COLOR}),
                create_chart_dropdown("profit-switch-vis", "line")
            ], className="control-group")

        ], className="vis-options")
    ],
    className="third-layer-p2 relative-div",
),

heatmap_layout = html.Div(
    children=[

        # TOP-RIGHT DROPDOWN
        html.Div(
            children=[
                dcc.Dropdown(
                    id="heatmap-metric-dropdown",
                    options=["Sales", "Profit", "Profit Margin (%)"],
                    value="Profit",  # default
                    clearable=False,
                    placeholder="Metric",
                    style={
                        "fontSize": "12px",
                    },
                    className="text-xs",
                ),
            ],
            className=(
                "absolute top-2 right-3 z-10 "
                "w-32"  # adjust width as needed
            ),
        ),

        # CENTERED OVERLAY (show values switch)
        html.Div(
            children=[
                html.P("show values", className="mr-2 text-sm"),
                daq.BooleanSwitch(
                    id="heat-map-show-value-switch",
                    on=False,
                    size=25
                ),
            ],
            className=(
                "absolute top-2 left-1/2 -translate-x-1/2 "
                "flex items-center px-3 py-1 rounded shadow z-10 bg-white/80"
            ),
        ),

        # HEATMAP GRAPH
        html.Div(
            dcc.Loading(
                id="loading-heatmap",
                type="circle",
                children=dcc.Graph(
                    id="heatmap",
                    style={"height": "235px", "width": "100%"},
                ),
            )
        ),
    ],
    className="relative"
)
