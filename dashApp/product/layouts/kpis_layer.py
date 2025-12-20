from dash import html, dcc

kpis_layer = html.Div(
    children=[
        dcc.Store(id='active-kpi-store', data='Sales'),
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
        ],
            id='kpi-sales-click', className='flex-1 min-w-0 active kpi-container'),

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
        ],
            id='kpi-profit-click', className='flex-1 min-w-0 kpi-container'),

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
        ], id='kpi-orders-click', className='flex-1 min-w-0 kpi-container'),
    ], className="flex flex-row justify-between items-center w-full min-w-0 gap-4 px-2 ")
