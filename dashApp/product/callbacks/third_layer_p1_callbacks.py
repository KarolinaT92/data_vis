import numpy as np
import plotly.graph_objects as go
from dash import Input, Output, callback
from plotly.subplots import make_subplots
import plotly.express as px
from shared.read_data import get_dataframe_from_store
from ..helper.cached_data import figure_key, cache_figure_get, cache_figure_set


@callback(Output('product-3th-layer-p1', 'figure'),
          Input("filtered-year-data", "data")
          )
def third_layer_p1(stored_data_dict):
    if not stored_data_dict or 'data' not in stored_data_dict:
        return px.scatter(title="Waiting for bars and heatmap...")

    selected_year = stored_data_dict.get('year')
    year_for_title = str(selected_year)

    key = figure_key(year_for_title, "bar-heatmap")
    # 1) FAST PATH: try cache
    fig = cache_figure_get(key)
    if fig is not None:
        return fig  # instant

    data_json = stored_data_dict.get('data')
    dff = get_dataframe_from_store(data_json)
    # --- Build the figure if not cached ---
    fig = build_bar_heatmap(dff, year_for_title)
    cache_figure_set(key, fig)

    return fig


def build_bar_heatmap(df, year_for_title):
    grouped = (
        df.groupby(["Product Name", "Category", "Sub-Category"], as_index=False)
        .agg({"Sales": "sum", "Profit": "sum"})
    )
    top10 = grouped.sort_values("Profit", ascending=False).head(10)
    profit_order = top10["Product Name"].tolist()

    df_top10 = df[df["Product Name"].isin(profit_order)].copy()
    df_top10["Discount"] = df_top10["Discount"].round(2)

    summary_by_discount = (
        df_top10
        .groupby(["Discount", "Product Name"], as_index=False)
        .agg(
            **{
                "Avg Profit Margin (%)": ("Profit Margin (%)", "mean"),
                "Count": ("Profit", "size"),
                "Total Quantity": ("Quantity", "sum"),
            }
        )
    )

    # keep Y order
    y_vals = profit_order

    # Pivot for heatmap Z
    z_margin = (
        summary_by_discount
        .pivot_table(index="Product Name", columns="Discount",
                     values="Avg Profit Margin (%)", aggfunc="mean")
        .reindex(index=y_vals, fill_value=np.nan)
    )

    # Drop all-NaN discount columns (keeps only discounts present for top-10)
    z_margin_filtered = z_margin.dropna(axis=1, how='all')

    x_vals = z_margin_filtered.columns.tolist()
    tick_text = [f"{x * 100:.0f}%" for x in x_vals]

    # Heatmap text labels
    text_values = z_margin_filtered.round(2).astype(str).replace("nan", "")

    # ---------- Colors ----------
    custom_blue_scale = [
        [0.0, "#99c9ff"],
        [0.5, "#4da6ff"],
        [1.0, "#0059b3"],
    ]
    blue_title = "#0059b3"
    orange = "orange"
    orange_dark = "#b34700"

    # ---------- Build subplots with shared Y ----------
    fig = make_subplots(
        rows=1, cols=2,
        shared_yaxes=True,
        column_widths=[0.55, 0.45],
        horizontal_spacing=0.08,
        specs=[[{"type": "xy"}, {"type": "heatmap"}]],
        # subplot_titles=("Top 10 Most Profitable Products & Sales (2017)",
        #                 "Profit Margin (%) by Discount")
    )

    # ----- Left subplot: Profit bars (main axis) -----
    profit_trace = go.Bar(
        x=top10["Profit"],
        y=top10["Product Name"],
        orientation="h",
        name="Profit",
        marker=dict(color=top10["Profit"], opacity=0.8, colorscale=custom_blue_scale, showscale=False),
        width=0.8,
        text=top10["Profit"].map("{:,.0f}".format),
        textposition="none",
        textfont=dict(size=13, color="#003366"),
        cliponaxis=False,
        customdata=top10[["Category", "Sub-Category", "Sales"]],
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Profit: %{x:,.2f}<br>"
            "Category: %{customdata[0]}<br>"
            "Sub-Category: %{customdata[1]}<br>"
            "Sales: %{customdata[2]:,.2f}<extra></extra>"
        ),
    )
    fig.add_trace(profit_trace, row=1, col=1)

    # ----- Left subplot overlay: Sales mini-bars on a separate top x-axis -----
    sales_trace = go.Bar(
        x=top10["Sales"],
        y=top10["Product Name"],
        orientation="h",
        name="Sales",
        marker=dict(color=orange),
        width=0.2,
        text=top10["Sales"].map("{:,.0f}".format),
        textposition="outside",
        outsidetextfont=dict(size=10, color=orange_dark, family="Arial Black"),
        insidetextanchor="start",
        cliponaxis=False,
    )
    # We'll attach this to a custom x-axis (xaxis3) that overlays xaxis in the left subplot.
    fig.add_trace(sales_trace, row=1, col=1)

    # ----- Right subplot: Heatmap (shares Y with left) -----
    heatmap = go.Heatmap(
        z=z_margin_filtered.values,
        x=x_vals,
        y=y_vals,
        text=text_values.values,
        texttemplate="%{text}",
        textfont=dict(size=12, color="black"),
        colorscale="RdYlGn",
        reversescale=False,
        zmid=0,
        colorbar=dict(title="Profit Margin (%)"),
        hovertemplate="Discount: %{x}<br>Product: %{y}<br>Profit Margin: %{z:.2f}%<extra></extra>"
    )
    fig.add_trace(heatmap, row=1, col=2)

    # ---------- Axis ranges & layout ----------
    x_max_profit = float(top10["Profit"].max())
    x_max_sales = float(top10["Sales"].max())

    # Force the left subplot to use a specific domain so we can overlay a top x-axis (xaxis3) cleanly
    fig.update_layout(
        # Domains: left subplot ~ 0 to 0.55, right subplot ~ 0.55 to 1.0 (matching column_widths)
        xaxis=dict(  # Profit axis (bottom) in left subplot
            title="Total Profit ($)",
            color=blue_title,
            tickfont=dict(color=blue_title),
            showgrid=True, gridcolor="lightgrey", gridwidth=0.4,
            range=[0, x_max_profit * 1.35],
            domain=[0.0, 0.55]
        ),
        yaxis=dict(  # Shared Y controls the category order for both
            title="",
            type='category',
            categoryorder='array',
            categoryarray=y_vals,
            autorange="reversed",  # top product at top
        ),
        # Create an overlaid top x-axis for Sales (still in the left subplot's domain)
        xaxis3=dict(
            title="Total Sales ($)",
            tickfont=dict(color=orange),
            color=orange,
            overlaying="x",
            side="top",
            anchor="y",
            showgrid=False,
            range=[0, x_max_sales * 1.18],
            matches=None,  # ensure it's independent from Profit scale
            scaleanchor=None,
            constrain="range"
        ),
        # Right subplot x-axis (discounts)
        xaxis2=dict(
            title="Discount",
            tickvals=x_vals,
            ticktext=[f"{v * 100:.0f}%" for v in x_vals],
            type='category',
            showgrid=False,
            domain=[0.60, 1.0]  # small gap equals horizontal_spacing
        ),
        # Hide Y tick labels on the heatmap side (they're shared from the left)
        yaxis2=dict(showticklabels=False, showgrid=False),
        barmode="overlay",
        uniformtext=dict(mode="show", minsize=4),
        showlegend=False,
        plot_bgcolor="white",
        margin=dict(l=140, r=120, t=150, b=50),
        title_text=f"Top 10 Profit Products in {year_for_title}: Profit & Sales (left) + Profit Margin by Discount (right)"
    )

    # Make sure the second (sales) trace uses the top overlay axis
    fig.data[1].update(xaxis="x3", yaxis="y")

    return fig
