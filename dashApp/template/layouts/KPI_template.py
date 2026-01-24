from dash import html


def build_kpi(
        *,
        title: str,
        kpi_id: str,
        img_source: str | None = None,
):
    return html.Div(
        [
            html.Div(
                [
                    html.Img(
                        src=img_source,
                        className="w-10 h-10 mr-3",
                    )
                    if img_source
                    else None,
                    html.Div(
                        [
                            html.Span(title),
                        ]
                    ),
                ],
                className="flex items-center justify-center kpi-header",
            ),
            html.H3(
                id=kpi_id,
                className="font-bold m-2 text-center text-xl",
            ),
        ],
        className="flex flex-col items-center justify-center",
    )
