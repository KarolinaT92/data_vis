from dash import html, dcc

years = [2014, 2015, 2016, 2017]


def make_option(year):
    return {
        "label": html.Div(
            [
                html.Span(
                    str(year),
                    style={
                        "display": "inline-block",
                        "position": "relative",
                        "top": "-2px",
                        "fontWeight": 500,
                    },
                ),
            ],
            style={
                "display": "flex",
                "flexDirection": "column",
            },
        ),
        "value": year,
    }


shipment_filter_layout = html.Div(
    [
        html.H3("Filters"),

        dcc.RadioItems(
            id="shipment-year-radio",
            options=[make_option(y) for y in years],
            value=2017,
            labelStyle={
                "display": "flex",
                "alignItems": "flex-start",
                "gap": "6px",
                "marginBottom": "10px",
            },
        ),
    ],
    style={
        "width": "260px",              
        "minWidth": "260px",          
        "padding": "16px",
        "background": "#f7f7f7",
        "borderRight": "1px solid #ddd",

        "position": "sticky",
        "top": "60px",                 
        "alignSelf": "flex-start",
    },
)

