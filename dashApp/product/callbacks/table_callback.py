# callbacks.py
import dash_mantine_components as dmc
from dash import callback, Output, Input, no_update, ctx
from dashApp.product.helper.standard_design import DISPLAY_COLS
from shared.read_data import df


def _as_list(x):
    """Helper: normalize store values to list."""
    if x is None:
        return []
    if isinstance(x, (list, tuple, set)):
        return list(x)
    return [x]


def _normalize_selected_indices(selected_indices_store):
    """
    Supports a few common shapes:
    - None
    - list of indices
    - dict like {"indices": [...]} or {"data": [...]} or {"selected": [...]}
    """
    if selected_indices_store is None:
        return []

    if isinstance(selected_indices_store, list):
        return selected_indices_store

    if isinstance(selected_indices_store, dict):
        for key in ("indices", "data", "selected", "value"):
            if key in selected_indices_store:
                v = selected_indices_store.get(key)
                return v if isinstance(v, list) else _as_list(v)

    # fallback
    return _as_list(selected_indices_store)


@callback(
    Output("top10-table-container", "children"),
    Input("year-dropdown", "value"),
    Input("selected-indices-scatter-plot", "data"),
    Input("effective-top-n-store", "data"),
    Input("selected-category-store", "data"),
    Input("dot-plot-click-data-store", "data"),
)
def update_product_detail_table(
    selected_year,
    selected_indices_store,
    effective_top_n,
    selected_category_store,
    clicked_data_store,
):
    # 1) Year required
    if selected_year is None:
        return dmc.Text("Select a year to display the table.")

    df_filtered = df[df["Year"] == selected_year].copy()

    # 2) Apply same filters as the graph (category + selected indices + topN later)
    # ---- Category filter ----
    selected_categories = _as_list(selected_category_store)

    # common patterns: [], None, ["All"], ["All Categories"]
    selected_categories = [
        c for c in selected_categories
        if c not in (None, "", "All", "All Categories", "ALL")
    ]

    if selected_categories:
        # If your store is Category, this is correct:
        df_filtered = df_filtered[df_filtered["Category"].isin(selected_categories)].copy()

    # ---- Selected indices filter (from scatter selection) ----
    selected_indices = _normalize_selected_indices(selected_indices_store)

    if selected_indices:
        # If the store contains row indices (typical), filter by df index
        # If it contains something else, we try to handle gracefully
        if all(isinstance(i, (int, float)) for i in selected_indices):
            selected_indices = [int(i) for i in selected_indices]
            df_filtered = df_filtered.loc[df_filtered.index.intersection(selected_indices)].copy()
        else:
            # If your store contains Product_Key(s) instead of indices
            # (this makes it robust if you later change the store)
            df_filtered = df_filtered[df_filtered["Product_Key"].isin(selected_indices)].copy()

    # If nothing left after graph filters
    if df_filtered.empty:
        return dmc.Text("No data to display after filtering.")

    # 3) Click priority: if dot clicked, show that product details (within filtered dataset)
    product_key_filter = None
    if clicked_data_store and isinstance(clicked_data_store, dict):
        product_key_filter = clicked_data_store.get("product_key")

    if product_key_filter:
        df_product = df_filtered[df_filtered["Product_Key"] == product_key_filter].reset_index(drop=True)

        if df_product.empty:
            return dmc.Text(f"No detailed records found for key: {product_key_filter}")

        df_display = df_product[DISPLAY_COLS].copy()

        product_name = (
            df_display["Product Name"].iloc[0]
            if "Product Name" in df_display.columns and not df_display.empty
            else "Selected Product"
        )
        table_caption = f"Details for: {product_name}"

    else:
        # 4) No click: show ALL rows for Top N products from the SAME filtered dataset
        try:
            top_n = int(effective_top_n) if effective_top_n is not None else 10
        except (TypeError, ValueError):
            top_n = 10

        # Use Product_Key to avoid duplicate-name problems (safer than Product Name)
        grouped = (
            df_filtered
            .groupby(["Product_Key", "Product Name", "Category", "Sub-Category"], as_index=False)
            .agg({"Sales": "sum", "Profit": "sum"})
        )

        top_keys = (
            grouped
            .sort_values("Profit", ascending=False)
            .head(top_n)["Product_Key"]
            .tolist()
        )

        df_top = df_filtered[df_filtered["Product_Key"].isin(top_keys)].reset_index(drop=True)
        df_display = df_top[DISPLAY_COLS].copy()

        # Build caption that reflects filters
        caption_parts = [f"Details of the {top_n} products"]
        if selected_categories:
            caption_parts.append(f"Category: {', '.join(map(str, selected_categories))}")
        if selected_indices:
            caption_parts.append("Selection applied")
        table_caption = " | ".join(caption_parts)

    if df_display.empty:
        return dmc.Text("No data to display after filtering.")

    # 5) Render
    head = list(df_display.columns)
    body = df_display.astype(str).values.tolist()

    return [
        dmc.Text(
            table_caption,
            style={
                "fontFamily": "Segoe UI, system-ui, -apple-system, BlinkMacSystemFont, "
                              "Roboto, Helvetica, Arial, sans-serif",
                "marginBottom": "10px",
            },
        ),
        dmc.TableScrollContainer(
            dmc.Table(
                data={"head": head, "body": body},
                striped="odd",
                highlightOnHover=True,
                withTableBorder=True,
                withColumnBorders=True,
                withRowBorders=True,
                horizontalSpacing="md",
                verticalSpacing="xs",
                stickyHeader=True,
            ),
            maxHeight=200,
            minWidth=600,
            type="scrollarea",
        ),
    ]


@callback(
    Output("dot-plot-click-data-store", "data"),
    Output("table-expanded-store", "data"),
    Output("product-3th-layer-p1", "clickData"),  # ✅ NEW: reset clickData
    Input("product-3th-layer-p1", "clickData"),
    Input("reset-table-btn", "n_clicks"),
    prevent_initial_call=True,
)
def handle_dot_click_and_reset(clickData, reset_clicks):
    trigger = ctx.triggered_id

    # -----------------------
    # RESET button clicked
    # -----------------------
    if trigger == "reset-table-btn":
        if not reset_clicks:  # None or 0
            return no_update, no_update, no_update
        # clear store + collapse + clear clickData
        return None, False, None

    # -----------------------
    # Graph clicked
    # -----------------------
    if trigger == "product-3th-layer-p1":
        if not clickData or not clickData.get("points"):
            return no_update, no_update, no_update

        point = clickData["points"][0]

        # Only react to DOT trace (curveNumber == 2)
        if point.get("curveNumber") == 2:
            product_key = (point.get("customdata") or [None])[0]
            if product_key:
                # update store + expand + clear clickData (so next same dot click works)
                return {"product_key": product_key}, True, None

        # Clicked bars/background -> ignore, but still clear clickData (optional but useful)
        return no_update, no_update, None

    return no_update, no_update, no_update


@callback(
    Output("bar-heatmap-wrapper", "style"),
    Output("product-table-wrapper", "className"),
    Output("reset-table-btn", "style"),  # 👈 change from "disabled" to "style"
    Input("table-expanded-store", "data"),
)
def toggle_last_layer(expand_version):
    expand_version = expand_version or 0
    base_table = "border-2 p-4"

    if expand_version > 0:
        return (
            {"display": "none"},  # hide bar heatmap
            f"{base_table} xl:col-span-4",  # expand table
            {"display": "inline-block"},  # show Reset button
        )

    return (
        {"display": "block"},  # show bar heatmap
        base_table,  # normal table width
        {"display": "none"},  # hide Reset button
    )
