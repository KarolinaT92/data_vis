import dash_mantine_components as dmc
from dash import html, dcc, callback, Output, Input, page_container, page_registry
from dash import Dash

app = Dash(
    __name__,
    external_scripts=[{"src": "https://cdn.tailwindcss.com"}],
    use_pages=True,
    pages_folder="",
    suppress_callback_exceptions=True,
    title="Superstore Dashboard",
)

server = app.server

app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            html, body {
                height: 100%;
                margin: 0;
                padding: 0;
                overflow: hidden;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""

import dashApp.customer
import dashApp.shipment
import dashApp.template
import dashApp.product


def make_link(page, active_path):
    cls = "nav-link active" if active_path == page["path"] else "nav-link"
    return dcc.Link(page["name"], href=page["path"], className=cls)


app.layout = dmc.MantineProvider(
    defaultColorScheme="light",
    withCssVariables=True,
    children=[
        html.Div(
            [
                dcc.Location(id="url"),

                html.Nav(id="nav", className="navbar"),

                html.Main(
                    page_container,
                    className="flex-1 overflow-hidden",
                ),
            ],
            className="h-screen flex flex-col overflow-hidden",
        )
    ],
)


@callback(
    Output("nav", "children"),
    Input("url", "pathname"),
)
def render_nav(pathname):
    pages = sorted(page_registry.values(), key=lambda p: p.get("order", 999))

    return [
        html.Div(
            [
                html.Img(
                    src="/assets/icons8-store-48.png",
                    style={"height": "40px", "width": "40px", "marginRight": "8px"},
                ),
                html.Span("Superstore", style={"fontWeight": "600"}),
            ],
            className="brand",
            style={"display": "flex", "alignItems": "center"},
        ),
        html.Div(
            [make_link(p, pathname) for p in pages],
            className="nav-links",
        ),
    ]


if __name__ == "__main__":
    app.run(debug=True)
