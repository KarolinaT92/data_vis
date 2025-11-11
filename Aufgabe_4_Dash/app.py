import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Output, Input

data_path = "..\\superstore_dataset\\cleaned_Superstore.csv"
df = pd.read_csv(data_path, parse_dates=['Order Date', 'Ship Date'])

df["ProfitMargin"] = np.where(df["Sales"] > 0, (df["Profit"] / df["Sales"]) * 100, np.nan)
df[["Sales", "Profit"]] = df[["Sales", "Profit"]].round(2)
df['Month'] = df['Order Date'].dt.month
df['Year'] = df['Order Date'].dt.year
df["Product_Key"] = df["Product ID"] + " | " + df["Product Name"]
# Original Unit Price
df["Original Unit Price"] = df["Sales"] / ((1 - df["Discount"]) * df["Quantity"])
df['Month_Name'] = pd.to_datetime(df['Month'], format='%m').dt.strftime('%b')

app = Dash(__name__)

app.layout = html.Div(
    style={
        "padding": "16px",
        "backgroundColor": "white",
        "maxWidth": "1600px",
        "margin": "0 auto"
    },
    children=[
        html.H2("Customer Profit & Discount Dashboard", style={"marginBottom": "16px"}),

        html.Div(
            style={"display": "flex", "gap": "40px"},
            children=[

                # ===== Left: Profit (60% width) =====
                html.Div(
                    style={"flex": "0 0 50%"},
                    children=[
                        html.H4("Top Most Profitable Customers", style={"marginBottom": "8px"}),

                        html.Div(
                            style={"display": "flex", "gap": "16px", "alignItems": "center", "flexWrap": "wrap"},
                            children=[
                                html.Div(
                                    children=[
                                        html.Label("view", style={"fontWeight": 600}),
                                        dcc.RadioItems(
                                            id="profit-view",
                                            options=[
                                                {"label": " Bar", "value": "bar"},
                                                {"label": " Lollipop", "value": "lollipop"},
                                            ],
                                            value="bar",
                                            inline=True
                                        ),
                                    ]
                                ),
                                html.Div(
                                    style={"flex": 1, "minWidth": "260px"},
                                    children=[
                                        html.Label("Top customers", style={"fontWeight": 600}),
                                        dcc.Slider(
                                            id="topn-slider",
                                            min=5, max=50, step=1, value=10,
                                            marks={5: "5", 10: "10", 20: "20", 30: "30", 40: "40", 50: "50"},
                                            tooltip={"placement": "bottom"},
                                            updatemode="mouseup",
                                        ),
                                    ]
                                ),
                            ]
                        ),

                        dcc.Graph(id="profit-graph", style={"height": "520px"})
                    ]
                ),

                # ===== Right: Discount (remaining width) =====
                html.Div(
                    style={"flex": "1"},
                    children=[
                        html.H4("Discount by Segment — Distribution View", style={"marginBottom": "8px"}),

                        html.Div(
                            style={"display": "flex", "gap": "16px", "alignItems": "flex-end", "flexWrap": "wrap"},
                            children=[
                                html.Div(
                                    children=[
                                        html.Label("view", style={"fontWeight": 600}),
                                        dcc.RadioItems(
                                            id="discount-view",
                                            options=[
                                                {"label": " Violin", "value": "violin"},
                                                {"label": " Bubble", "value": "bubble"},
                                            ],
                                            value="violin",
                                            inline=True
                                        ),
                                    ]
                                ),
                                html.Div(
                                    children=[
                                        html.Label("Bubble size (px)", style={"fontWeight": 600}),
                                        dcc.RangeSlider(
                                            id="bubble-size",
                                            min=8, max=80, step=1, value=[14, 50],
                                            marks={8: "8", 20: "20", 40: "40", 60: "60", 80: "80"},
                                            tooltip={"placement": "bottom"},
                                            updatemode="mouseup",
                                        ),
                                    ],
                                    style={"minWidth": "280px"}
                                ),
                                html.Div(
                                    children=[
                                        html.Label("Show labels when Count ≥", style={"fontWeight": 600}),
                                        dcc.Input(
                                            id="bubble-label-thresh",
                                            type="number",
                                            min=0, step=1, value=70,
                                            style={"width": "110px"}
                                        ),
                                    ]
                                ),
                            ]
                        ),

                        dcc.Graph(id="discount-graph", style={"height": "520px"})
                    ]
                ),
            ],
        ),
    ],
)


# ================= Left callback: Profit (Bar/Lollipop) =================
@app.callback(
    Output("profit-graph", "figure"),
    Input("topn-slider", "value"),
    Input("profit-view", "value"),
)
def update_profit(top_n, view):
    totals = (
        df.groupby("Customer Name", as_index=False)["Profit"]
        .sum()
        .rename(columns={"Profit": "TotalProfit"})
        .sort_values("TotalProfit", ascending=False)
        .head(int(top_n))
    )

    greens_scale = ["#9ED4A3", "#1F7A35"]

    if view == "bar":
        fig = px.bar(
            totals, x="Customer Name", y="TotalProfit",
            title=f"Top {int(top_n)} Most Profitable Customers",
            color="TotalProfit",
            color_continuous_scale=greens_scale
        )
        fig.update_traces(marker=dict(line=dict(color="black", width=1)), width=0.5)
        fig.update_layout(coloraxis_showscale=False)

    else:  # lollipop
        x_vals = totals["Customer Name"].tolist()
        y_vals = totals["TotalProfit"].tolist()

        # Build figure
        fig = go.Figure()

        # stems
        x_stems, y_stems = [], []
        for x, y in zip(x_vals, y_vals):
            x_stems += [x, x, None]
            y_stems += [0, y, None]

        fig.add_trace(go.Scatter(
            x=x_stems, y=y_stems,
            mode="lines",
            line=dict(color="lightgray", width=3),
            hoverinfo="skip",
            showlegend=False
        ))

        # markers (intensity by value)
        fig.add_trace(go.Scatter(
            x=x_vals, y=y_vals,
            mode="markers",
            marker=dict(
                size=12,
                color=y_vals,
                colorscale=greens_scale,
                line=dict(color="black", width=1)
            ),
            hovertemplate="<b>%{x}</b><br>Total Profit: %{y:,.2f}<extra></extra>",
            showlegend=False,
            name=""
        ))

        fig.update_layout(title=f"Top {int(top_n)} Most Profitable Customers")

    # shared styling
    fig.update_layout(
        paper_bgcolor="white", plot_bgcolor="white",
        font=dict(size=14),
        bargap=0.4,
        margin=dict(l=40, r=20, t=40, b=80),
        showlegend=False
    )
    fig.update_xaxes(tickangle=45, showline=True, linecolor="black")
    fig.update_yaxes(
        title_text="Total Profit ($)",
        showgrid=True, gridcolor="lightgray", griddash="dash",
        showline=True, linecolor="black"
    )
    return fig


# ============ Right callback: Discount (Violin/Bubble with size control) ============
@app.callback(
    Output("discount-graph", "figure"),
    Input("discount-view", "value"),
    Input("bubble-size", "value"),
    Input("bubble-label-thresh", "value"),
)
def update_discount(view_type, bubble_size_px, label_thresh):
    def apply_common(fig):
        fig.update_layout(
            paper_bgcolor="white", plot_bgcolor="white",
            font=dict(size=14),
            margin=dict(l=40, r=20, t=40, b=60),
        )
        fig.update_yaxes(
            tickmode="array",
            tickvals=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
            ticktext=["0", "10", "20", "30", "40", "50", "60", "70", "80"],
            title_text="Discount (%)",
            showgrid=True, gridcolor="lightgray", griddash="dash",
            showline=True, linecolor="black"
        )
        fig.update_xaxes(
            title_text="Segment",
            showline=True, linecolor="black"
        )
        return fig

    if view_type == "violin":
        fig = px.violin(
            df, x="Segment", y="Discount",
            box=True, points="all",
            color_discrete_sequence=["#1f77b4"],
            title=None
        )
        return apply_common(fig)

    # ---- Bubble view ----
    disc_step = 0.05
    discount_bin = np.round(df["Discount"] / disc_step) * disc_step
    dff = (
        df.assign(DiscountGroup=discount_bin)
        .groupby(["Segment", "DiscountGroup"], as_index=False)
        .size()
        .rename(columns={"size": "Count"})
    )

    # jitter (±1%) to reduce complete overlap on identical bins
    rng = np.random.default_rng(42)
    dff["DiscountJitter"] = dff["DiscountGroup"] + rng.uniform(-0.01, 0.01, size=len(dff))

    # map Count -> bubble size via slider range
    min_px, max_px = bubble_size_px if isinstance(bubble_size_px, (list, tuple)) else (14, 50)
    cmin, cmax = dff["Count"].min(), dff["Count"].max()
    if cmax == cmin:
        dff["BubbleSize"] = (min_px + max_px) / 2.0
    else:
        dff["BubbleSize"] = np.interp(dff["Count"], (cmin, cmax), (min_px, max_px))

    # labels threshold (default 70)
    thresh = 0 if label_thresh is None else int(label_thresh)
    dff["Label"] = np.where(dff["Count"] >= thresh, dff["Count"].astype(str), "")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dff["Segment"],
        y=dff["DiscountJitter"],
        mode="markers+text",
        text=dff["Label"],
        textposition="middle center",
        marker=dict(
            size=dff["BubbleSize"],
            color="rgba(31,119,180,0.75)",
            line=dict(color="black", width=1)
        ),
        hovertemplate="<b>%{x}</b><br>Discount (bin): %{y:.2f}<br>Count: %{customdata}<extra></extra>",
        customdata=dff["Count"]
    ))
    fig.update_layout(title="Discount Frequency by Segment (Bubble Size = Count)")
    return apply_common(fig)


if __name__ == "__main__":
    app.run(debug=True)
