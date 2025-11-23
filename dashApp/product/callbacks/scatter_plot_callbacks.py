import plotly.express as px
from dash import callback, Output, Input
from shared.read_data import df


@callback(Output('scatter-plot', 'figure'),
          Input('year-dropdown', 'value'))
def update_scatter_plot(selected_year):
    selected_df = df[df["Year"] == selected_year]

    # The Scatter plot definition is unchanged
    fig = px.scatter(
        selected_df,
        x="Profit",
        y="Sales",
        color="Category",
        hover_data=[
            "Product Name",
            "Sub-Category",
            "Quantity",
            "Discount",
            "Month_Name"
        ],
        labels={
            "Sales": "Sales ($)",
            "Profit": "Profit ($)",
            "Category": "Product Category"
        },
        title="Sales vs Profit by Product Category (2017)",
    )

    # Styling markers (unchanged)
    fig.update_traces(
        marker=dict(size=9, line=dict(width=1, color="white"), opacity=0.8)
    )

    # Layout and readability (unchanged)
    fig.update_layout(
        plot_bgcolor="white",
        legend=dict(
            title="Category",
            orientation="h",
            y=1.08,
            x=0.5,
            xanchor="center",
            font=dict(size=13)
        ),
        margin=dict(l=60, r=40, t=60, b=60),
    )

    # --- Gridlines, Axis Lines, and ZEROLINES (MODIFIED) ---

    # X-Axis (Vertical Line at x=0)
    fig.update_xaxes(
        title="Sales ($)",
        showgrid=False,
        gridcolor="rgba(0,0,0,0.12)",
        griddash="dash",
        zeroline=True,
        zerolinecolor='black',  # Choose a distinct color
        zerolinewidth=1,  # Make it thicker than the border line
    )

    # Y-Axis (Horizontal Line at y=0)
    fig.update_yaxes(
        title="Profit ($)",
        showgrid=True,
        gridcolor="rgba(0,0,0,0.12)",
        griddash="dash",
        zeroline=True,
        zerolinecolor='black',  # Choose a distinct color
        zerolinewidth=1,  # Make it thicker than the border line
    )
    return fig

