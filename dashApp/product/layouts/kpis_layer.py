from dash import html

kpis_layer = html.Div(
    children=[
        html.Div([
            html.Div(
                [
                    html.Img(
                        src="https://img.icons8.com/EBC351/ios11/2x/checkout.png",
                        className="w-6 h-6 mr-1"
                    ),
                    html.Div([
                        html.Span("Sales"),
                    ])
                ],
                className="kpi-header"
            ),
            html.H3(id='kpi-total-sales', className='font-bold m-2'),
        ], className='kpi-container'),

        html.Div([
            html.Div(
                [
                    html.Img(
                        src="https://img.icons8.com/EBC351/ios11/2x/growing-money.png",
                        className="w-6 h-6 mr-1"
                    ),
                    html.Div([
                        html.Span("Profits"),
                    ])
                ],
                className="kpi-header"
            ),
            html.H3(id='kpi-profit', className='font-bold m-2'),
        ], className='kpi-container'),

        html.Div([
            html.Div(
                [
                    html.Img(
                        src="https://img.icons8.com/EBC351/ios11/2x/shopping-basket-success.png",
                        className="w-6 h-6 mr-1"
                    ),
                    html.Div([
                        html.Span("Orders"),
                    ])

                ],
                className="kpi-header"
            ),
            html.H3(id='kpi-orders', className='font-bold m-2'),
        ], className='kpi-container'),
    ], className="kpis-box")
