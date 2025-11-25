from dash import Dash, html, dcc, callback, Output, Input, page_container, page_registry
import dash_mantine_components as dmc

app = Dash(
    __name__,
    use_pages=True,
    pages_folder="",
    suppress_callback_exceptions=True,
    title="Superstore Dashboard"
)

from dashApp import overview, product, customer, shipment

def make_link(page, active_path):
    cls = "nav-link active" if active_path == page["path"] else "nav-link"
    return dcc.Link(page["name"], href=page["path"], className=cls)

app.layout = dmc.MantineProvider(
    html.Div(
        [
            dcc.Location(id="url"),
            html.Nav(id="nav", className="navbar"),
            html.Main(page_container, className="page"),
        ],
        className="app-shell"
    )
)

@callback(Output("nav", "children"), Input("url", "pathname"))
def render_nav(pathname):
    # Order links by optional 'order' you’ll set on each page
    pages = sorted(page_registry.values(), key=lambda p: p.get("order", 999))
    return [
        html.Div("Superstore", className="brand"),
        html.Div([make_link(p, pathname) for p in pages], className="nav-links")
    ]

if __name__ == "__main__":
    app.run(debug=True) # use_reloader=False   important for debugging in pycharm

