import numpy as np
import plotly.graph_objects as go
from dash import Input, Output, callback
from plotly.subplots import make_subplots
from ..helper.cached_data import PlotRenderer
from ..helper.standard_design import TOP_LEFT_TITLE


@callback(Output('product-3th-layer-p1', 'figure'),
          Input('year-dropdown', 'value'),
          Input("selected-indices-scatter-plot", "data"),
          Input('product-3th-layer-p1-slider', 'value'),
          Input('selected-category-store', 'data'),
          )
def update_first_layer(selected_year, selected_ids, top_n, selected_category_list):
    # top_n = range_values[1]
    return PlotRenderer.render_plot_top_profitable_products(selected_year, selected_ids, "bar-heatmap",
                                                            build_bar_heatmap, top_n, selected_category_list)


def build_bar_heatmap(df, year_for_title, top_n=10, selected_category_list=None):
    if selected_category_list and len(selected_category_list) > 0:
        df = df[df['Category'].isin(selected_category_list)]

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

    # This is THE master order for both subplots
    profit_order = top_products["Product Name"].tolist()
    y_vals = profit_order

    # Filter raw df to only those products (for dot plot)
    df_top = df[df["Product Name"].isin(profit_order)].copy()
    df_top["Discount"] = df_top["Discount"].round(2)

    summary_by_discount = (
        df_top
        .groupby(["Discount", "Product Name"], as_index=False)
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
        y=top_products["Product Name"],
        orientation="h",
        name="Profit",
        marker=dict(
            color=top_products["Profit"],
            opacity=0.8,
            colorscale=custom_blue_scale,
            showscale=False
        ),
        width=0.8,
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
        y=top_products["Product Name"],
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
    dot_plot = go.Scatter(
        x=summary_by_discount["Discount"],
        y=summary_by_discount["Product Name"],
        mode="markers+text",
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

    fig.update_layout(
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
        margin=dict(l=140, r=120, t=90, b=50),
        title_text=f"Top Products ({year_for_title}): Profit & Sales (left) + Profit Margin by Discount (right)",
        title={**TOP_LEFT_TITLE},

        height=450,  # helps in Dash so it doesn't look squeezed
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
