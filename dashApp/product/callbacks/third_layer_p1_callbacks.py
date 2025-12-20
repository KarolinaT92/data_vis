import numpy as np
import plotly.graph_objects as go
from dash import Input, Output, callback
from plotly.subplots import make_subplots
from ..helper.cached_data import PlotRenderer
from ..helper.standard_design import TOP_LEFT_TITLE, SALES_COLOR, PROFIT_COLOR
import pandas as pd


def truncate_name(name, max_len=30):
    return name if len(name) <= max_len else name[:max_len] + "…"


@callback(Output('product-3th-layer-p1', 'figure'),
          Input('year-dropdown', 'value'),
          Input("selected-indices-scatter-plot", "data"),
          Input('effective-top-n-store', 'data'),
          Input('selected-category-store', 'data'),
          Input('dots-hover-details-switch', 'on'),
          )
def update_first_layer(selected_year, selected_ids, top_n, selected_category_list, show_dot_values):
    return PlotRenderer.render_plot_top_profitable_products(selected_year, selected_ids,
                                                            build_bar_heatmap, top_n, selected_category_list,
                                                            show_dot_values)


def build_bar_heatmap(df, year_for_title, top_n, selected_category_list=None,
                      show_dot_values=False, number_of_selected=0):
    if selected_category_list and len(selected_category_list) > 0:
        df = df[df['Category'].isin(selected_category_list)]

    grouped = (
        df.groupby(["Product Name", "Category", "Sub-Category"], as_index=False)
        .agg({"Sales": "sum", "Profit": "sum"})
    )

    top_products = grouped.sort_values("Profit", ascending=False).head(top_n)

    top_products["Product Name Short"] = top_products["Product Name"].apply(
        truncate_name
    )

    profit_min = float(top_products["Profit"].min())
    profit_max = float(top_products["Profit"].max())
    sales_max = float(top_products["Sales"].max())

    # Left bound must include negative profit (and 0)
    left = min(profit_min, 0.0)

    # Right bound must be big enough for BOTH profit and sales (and 0)
    right = max(profit_max, sales_max, 0.0)

    # Padding
    span = right - left
    if span == 0:
        span = max(abs(left), abs(right), 1.0)

    pad = span * 0.15
    shared_range = [left - pad, right + pad]

    # This is THE master order for both subplots
    profit_order_short = top_products["Product Name Short"].tolist()
    y_vals = profit_order_short

    # Filter raw df to only those products (for dot plot)
    df_top = df[df["Product Name"].isin(top_products["Product Name"].tolist())].copy()
    df_top["Discount"] = df_top["Discount"].round(2)

    name_map = top_products[['Product Name', 'Product Name Short']].set_index('Product Name')[
        'Product Name Short'].to_dict()
    df_top['Product Name Short'] = df_top['Product Name'].map(name_map)

    summary_by_discount = (
        df_top
        .groupby(["Product_Key", "Discount", "Product Name Short"], as_index=False)
        .agg(
            **{
                "Avg Profit Margin (%)": ("Profit Margin (%)", "mean"),
                "Count": ("Profit", "size"),
                "Total Quantity": ("Quantity", "sum"),
            }
        )
    )

    summary_by_discount = summary_by_discount.dropna(subset=["Avg Profit Margin (%)"])

    # --- Discount axis ticks ---
    max_discount = summary_by_discount["Discount"].max()
    if pd.isna(max_discount) or max_discount is None:
        # If no data is available, set a default max discount for the axis (e.g., 0.5 for 50%)
        # This prevents the arange error and keeps the chart from crashing.
        max_discount = 0.0
        full_x_vals = np.arange(0.0, max_discount + 0.1, 0.1)
    else:
        # Proceed with the calculated max discount
        full_x_vals = np.arange(0.0, max_discount + 0.1, 0.1)

    full_tick_text = [f"{x * 100:.0f}%" for x in full_x_vals]

    fig = make_subplots(
        rows=1, cols=2,
        shared_yaxes=True,
        column_widths=[0.55, 0.45],
        horizontal_spacing=0.08,
        specs=[[{"type": "xy"}, {"type": "xy"}]],
    )

    # ----- Left subplot: use top_products, NOT top10 -----
    profit_trace = go.Bar(
        x=top_products["Profit"],
        y=top_products["Product Name Short"],
        orientation="h",
        name="Profit",
        marker=dict(
            color=PROFIT_COLOR,
        ),
        width=0.4,
        text=top_products["Profit"].map("{:,.0f}".format),
        textposition="none",
        textfont=dict(size=13, color=PROFIT_COLOR),  # color="#003366"
        cliponaxis=False,
        # **<-- MODIFIED customdata: Add 'Product Name' as the first element (index 0) -->**
        customdata=top_products[["Product Name", "Category", "Sub-Category", "Sales"]].values,
        hovertemplate=(
            "<b>Product: %{customdata[0]}</b><br>"  # Use the full product name
            "Profit: %{x:,.2f}<br>"
            "Category: %{customdata[1]}<br>"
            "Sub-Category: %{customdata[2]}"
            "<extra></extra>"
        )
    )
    fig.add_trace(profit_trace, row=1, col=1)

    sales_trace = go.Bar(
        x=top_products["Sales"],
        y=top_products["Product Name Short"],
        orientation="h",
        name="Sales",
        marker=dict(color=SALES_COLOR),  # color=orange
        width=0.1,
        text=top_products["Sales"].map("{:,.0f}".format),
        textposition="outside",
        outsidetextfont=dict(size=10, color=SALES_COLOR, family="Arial Black"),  # color=orange_dark
        insidetextanchor="start",
        cliponaxis=False,
        # **<-- MODIFIED customdata: Add 'Product Name' (using profit_trace's customdata) -->**
        customdata=top_products[["Product Name", "Category", "Sub-Category", "Sales"]].values,
        hovertemplate=(
            "<b>Product: %{customdata[0]}</b><br>"  # Use the full product name
            "Sales: %{customdata[3]:,.2f}<br>"
            "Category: %{customdata[1]}<br>"
            "Sub-Category: %{customdata[2]}"
            "<extra></extra>"
        )
    )
    fig.add_trace(sales_trace, row=1, col=1)

    # ----- Right subplot: Dot Plot -----
    # 1. Determine the mode based on the switch
    if show_dot_values:
        dot_mode = "markers+text"
    else:
        dot_mode = "markers"  # <--- Toggles to hide the text
        # This prevents the issue of Plotly discarding the text array permanently.

    # Merge full product name into summary_by_discount
    summary_by_discount = pd.merge(
        summary_by_discount,
        top_products[['Product Name', 'Product Name Short']],
        on='Product Name Short',
        how='left'
    ).drop_duplicates()

    dot_plot = go.Scatter(
        x=summary_by_discount["Discount"],
        y=summary_by_discount["Product Name Short"],

        mode=dot_mode,
        marker=dict(
            size=25,
            color=summary_by_discount["Avg Profit Margin (%)"],
            colorscale="RdBu",  # Green red: "RdYlGn", blue-yellow-red": RdYlBu"
            colorbar=dict(title="Profit Margin (%)"),
            showscale=True,
        ),
        text=summary_by_discount["Avg Profit Margin (%)"].round(1).astype(str),
        textfont=dict(size=10, color="black"),
        textposition="middle center",
        customdata=summary_by_discount[["Product_Key", "Product Name", "Total Quantity"]].values,
        hovertemplate=(
            "<b>Product: %{customdata[1]}</b><br>"  # Use full product name
            "Profit Margin: %{marker.color:.2f}%<br>"
            "<extra></extra>"
        )
    )
    fig.add_trace(dot_plot, row=1, col=2)

    # x_max_profit = float(top_products["Profit"].max())
    profit_min = float(top_products["Profit"].min())
    profit_max = float(top_products["Profit"].max())

    # Always include zero so the bars can extend left/right correctly
    left = min(profit_min, 0.0)
    right = max(profit_max, 0.0)

    # Padding (handle the "all same value" case safely)
    span = right - left
    if span == 0:
        span = max(abs(left), abs(right), 1.0)

    pad = span * 0.15
    profit_range = [left - pad, right + pad]

    x_max_sales = float(top_products["Sales"].max())

    # dynamic height: base + per-row pixels
    rows = len(y_vals)
    base_height = 160  # header/title/margins
    per_row = 35  # adjust to taste
    fig_height = base_height + per_row * rows

    # if number_of_selected < 0:
    #
    # else:
    #     title = f'Performance of {top_n} Selected Products ({year_for_title}): Profit & Sales (left) + Profit Margin by Discount (right)'
    title = f"Top {top_n} Profitable Products ({year_for_title}): Profit & Sales (left) + Profit Margin by Discount (right)"
    fig.update_layout(
        height=fig_height,
        xaxis=dict(
            title="Total Profit ($)",
            color=PROFIT_COLOR,
            tickfont=dict(color=PROFIT_COLOR),
            showgrid=True, gridcolor="lightgrey", gridwidth=0.4,
            range=shared_range,
            domain=[0.0, 0.55]
        ),
        yaxis=dict(
            title="",
            type='category',
            categoryorder='array',
            categoryarray=y_vals,
            autorange="reversed",
        ),
        xaxis3=dict(
            title="Total Sales ($)",
            tickfont=dict(color=SALES_COLOR),
            color=SALES_COLOR,
            overlaying="x",
            side="top",
            anchor="y",
            showgrid=False,
            range=shared_range,
            matches=None,
            scaleanchor=None,
            constrain="range",
            # tickmode="array",
            # tickvals=[0, right * 0.25, right * 0.5, right * 0.75, right],
            # ticktext=[f"{v:,.0f}" for v in [0, right * 0.25, right * 0.5, right * 0.75, right]],
        ),
        xaxis2=dict(
            title="Discount",
            tickvals=full_x_vals,
            ticktext=full_tick_text,
            type='linear',
            showgrid=False,
            zeroline=False,
            range=[-0.1, max_discount + 0.15],
        ),
        yaxis2=dict(showticklabels=False, showgrid=False, ticks="", matches='y'),
        barmode="overlay",
        hovermode="closest",
        uniformtext=dict(mode="show", minsize=4),
        showlegend=False,
        plot_bgcolor="white",
        margin=dict(l=20, r=20, t=90, b=50),
        title_text=title,
        title={**TOP_LEFT_TITLE},
    )

    fig.update_xaxes(
        showspikes=True,
        spikemode="across",
        spikesnap="cursor",
        spikethickness=1,
        spikedash="solid",
        spikecolor="rgba(0,0,0,0.5)"
    )
    fig.update_yaxes(
        showspikes=True,
        spikemode="across",
        spikesnap="cursor",
        spikethickness=1,
        spikedash="solid",
        spikecolor="rgba(0,0,0,0.5)"
    )

    # Attach Sales to x3
    fig.data[1].update(xaxis="x3", yaxis="y")

    return fig
