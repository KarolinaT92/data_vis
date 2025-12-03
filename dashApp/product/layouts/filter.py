from dash import html, dcc
import dash_mantine_components as dmc
from dashApp.product.callbacks.filter_category_callbacks import TREE_DATA

years = [2014, 2015, 2016, 2017]


def make_option(year):
    return {
        "label": html.Div(
            [
                # This line is visually aligned with the radio circle
                html.Span(
                    str(year),
                    style={
                        "display": "inline-block",
                        "position": "relative",
                        "top": "-2px",  # 🔥 tweak this (e.g. -1, -2, -3) to match perfectly
                        "fontWeight": 500,
                    },
                ),

                # MultiSelect sits BELOW the year, doesn’t affect alignment
                html.Div(
                    # dmc.MultiSelect(
                    #     id=f"quarter-multi-{year}",
                    #     data=[f"Q{i}" for i in range(1, 5)],
                    #     placeholder="All quarters",
                    #     style={"minWidth": "140px"},
                    # ),
                    dcc.Checklist(
                        options=['All quarters', 'Q1', 'Q2', 'Q3', 'Q4'],
                        value=['All quarters'],
                    ),
                    id=f"quarter-wrapper-{year}",
                    style={"display": "none", "marginTop": "4px"},
                ),
            ],
            style={
                "display": "flex",
                "flexDirection": "column",
            },
        ),
        "value": year,
    }


filter_layout = html.Div(
    [
        html.Div([html.H3("Filters"),
                  dcc.RadioItems(
                      id="year-dropdown",
                      options=[make_option(y) for y in years],
                      value=2017,
                      labelStyle={
                          "display": "flex",
                          "alignItems": "flex-start",  # align circle with TOP of label column
                          "gap": "6px",
                          "marginBottom": "10px",
                      }
                  )
                  ]
                 ),

    ],
    className="left-panel"
)
