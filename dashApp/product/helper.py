from dashApp.product.colors import SALES_COLOR, PROFIT_COLOR
import plotly.graph_objects as go

def react_to_category_dropdown(df, year, selected_categories=None, selected_regions=None):
    year = int(year)

    # defaults: all
    if not selected_categories:
        selected_categories = sorted(df["Category"].dropna().unique())
    if not selected_regions:
        selected_regions = sorted(df["Region"].dropna().unique())

    dff = df[
        (df["Year"] == year) &
        (df["Category"].isin(selected_categories)) &
        (df["Region"].isin(selected_regions))
        ].copy()

    return dff


def _create_sales_trace(monthly, chart_type):
    """Helper to create Sales trace based on chart_type ('line' or 'bar')."""
    if chart_type == 'bar':
        return go.Bar(
            x=monthly["Month_Name"],
            y=monthly["Sales"],
            name="Total Sales",
            marker_color=SALES_COLOR,
            hovertemplate="Month: %{x}<br>Sales: $%{y:,.0f}<extra></extra>",
            width=0.3
        )
    elif chart_type == 'line':
        return go.Scatter(
            x=monthly["Month_Name"],
            y=monthly["Sales"],
            name="Total Sales",
            mode="lines+markers",
            line=dict(color=SALES_COLOR, width=2.5),
            hovertemplate="Month: %{x}<br>Sales: $%{y:,.0f}<extra></extra>",
        )
    else:
        # Default to bar if invalid type is passed
        return _create_sales_trace(monthly, 'bar')


def _create_profit_trace(monthly, chart_type):
    """Helper to create Profit trace based on chart_type ('line' or 'bar')."""
    if chart_type == 'bar':
        return go.Bar(
            x=monthly["Month_Name"],
            y=monthly["Profit"],
            name="Total Profit",
            marker_color=PROFIT_COLOR,
            hovertemplate="Month: %{x}<br>Profit: $%{y:,.0f}<extra></extra>",
            width=0.3
        )
    elif chart_type == 'line':
        return go.Scatter(
            x=monthly["Month_Name"],
            y=monthly["Profit"],
            name="Total Profit",
            mode="lines+markers",
            line=dict(color=PROFIT_COLOR, width=2.5),
            hovertemplate="Month: %{x}<br>Profit: $%{y:,.0f}<extra></extra>",
        )
    else:
        # Default to line if invalid type is passed
        return _create_profit_trace(monthly, 'line')
