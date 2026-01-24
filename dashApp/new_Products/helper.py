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
