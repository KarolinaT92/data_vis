# callbacks.py
import dash_mantine_components as dmc
from dash import callback, Output, Input
from dashApp.product.helper.standard_design import DISPLAY_COLS
from shared.read_data import df
import pandas as pd


@callback(
    Output("top10-table-container", "children"),
    Input('year-dropdown', 'value'),
    # --- NEW INPUT: The dcc.Store containing the clicked product key ---
    Input('dot-plot-click-data-store', 'data')
)
def update_product_detail_table(selected_year, clicked_data_store):
    # 1. Preliminary Check (Year)
    if selected_year is None:
        return dmc.Text("Select a year to display the table.")

    df_year = df[df['Year'] == selected_year].copy()

    # Initialize the filtered DataFrame and the table caption
    df_display = pd.DataFrame(columns=df.columns)
    table_caption = ""

    product_key_filter = None

    # 2. Check for Clicked Product Key (Prioritized Filtering)
    if clicked_data_store and 'product_key' in clicked_data_store:
        product_key_filter = clicked_data_store['product_key']

    if product_key_filter:
        # --- CASE 1: DOT CLICKED (Filter by unique Product_Key) ---

        # Filter the year's data by the exact unique key using the confirmed column name
        df_filtered = df_year[df_year['Product_Key'] == product_key_filter].reset_index(drop=True)

        if df_filtered.empty:
            return dmc.Text(f"No detailed records found for key: {product_key_filter}")

        # The table only displays a subset of columns (DISPLAY_COLS)
        df_display = df_filtered[DISPLAY_COLS].copy()

        # Extract the Product Name for a descriptive caption
        product_name = df_display['Product Name'].iloc[
            0] if not df_display.empty and 'Product Name' in df_display.columns else 'Selected Product'
        table_caption = f"Detail records for: {product_name} (Key: {product_key_filter}) — {len(df_display)} rows"

    else:
        # --- CASE 2: NO DOT CLICKED (Fallback to Top 10) ---

        # Re-implement the original top 10 logic
        grouped = (
            df_year
            .groupby(["Product Name", "Category", "Sub-Category"], as_index=False)
            .agg({"Sales": "sum", "Profit": "sum"})
        )
        top10_names = grouped.sort_values("Profit", ascending=False).head(10)["Product Name"].tolist()

        # Keep all rows for the top10 products
        top10_all_rows = df_year[df_year["Product Name"].isin(top10_names)].reset_index(drop=True)
        df_display = top10_all_rows[DISPLAY_COLS].copy()

        table_caption = f"Top 10 profitable products (Aggregated View) — {len(df_display)} rows"

    # 3. Render the dmc.Table
    if df_display.empty:
        return dmc.Text("No data to display after filtering.")

    # Convert to strings for dmc.Table body
    head = list(df_display.columns)
    body = df_display.astype(str).values.tolist()

    return (
        dmc.TableScrollContainer(
            dmc.Table(
                data={
                    "caption": table_caption,
                    "head": head,
                    "body": body,
                },
                striped="odd",
                highlightOnHover=True,
                withTableBorder=True,
                withColumnBorders=True,
                withRowBorders=True,
                horizontalSpacing="md",
                verticalSpacing="xs",
                stickyHeader=True,
            ),
            maxHeight=250,
            minWidth=600,
            type="scrollarea",
        )
    )
