import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Output, Input
import dash_daq as daq

# ---------- Data ----------
data_path = "/Users/karolina/data_vis/superstore_dataset/cleaned_Superstore.csv"
df = pd.read_csv(data_path, parse_dates=['Order Date', 'Ship Date'])

df["ProfitMargin"] = np.where(df["Sales"] > 0, (df["Profit"] / df["Sales"]) * 100, np.nan)
df[["Sales", "Profit"]] = df[["Sales", "Profit"]].round(2)
df['Month'] = df['Order Date'].dt.month
df['Year'] = df['Order Date'].dt.year
df["Product_Key"] = df["Product ID"] + " | " + df["Product Name"]
df["Original Unit Price"] = df["Sales"] / ((1 - df["Discount"]) * df["Quantity"])
df['Month_Name'] = pd.to_datetime(df['Month'], format='%m').dt.strftime('%b')

app = Dash(__name__)

# ---------- Layout ----------
app.layout = html.Div(
    style={"padding": "16px", "backgroundColor": "white", "maxWidth": "1600px", "margin": "0 auto"},
    children=[
        html.H2("Customer Profit & Discount Dashboard", style={"marginBottom": "16px"}),

        # ===== Row 1: Top Customers (left) + Discount by Segment (right) =====
        html.Div(
            style={"display": "flex", "gap": "40px"},
            children=[
                # ---- Left: Top Customers ----
                html.Div(
                    style={"flex": "0 0 50%"},
                    children=[
                        html.H4("Top Most Profitable Customers", style={"marginBottom": "8px"}),
                        html.Div(
                            style={"display": "flex", "gap": "16px", "alignItems": "center", "flexWrap": "wrap"},
                            children=[
                                html.Div(children=[
                                    html.Label("view", style={"fontWeight": 600}),
                                    dcc.RadioItems(
                                        id="profit-view",
                                        options=[{"label": " Bar", "value": "bar"},
                                                 {"label": " Lollipop", "value": "lollipop"}],
                                        value="bar", inline=True),
                                ]),
                                html.Div(style={"flex": 1, "minWidth": "260px"}, children=[
                                    html.Label("Top customers", style={"fontWeight": 600}),
                                    dcc.Slider(
                                        id="topn-slider", min=5, max=50, step=1, value=10,
                                        marks={5: "5", 10: "10", 20: "20", 30: "30", 40: "40", 50: "50"},
                                        tooltip={"placement": "bottom"}, updatemode="mouseup"),
                                ]),
                            ]
                        ),
                        dcc.Graph(id="profit-graph", style={"height": "520px"})
                    ]
                ),

                # ---- Right: Discount by Segment ----
                html.Div(
                    style={"flex": "1"},
                    children=[
                        html.H4("Discount by Segment — Distribution View", style={"marginBottom": "8px"}),
                        html.Div(
                            style={"display": "flex", "gap": "16px", "alignItems": "flex-end", "flexWrap": "wrap"},
                            children=[
                                html.Div(children=[
                                    html.Label("view", style={"fontWeight": 600}),
                                    dcc.RadioItems(
                                        id="discount-view",
                                        options=[{"label": " Violin", "value": "violin"},
                                                 {"label": " Bubble", "value": "bubble"}],
                                        value="violin", inline=True),
                                ]),
                                html.Div(style={"minWidth": "280px"}, children=[
                                    html.Label("Bubble size (px)", style={"fontWeight": 600}),
                                    dcc.RangeSlider(
                                        id="bubble-size", min=8, max=80, step=1, value=[14, 50],
                                        marks={8: "8", 20: "20", 40: "40", 60: "60", 80: "80"},
                                        tooltip={"placement": "bottom"}, updatemode="mouseup"),
                                ]),
                                html.Div(children=[
                                    html.Label("Show labels when Count ≥", style={"fontWeight": 600}),
                                    dcc.Input(id="bubble-label-thresh", type="number", min=0, step=1, value=70,
                                              style={"width": "110px"}),
                                ]),
                            ]
                        ),
                        dcc.Graph(id="discount-graph", style={"height": "520px"})
                    ]
                ),
            ],
        ),

        # ===== Row 2: Time Series (left) + Category Overview (right) =====
        html.Div(
            style={"display": "flex", "gap": "40px", "marginTop": "36px"},
            children=[
                # ---- Left: Time Series ----
                html.Div(
                    style={"flex": "0 0 50%"},
                    children=[
                        html.H4("Sales and profit over time", style={"marginBottom": "8px"}),

                        html.Div(
                            style={"display": "flex", "gap": "16px", "alignItems": "center", "flexWrap": "wrap"},
                            children=[
                                html.Div(children=[
                                    html.Label("Metric", style={"fontWeight": 600}),
                                    dcc.Dropdown(
                                        id="ts-metric",
                                        options=[
                                            {"label": "Sales", "value": "Sales"},
                                            {"label": "Profit", "value": "Profit"},
                                            {"label": "Profit Margin (%)", "value": "ProfitMargin"},
                                        ],
                                        value="Sales", clearable=False, style={"width": "220px"}),
                                ]),
                                html.Div(children=[
                                    html.Label("Aggregation", style={"fontWeight": 600}),
                                    dcc.RadioItems(
                                        id="ts-agg",
                                        options=[{"label": " Month", "value": "M"},
                                                 {"label": " Quarter", "value": "Q"}],
                                        value="M", inline=True),
                                ]),
                            ]
                        ),
                        dcc.Graph(id="ts-graph", style={"height": "520px"}),
                    ]
                ),

                # ---- Right: Category Overview ----
                html.Div(
                    style={"flex": "1"},
                    children=[
                        html.H4("Sales and profit by categories", style={"marginBottom": "8px"}),

                        html.Div(
                            style={"display": "flex", "gap": "16px", "alignItems": "center", "flexWrap": "wrap"},
                            children=[
                                # View FIRST
                                html.Div(children=[
                                    html.Label("view", style={"fontWeight": 600}),
                                    dcc.RadioItems(
                                        id="cat-view",
                                        options=[{"label": " Bar", "value": "bar"},
                                                 {"label": " Treemap (Sub-Category)", "value": "treemap"}],
                                        value="bar", inline=True),
                                ]),
                                # Metric as "segmented switch" (styled RadioItems)
                                html.Div(children=[
                                    html.Label("Metric", style={"fontWeight": 600}),
                                    dcc.RadioItems(
                                        id="cat-metric",
                                        options=[{"label": " Sales", "value": "Sales"},
                                                 {"label": " Profit", "value": "Profit"}],
                                        value="Sales",
                                        inline=True,
                                        labelStyle={
                                            "display": "inline-block",
                                            "padding": "6px 12px",
                                            "border": "1px solid #ccc",
                                            "borderRadius": "18px",
                                            "marginRight": "8px",
                                            "cursor": "pointer"
                                        },
                                        inputStyle={"marginRight": "6px"}
                                    ),
                                ]),
                                html.Div(children=[
                                    dcc.Checklist(
                                        id="cat-options",
                                        options=[{"label": " Normalize to %", "value": "pct"}],
                                        value=[], inline=True),
                                ]),
                            ]
                        ),

                        dcc.Graph(id="cat-graph", style={"height": "520px"}),
                    ]
                ),
            ],
        ),
    ],
)

# ---------- Callbacks ----------

# 1) Top Customers (Bar / Lollipop)
@app.callback(
    Output("profit-graph", "figure"),
    Input("topn-slider", "value"),
    Input("profit-view", "value"),
)
def update_profit(top_n, view):
    totals = (
        df.groupby("Customer Name", as_index=False)["Profit"]
          .sum().rename(columns={"Profit": "TotalProfit"})
          .sort_values("TotalProfit", ascending=False)
          .head(int(top_n))
    )
    greens_scale = ["#9ED4A3", "#1F7A35"]

    if view == "bar":
        fig = px.bar(
            totals, x="Customer Name", y="TotalProfit",
            title=f"Top {int(top_n)} Most Profitable Customers",
            color="TotalProfit", color_continuous_scale=greens_scale
        )
        fig.update_traces(marker=dict(line=dict(color="black", width=1)), width=0.5)
        fig.update_layout(coloraxis_showscale=False)
    else:
        x_vals = totals["Customer Name"].tolist()
        y_vals = totals["TotalProfit"].tolist()
        fig = go.Figure()
        # stems
        xs, ys = [], []
        for x, y in zip(x_vals, y_vals):
            xs += [x, x, None]
            ys += [0, y, None]
        fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines",
                                 line=dict(color="lightgray", width=3),
                                 hoverinfo="skip", showlegend=False))
        # markers
        fig.add_trace(go.Scatter(
            x=x_vals, y=y_vals, mode="markers",
            marker=dict(size=12, color=y_vals, colorscale=greens_scale,
                        line=dict(color="black", width=1)),
            hovertemplate="<b>%{x}</b><br>Total Profit: %{y:,.2f}<extra></extra>",
            showlegend=False
        ))
        fig.update_layout(title=f"Top {int(top_n)} Most Profitable Customers")

    fig.update_layout(
        paper_bgcolor="white", plot_bgcolor="white",
        font=dict(size=14), bargap=0.4,
        margin=dict(l=40, r=20, t=40, b=80), showlegend=False
    )
    fig.update_xaxes(tickangle=45, showline=True, linecolor="black")
    fig.update_yaxes(title_text="Total Profit ($)",
                     showgrid=True, gridcolor="lightgray", griddash="dash",
                     showline=True, linecolor="black")
    return fig

# 2) Discount (Violin / Bubble)
@app.callback(
    Output("discount-graph", "figure"),
    Input("discount-view", "value"),
    Input("bubble-size", "value"),
    Input("bubble-label-thresh", "value"),
)
def update_discount(view_type, bubble_size_px, label_thresh):
    def apply_common(fig):
        fig.update_layout(paper_bgcolor="white", plot_bgcolor="white",
                          font=dict(size=14), margin=dict(l=40, r=20, t=40, b=60))
        fig.update_yaxes(
            tickmode="array",
            tickvals=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
            ticktext=["0", "10", "20", "30", "40", "50", "60", "70", "80"],
            title_text="Discount (%)",
            showgrid=True, gridcolor="lightgray", griddash="dash",
            showline=True, linecolor="black"
        )
        fig.update_xaxes(title_text="Segment", showline=True, linecolor="black")
        return fig

    if view_type == "violin":
        fig = px.violin(df, x="Segment", y="Discount",
                        box=True, points="all",
                        color_discrete_sequence=["#1f77b4"], title=None)
        return apply_common(fig)

    # Bubble view
    disc_step = 0.05
    discount_bin = np.round(df["Discount"] / disc_step) * disc_step
    dff = (df.assign(DiscountGroup=discount_bin)
             .groupby(["Segment", "DiscountGroup"], as_index=False)
             .size().rename(columns={"size": "Count"}))
    # jitter (±1%)
    rng = np.random.default_rng(42)
    dff["DiscountJitter"] = dff["DiscountGroup"] + rng.uniform(-0.01, 0.01, size=len(dff))

    # map Count -> bubble size via slider range
    min_px, max_px = bubble_size_px if isinstance(bubble_size_px, (list, tuple)) else (14, 50)
    cmin, cmax = dff["Count"].min(), dff["Count"].max()
    dff["BubbleSize"] = (min_px + max_px) / 2.0 if cmax == cmin else np.interp(dff["Count"], (cmin, cmax), (min_px, max_px))

    # labels threshold
    thresh = 0 if label_thresh is None else int(label_thresh)
    dff["Label"] = np.where(dff["Count"] >= thresh, dff["Count"].astype(str), "")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dff["Segment"], y=dff["DiscountJitter"], mode="markers+text",
        text=dff["Label"], textposition="middle center",
        marker=dict(size=dff["BubbleSize"], color="rgba(31,119,180,0.75)", line=dict(color="black", width=1)),
        hovertemplate="<b>%{x}</b><br>Discount (bin): %{y:.2f}<br>Count: %{customdata}<extra></extra>",
        customdata=dff["Count"]
    ))
    fig.update_layout(title="Discount Frequency by Segment (Bubble Size = Count)")
    return apply_common(fig)

# 3) Time Series 
@app.callback(
    Output("ts-graph", "figure"),
    Input("ts-metric", "value"),
    Input("ts-agg", "value"),
)
def update_time_series(metric, agg_rule):
    g = (df.set_index("Order Date")
             .resample(agg_rule)
             .agg({"Sales": "sum", "Profit": "sum"})
             .reset_index())
    g["ProfitMargin"] = np.where(g["Sales"] > 0, (g["Profit"] / g["Sales"]) * 100, np.nan)

    if metric == "ProfitMargin":
        y = "ProfitMargin"; y_title = "Profit Margin (%)"; fmt_hover = "%{y:.1f}%"
    elif metric == "Profit":
        y = "Profit"; y_title = "Profit ($)"; fmt_hover = "%{y:$,.2f}"
    else:
        y = "Sales"; y_title = "Sales ($)"; fmt_hover = "%{y:$,.2f}"

    fig = px.line(g, x="Order Date", y=y, markers=True, title=None,
                  color_discrete_sequence=["#1f77b4"])
    time_fmt = "%b %Y" if agg_rule == "M" else "Q%q %Y"
    fig.update_traces(hovertemplate=f"%{{x|{time_fmt}}}<br>{fmt_hover}<extra></extra>")
    fig.update_layout(template="plotly_white", margin=dict(l=40, r=20, t=30, b=40),
                      yaxis_title=y_title, xaxis_title="Order Date")
    fig.update_xaxes(showline=True, linecolor="black")
    fig.update_yaxes(showgrid=True, gridcolor="lightgray", griddash="dash",
                     showline=True, linecolor="black")
    return fig

# 4) Category Overview (Bar or Treemap; improved)
@app.callback(
    Output("cat-graph", "figure"),
    Input("cat-view", "value"),
    Input("cat-metric", "value"),
    Input("cat-options", "value"),
)
def update_category(view, metric, options):
    # Treemap: size by Sales, color by chosen metric (or margin if Sales)
    if view == "treemap":
        agg = (df.groupby(["Category", "Sub-Category"], as_index=False)
                 .agg({"Sales": "sum", "Profit": "sum"}))
        agg["ProfitMargin"] = np.where(agg["Sales"] > 0, (agg["Profit"] / agg["Sales"]) * 100, np.nan)

        if metric == "Profit":
            color_col = "Profit"; cscale = "RdBu"; c_mid = 0; c_title = "Profit ($)"
        else:  # metric == "Sales"
            color_col = "ProfitMargin"; cscale = "RdYlGn"; c_mid = None; c_title = "Profit Margin (%)"

        fig = px.treemap(
            agg, path=["Category", "Sub-Category"], values="Sales",
            color=color_col, color_continuous_scale=cscale,
            color_continuous_midpoint=c_mid, title=None
        )
        fig.update_traces(
            hovertemplate="<b>%{label}</b><br>Sales: %{value:$,.0f}"
                          "<br>Profit: %{customdata[0]:$,.0f}"
                          "<br>Profit Margin: %{customdata[1]:.1f}%<extra></extra>",
            customdata=np.stack([agg["Profit"], agg["ProfitMargin"]], axis=-1)
        )
        fig.update_layout(template="plotly_white", coloraxis_colorbar=dict(title=c_title),
                          margin=dict(l=20, r=20, t=30, b=20))
        return fig

    # Bar view (Category-level), optional normalization to %
    agg = (df.groupby("Category", as_index=False)[metric]
             .sum().sort_values(metric, ascending=False))

    if "pct" in (options or []):
        total = agg[metric].sum()
        agg["Share (%)"] = (agg[metric] / total) * 100
        ycol, ytitle = "Share (%)", "Share (%)"
        hover = "%{y:.1f}%"; color_col = "Share (%)"
    else:
        ycol, ytitle = metric, f"{metric} ($)"
        hover = "%{y:$,.2f}"; color_col = metric

    fig = px.bar(
        agg, x="Category", y=ycol,
        color=color_col, color_continuous_scale="Blues", title=None
    )
    fig.update_traces(marker_line=dict(color="black", width=1),
                      hovertemplate="<b>%{x}</b><br>"+hover+"<extra></extra>")
    fig.update_layout(
        template="plotly_white",
        margin=dict(l=40, r=20, t=30, b=60),
        yaxis_title=ytitle, xaxis_title="Category",
        coloraxis_showscale=False,
    )
    fig.update_xaxes(showline=True, linecolor="black")
    fig.update_yaxes(showgrid=True, gridcolor="lightgray", griddash="dash",
                     showline=True, linecolor="black")
    return fig

# ---------- Run ----------
if __name__ == "__main__":
    app.run(debug=True)
