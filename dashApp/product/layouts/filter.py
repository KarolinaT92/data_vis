from dash import html, dcc
import dash_mantine_components as dmc

from dashApp.product.callbacks.filter_category_callbacks import TREE_DATA


def filter_year():
    pass


filter_layout = html.Div(
    [
        html.Div([html.H3("Filters"),
                  dcc.RadioItems([2014, 2015, 2016, 2017], 2017, id='year-dropdown')]
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
