from dash import callback, Output, Input, html
import pandas as pd
from shared.read_data import df
import json


@callback(
    Output("category-selection", 'children'),
    Input('selected-category-store', 'data'),  # a list of string
)
def update_category_selection_text(selected):

    if selected:
        # Create a list of html.Li components for each selected category
        list_items = [html.Li(category) for category in selected]

        # Wrap the list items in an html.Ul (Unordered List)
        category_list = html.Ul(list_items, style={'list-style-type': 'disc', 'padding-left': '20px'})

        # Return the main text and the list container
        return [
            html.B("Selected Categories:"),  # Use html.B for bolding the label
            category_list
        ]
    else:
        return html.P("Show category: All")  # Return a P element if only one component is needed


def build_product_tree(df: pd.DataFrame):
    """
    Build hierarchical tree:
    Category → Sub-Category → Product Name
    """
    tree = []

    for category, df_cat in df.groupby("Category"):
        cat_node = {
            "value": f"cat::{category}",
            "label": category,
            "children": []
        }

        for subcat, df_sub in df_cat.groupby("Sub-Category"):
            sub_node = {
                "value": f"sub::{category}::{subcat}",
                "label": subcat,
                "children": []
            }

            for product in sorted(df_sub["Product Name"].unique()):
                prod_node = {
                    "value": f"prod::{category}::{subcat}::{product}",
                    "label": product,
                }
                sub_node["children"].append(prod_node)

            cat_node["children"].append(sub_node)

        tree.append(cat_node)

    return tree


TREE_DATA = build_product_tree(df)
years = [2014, 2015, 2016, 2017]


@callback(
    [Output(f"quarter-wrapper-{y}", "style") for y in years],
    Input("year-dropdown", "value")
)
def show_only_selected_multiselect(selected_year):
    styles = []
    for y in years:
        if y == selected_year:
            styles.append({"display": "block"})
        else:
            styles.append({"display": "none"})
    return styles


# 1) Initialize the tree data once when the page is loaded
@callback(
    Output("product-tree", "data"),
    Input("products-init", "data"),  # any value, we don't care
    prevent_initial_call=False,
)
def init_product_tree(_):
    tree_data = TREE_DATA
    return tree_data


# 2) Example: show which nodes are checked (multi-select)
@callback(
    Output("product-tree-selection", "children"),
    Input("product-tree", "checked"),
    prevent_initial_call=False,
)
def show_checked_nodes(checked_values):
    if not checked_values:
        return "No selection."
    # For now just show them; later you filter df based on these
    return json.dumps(checked_values, indent=2, ensure_ascii=False)
