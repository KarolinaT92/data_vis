from dash import html

img_source = "https://img.icons8.com/EBC351/ios11/2x/conference-call.png"
kpi_title = "Customers"
kpi_id = "kpi-total-customers"

kpi_layout = html.Div([
    html.Div(
        [
            html.Img(
                src=img_source,
                className="w-10 h-10 mr-3"
            ),
            html.Div([
                html.Span(kpi_title),
            ])
        ],
        className="kpi-header"
    ),
    html.H3(id=kpi_id, className='font-bold m-2'),
])
