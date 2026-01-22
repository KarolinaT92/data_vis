from dash import html, dcc
from shared.read_data import df


def build_filter_layout(id_prefix="customer"):
    YEARS = sorted(df["Year"].dropna().unique())
    SEGMENTS = sorted(df["Segment"].dropna().unique())
    REGIONS = sorted(df["Region"].dropna().unique())

    return html.Div(
        [
            # ---- Year ----
            html.Div(
                [
                    html.Label("Year", className="filter-label"),
                    dcc.RadioItems(
                        id=f"{id_prefix}-year",
                        options=[
                            {
                                "label": html.Span(
                                    str(y),
                                    className="year-pill",
                                ),
                                "value": int(y),
                            }
                            for y in YEARS
                        ],
                        value=max(YEARS),
                        className="year-pill-group",
                        inline=True,
                    ),
                ],
            ),

            # ---- Segment ----
            html.Div(
                [
                    html.Label("Segment", className="filter-label"),
                    dcc.Dropdown(
                        id=f"{id_prefix}-segment",
                        options=[{"label": s, "value": s} for s in SEGMENTS],
                        value=SEGMENTS,
                        multi=True,
                        clearable=False,
                        maxHeight=220,
                    ),
                ],
            ),

            # ---- Region ----
            html.Div(
                [
                    html.Label("Region", className="filter-label"),
                    dcc.Dropdown(
                        id=f"{id_prefix}-region",
                        options=[{"label": r, "value": r} for r in REGIONS],
                        value=REGIONS,
                        multi=True,
                        clearable=False,
                        maxHeight=220,
                    ),
                ],
                style={"marginTop": "12px"},
            ),
        ],
        className="flex flex-col gap-6 w-full",
    )
