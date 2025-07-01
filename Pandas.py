# pandas_stats.py
import pandas as pd, os, glob
from datetime import datetime

NULLS = ["", "NA", "null", "N/A"]

def load_data():
    dfs = []
    for file in glob.glob("data/2024_fb_ads_president_scored_anon.csv"):
        df = pd.read_excel(file, na_values=NULLS)
        df["source_file"] = file
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)

def feature_engineer(df):
    if {"spend_lower", "spend_upper"}.issubset(df.columns):
        df["spend_midpoint"] = (df["spend_lower"] + df["spend_upper"]) / 2
    if "ad_text" in df.columns:
        df["text_length"] = df["ad_text"].astype(str).str.len()
    if {"ad_creation_time", "ad_end_time"}.issubset(df.columns):
        df["duration_days"] = (pd.to_datetime(df["ad_end_time"]) - pd.to_datetime(df["ad_creation_time"])).dt.days
    return df

def describe_group(df, name):
    with open(f"outputs/{name}.txt", 'w', encoding='utf-8') as f:
        f.write(df.describe(include="all").to_string())

def main():
    os.makedirs("outputs", exist_ok=True)
    df = load_data()
    df = feature_engineer(df)

    describe_group(df, "pandas_overall")

    if "page_id" in df.columns:
        for pid, g in df.groupby("page_id"):
            describe_group(g, f"pandas_pageid_{pid}")
    if {"page_id", "ad_id"}.issubset(df.columns):
        for (pid, aid), g in df.groupby(["page_id", "ad_id"]):
            describe_group(g, f"pandas_pageid_adid_{pid}_{aid}")

if __name__ == "__main__":
    main()
