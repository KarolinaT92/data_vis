import numpy as np
import plotly.graph_objects as go
from dash import Input, Output, callback
from plotly.subplots import make_subplots
from ..helper.cached_data import PlotRenderer
from ..helper.standard_design import TOP_LEFT_TITLE
import pandas as pd

def truncate_name(name, max_len=30):
    return name if len(name) <= max_len else name[:max_len] + "…"


@callback(Output('product-3th-layer-p1', 'figure'),
          Input('year-dropdown', 'value'),
          Input("selected-indices-scatter-plot", "data"),
          Input('product-3th-layer-p1-slider', 'value'),
          Input('selected-category-store', 'data'),
          Input('dots-hover-details-switch', 'on')
          )
def update_first_layer(selected_year, selected_ids, top_n, selected_category_list, show_dot_values):
    return PlotRenderer.render_plot_top_profitable_products(selected_year, selected_ids,
                                                            build_bar_heatmap, top_n, selected_category_list,
                                                            show_dot_values)


def build_bar_heatmap(df, year_for_title, top_n=5, selected_category_list=None, show_dot_values=False):
    if selected_category_list and len(selected_category_list) > 0:
        df = df[df['Category'].isin(selected_category_list)]

    print("show_dot_values =", show_dot_values, type(show_dot_values))
    grouped = (
        df.groupby(["Product Name", "Category", "Sub-Category"], as_index=False)
        .agg({"Sales": "sum", "Profit": "sum"})
    )

    # Decide which products to show (top / bottom)
    if top_n >= 0:
        top_products = grouped.sort_values("Profit", ascending=False).head(top_n)
    else:
        abs_top_n = abs(top_n)
        top_products = grouped.sort_values("Profit", ascending=True).head(abs_top_n)

    top_products["Product Name Short"] = top_products["Product Name"].apply(
        truncate_name
    )

    # This is THE master order for both subplots
    profit_order_short = top_products["Product Name Short"].tolist()
    y_vals = profit_order_short

    # Filter raw df to only those products (for dot plot)
    df_top = df[df["Product Name"].isin(top_products["Product Name"].tolist())].copy()
    df_top["Discount"] = df_top["Discount"].round(2)

    name_map = top_products[['Product Name', 'Product Name Short']].set_index('Product Name')[
        'Product Name Short'].to_dict()
    df_top['Product Name Short'] = df_top['Product Name'].map(name_map)  # <--- ADDED

    summary_by_discount = (
        df_top
        .groupby(["Discount", "Product Name Short"], as_index=False)
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

    custom_blue_scale = [
        [0.0, "#99c9ff"],
        [0.5, "#4da6ff"],
        [1.0, "#0059b3"],
    ]
    blue_title = "#0059b3"
    orange = "orange"
    orange_dark = "#b34700"

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
            color=top_products["Profit"],
            opacity=0.8,
            colorscale=custom_blue_scale,
            showscale=False
        ),
        # width=0.8,
        text=top_products["Profit"].map("{:,.0f}".format),
        textposition="none",
        textfont=dict(size=13, color="#003366"),
        cliponaxis=False,
        customdata=top_products[["Category", "Sub-Category", "Sales"]],
        # hovertemplate=(
        #     "<b>%{y}</b><br>"
        #     "Profit: %{x:,.2f}<br>"
        #     "Category: %{customdata[0]}<br>"
        #     "Sub-Category: %{customdata[1]}<br>"
        #     "Sales: %{customdata[2]:,.2f}<extra></extra>"
        # ),
    )
    fig.add_trace(profit_trace, row=1, col=1)

    sales_trace = go.Bar(
        x=top_products["Sales"],
        y=top_products["Product Name Short"],
        orientation="h",
        name="Sales",
        marker=dict(color=orange),
        width=0.2,
        text=top_products["Sales"].map("{:,.0f}".format),
        textposition="outside",
        outsidetextfont=dict(size=10, color=orange_dark, family="Arial Black"),
        insidetextanchor="start",
        cliponaxis=False,
    )
    fig.add_trace(sales_trace, row=1, col=1)

    # ----- Right subplot: Dot Plot -----
    # 1. Determine the mode based on the switch
    if show_dot_values:
        dot_mode = "markers+text"
    else:
        dot_mode = "markers"  # <--- Toggles to hide the text
        # This prevents the issue of Plotly discarding the text array permanently.

    dot_plot = go.Scatter(
        x=summary_by_discount["Discount"],
        y=summary_by_discount["Product Name Short"],

        mode=dot_mode,
        marker=dict(
            size=25,
            color=summary_by_discount["Avg Profit Margin (%)"],
            colorscale="RdYlGn",
            colorbar=dict(title="Profit Margin (%)"),
            showscale=True,
        ),
        text=summary_by_discount["Avg Profit Margin (%)"].round(1).astype(str),
        textfont=dict(size=10, color="black"),
        textposition="middle center",
        # hovertemplate=(
        #     "Discount: %{x}<br>"
        #     "Product: %{y}<br>"
        #     "Avg Profit Margin: %{marker.color:.2f}%<extra></extra>"
        # )
    )
    fig.add_trace(dot_plot, row=1, col=2)

    x_max_profit = float(top_products["Profit"].max())
    x_max_sales = float(top_products["Sales"].max())

    # dynamic height: base + per-row pixels
    rows = len(y_vals)
    base_height = 160  # header/title/margins
    per_row = 35  # adjust to taste
    fig_height = base_height + per_row * rows

    fig.update_layout(
        height=fig_height,
        xaxis=dict(
            title="Total Profit ($)",
            color=blue_title,
            tickfont=dict(color=blue_title),
            showgrid=True, gridcolor="lightgrey", gridwidth=0.4,
            range=[0, x_max_profit * 1.35],
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
            tickfont=dict(color=orange),
            color=orange,
            overlaying="x",
            side="top",
            anchor="y",
            showgrid=False,
            range=[0, x_max_sales * 1.18],
            matches=None,
            scaleanchor=None,
            constrain="range"
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
        title_text=f"Top {top_n} Profitable Products ({year_for_title}): Profit & Sales (left) + Profit Margin by Discount (right)",
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
