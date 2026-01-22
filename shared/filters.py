def apply_filters(df, year, segments, regions):
    filtered = df[df["Year"] == year]

    if segments:
        filtered = filtered[filtered["Segment"].isin(segments)]

    if regions:
        filtered = filtered[filtered["Region"].isin(regions)]

    return filtered
