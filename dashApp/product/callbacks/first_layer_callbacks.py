from dash import callback, Output, Input
from shared.read_data import get_dataframe_from_store, CAT_COLORS
import plotly.express as px


@callback(Output('bubble-chart', 'figure'),

          Input('filtered-year-data', 'data'))
def update_first_layer(stored_data_dict):
    CAT_ORDER = ["Furniture", "Office Supplies", "Technology"]

    selected_year = stored_data_dict.get('year')
    year_for_title = str(selected_year)
    data_json = stored_data_dict.get('data')
    dff = get_dataframe_from_store(data_json)

    grouped = (
        dff.groupby("Category", as_index=False)
        .agg({
            "Sales": "sum",
            "Profit": "sum",
            "Quantity": "sum"
        })
    )
    fig = px.scatter(
        grouped,
        x="Sales",
        y="Profit",
        size="Quantity",
        color="Category",
        hover_name="Category",
        text="Category",
        size_max=50,
        title=None,  # we'll set a styled title below
        labels={"Sales": "Total Sales", "Profit": "Total Profit", "Quantity": "Total Quantity"},
        category_orders={"Category": CAT_ORDER},
        color_discrete_map=CAT_COLORS
    )

    fig.update_traces(
        textposition="middle center",
        textfont=dict(size=12, color="black"),
        opacity=0.85
    )

    sales_ticks = sorted(grouped["Sales"].round(0).unique())
    profit_ticks = sorted(grouped["Profit"].round(0).unique())

    fig.update_layout(
        title=dict(
            text=f"Sales, Profit & Quantity Distribution by Category — {year_for_title}",
            x=0.5, xanchor="center",
            y=0.9, yanchor="top",  # Move title lower (from 0.97 to 0.9)
            font=dict(size=14),  # Slightly smaller font
            pad=dict(t=0, b=0, l=0, r=0)  # Remove all title padding
        ),
        showlegend=False,
        xaxis=dict(
            title="Sales ($)",
            showgrid=True,
            tickvals=sales_ticks,
            gridcolor="lightgrey",
            gridwidth=0.5,
            griddash="dot",
            title_font=dict(size=10),  # Smaller axis title font
            tickfont=dict(size=10)
        ),
        yaxis=dict(
            title="Profit($)",
            showgrid=True,
            tickvals=profit_ticks,
            gridcolor="lightgrey",
            gridwidth=0.5,
            griddash="dot",
            title_font=dict(size=10),  # Smaller axis title font
            tickfont=dict(size=10)
        ),
        plot_bgcolor="white",
        margin=dict(l=40, r=20, t=30, b=30)
    )

    # 2. Adjust Text/Marker Size
    fig.update_traces(
        textfont=dict(size=10, color="black"),  # Smaller text on bubbles
        # marker=dict(size=fig.data[0].marker.size / 1.2)  # Optional: slightly reduce bubble size overall
    )

    # Let axes auto-adjust margins if labels get tight
    fig.update_xaxes(automargin=True)
    fig.update_yaxes(automargin=True)
    return fig
