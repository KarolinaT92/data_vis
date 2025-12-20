from dash import html

kpi_layout = html.Div(
    children=[
        html.Div(
            className="kpi-container",
            children=[
                html.Div(
                    className="kpi-header",
                    children=[
                        html.Img(
                            src="https://img.icons8.com/EBC351/ios11/2x/conference-call.png",
                            className="kpi-icon",
                        ),
                        html.Div(html.Span("Customers")),
                    ],
                ),
                html.H3(id="kpi-total-customers", className="kpi-value"),
            ],
        ),
        html.Div(
            className="kpi-container",
            children=[
                html.Div(
                    className="kpi-header",
                    children=[
                        html.Img(
                            src="https://img.icons8.com/EBC351/ios11/2x/cheap-2.png",
                            className="kpi-icon",
                        ),
                        html.Div(html.Span("Avg Sales")),
                    ],
                ),
                html.H3(id="kpi-avg-sales", className="kpi-value"),
            ],
        ),
        html.Div(
            className="kpi-container",
            children=[
                html.Div(
                    className="kpi-header",
                    children=[
                        html.Img(
                            src="https://img.icons8.com/EBC351/ios11/2x/money.png",
                            className="kpi-icon",
                        ),
                        html.Div(html.Span("Avg Profit")),
                    ],
                ),
                html.H3(id="kpi-avg-profit", className="kpi-value"),
            ],
        ),
    ],
    style={
        "display": "flex",
        "flexDirection": "row",
        "gap": "12px",
        "width": "fit-content",    
        "alignItems": "flex-start",
    }
)
