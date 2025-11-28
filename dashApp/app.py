import dash_mantine_components as dmc
from dash import html, dcc, callback, Output, Input, page_container, page_registry
from dashApp.initialize import app


def make_link(page, active_path):
    cls = "nav-link active" if active_path == page["path"] else "nav-link"
    return dcc.Link(page["name"], href=page["path"], className=cls)


app.layout = dmc.MantineProvider(
    defaultColorScheme="light",  # or "dark" if you prefer
    withCssVariables=True,  # optional, but nice for theming
    children=[
        html.Div(
            [
                dcc.Location(id="url"),
                html.Nav(id="nav", className="navbar"),
                html.Main(page_container, className="page"),
            ],
            className="app-shell"
        )
    ]
)


@callback(Output("nav", "children"),
          Input("url", "pathname"),
          prevent_initial_call=True, allow_duplicate=True
          )
def render_nav(pathname):
    pages = sorted(page_registry.values(), key=lambda p: p.get("order", 999))
    return [
        html.Div("Superstore", className="brand"),
        html.Div([make_link(p, pathname) for p in pages], className="nav-links")
    ]


if __name__ == "__main__":
    app.run(debug=True)  # use_reloader=False   important for debugging in pycharm
