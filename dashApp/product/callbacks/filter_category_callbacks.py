from dash import callback, Output, Input
import pandas as pd
from shared.read_data import df
import json


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
