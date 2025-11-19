from dash import html, dcc


def filter_year():
    pass


filter_layout = html.Div(
    [
        html.H3("Filters"),
        dcc.RadioItems([2014, 2015, 2016, 2017], 2017, id='year-dropdown'),
    ],
    className="left-panel"
)
