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
                        "top": "-2px",        # 🔥 tweak this (e.g. -1, -2, -3) to match perfectly
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
                      id="year-dropdown",  # same ID as before
                      options=[make_option(y) for y in years],
                      value=2017,
                      labelStyle={
                          "display": "flex",
                          "alignItems": "flex-start",  # align circle with TOP of label column
                          "gap": "6px",
                          "marginBottom": "10px",
                      },
                  ),

                  # dcc.RadioItems([2014, 2015, 2016, 2017], 2017,
                  #                id='year-dropdown'),

                  ]
                 ),
        html.Div(
            [
                html.H2("Product Selector"),

                # Tree selector
                dmc.Tree(
                    id="product-tree",
                    data=TREE_DATA,  # precomputed hierarchical data
                    # checkable=True,  # show checkboxes for multi-select
                    selectOnClick=True,  # click-to-select
                    expanded=[],  # specify expanded nodes by their IDs
                    style={
                        "maxHeight": "400px",
                        "overflow": "auto",
                        "border": "1px solid #ddd",
                        "borderRadius": "6px",
                        "padding": "8px",
                        "marginBottom": "1rem",
                    },
                ),

                # Debug / info area: show current selection
                html.Pre(
                    id="product-tree-selection",
                    style={
                        "backgroundColor": "#f7f7f7",
                        "padding": "8px",
                        "borderRadius": "4px",
                        "fontSize": "0.85rem",
                    },
                ),
            ],
            # className="container",
        )
    ],
    className="left-panel"
)
