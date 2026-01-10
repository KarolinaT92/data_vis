from dash import html, dcc
from shared.read_data import df

YEARS = sorted(df["Year"].dropna().unique())
SEGMENTS = sorted(df["Segment"].dropna().unique())
REGIONS = sorted(df["Region"].dropna().unique())
DEFAULT_YEAR = max(YEARS)

filter_layout = html.Div(
    [
        html.H3("Filters", style={"marginBottom": "16px"}),

        html.Div(
            [
                html.Label("Year", style={"fontWeight": 600}),
                dcc.RadioItems(
                    id="customer-year-dropdown",
                    options=[{"label": str(y), "value": int(y)} for y in YEARS],
                    value=int(DEFAULT_YEAR),
                    labelStyle={
                "display": "block",
                "marginBottom": "6px",
                    },
                ),
            ],
            style={"marginBottom": "16px"},
        ),

        html.Div(
            [
                html.Label("Segment", style={"fontWeight": 600}),
                dcc.Dropdown(
                    id="customer-segment-dropdown",
                    options=[{"label": s, "value": s} for s in SEGMENTS],
                    value=SEGMENTS,
                    multi=True,
                    clearable=False,
                ),
            ],
            style={"marginBottom": "16px"},
        ),

        html.Div(
            [
                html.Label("Region", style={"fontWeight": 600}),
                dcc.Dropdown(
                    id="customer-region-dropdown",
                    options=[{"label": r, "value": r} for r in REGIONS],
                    value=REGIONS,
                    multi=True,
                    clearable=False,
                ),
            ],
        ),
    ],
    style={
        "width": "260px",
        "padding": "20px",
        "background": "#f7f7f7",
        "borderRight": "1px solid #ddd",


        "position": "sticky",
        "top": "0",


        "alignSelf": "flex-start",
        "height": "fit-content",
    },
)
