# polars_stats.py
import polars as pl, os, glob

NULLS = ["", "NA", "null", "N/A"]

def load_data():
    dfs = []
    for file in glob.glob("data/2024_fb_ads_president_scored_anon.csv"):
        df = pl.read_excel(file)
        df = df.with_columns(pl.lit(file).alias("source_file"))
        dfs.append(df)
    return pl.concat(dfs)

def feature_engineer(df: pl.DataFrame) -> pl.DataFrame:
    if {"spend_lower", "spend_upper"}.issubset(df.columns):
        df = df.with_columns(((pl.col("spend_lower") + pl.col("spend_upper")) / 2).alias("spend_midpoint"))
    if "ad_text" in df.columns:
        df = df.with_columns(pl.col("ad_text").cast(pl.Utf8).str.lengths().alias("text_length"))
    if {"ad_creation_time", "ad_end_time"}.issubset(df.columns):
        df = df.with_columns(
            (pl.col("ad_end_time").str.to_datetime() - pl.col("ad_creation_time").str.to_datetime()).dt.days().alias("duration_days")
        )
    return df

def save_describe(df, name):
    df.describe().write_csv(f"outputs/{name}.csv")

def main():
    os.makedirs("outputs", exist_ok=True)
    df = load_data()
    df = feature_engineer(df)

    save_describe(df, "polars_overall")

    if "page_id" in df.columns:
        for pid in df.select("page_id").unique().to_series().to_list():
            g = df.filter(pl.col("page_id") == pid)
            save_describe(g, f"polars_pageid_{pid}")
    if {"page_id", "ad_id"}.issubset(df.columns):
        unique_combos = df.select(["page_id", "ad_id"]).unique()
        for row in unique_combos.iter_rows():
            g = df.filter((pl.col("page_id") == row[0]) & (pl.col("ad_id") == row[1]))
            save_describe(g, f"polars_pageid_adid_{row[0]}_{row[1]}")

if __name__ == "__main__":
    main()
