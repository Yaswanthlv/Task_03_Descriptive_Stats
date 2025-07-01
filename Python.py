# pure_python_stats.py
import csv, os, sys
from collections import defaultdict, Counter
from statistics import mean, stdev
from datetime import datetime

NULLS = {"", "NA", "null", "N/A"}

def safe_float(val):
    try: return float(val)
    except: return None

def load_data(path):
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        data = []
        for row in reader:
            cleaned = {k: (v if v not in NULLS else None) for k, v in row.items()}
            data.append(cleaned)
        return data

def feature_engineer(data):
    for row in data:
        if row.get("spend_lower") and row.get("spend_upper"):
            try:
                row["spend_midpoint"] = str((float(row["spend_lower"]) + float(row["spend_upper"])) / 2)
            except: pass
        if row.get("ad_text"):
            row["text_length"] = str(len(row["ad_text"]))
        if row.get("ad_creation_time") and row.get("ad_end_time"):
            try:
                fmt = "%Y-%m-%d %H:%M:%S"
                start = datetime.strptime(row["ad_creation_time"], fmt)
                end = datetime.strptime(row["ad_end_time"], fmt)
                row["duration_days"] = str((end - start).days)
            except: pass
    return data

def describe(data):
    desc = {}
    if not data: return desc
    cols = data[0].keys()
    for col in cols:
        values = [row[col] for row in data if row[col] not in [None]]
        if not values: continue
        try:
            nums = list(map(float, values))
            desc[col] = {
                "count": len(nums),
                "mean": round(mean(nums), 2),
                "min": min(nums),
                "max": max(nums),
                "std": round(stdev(nums), 2) if len(nums) > 1 else 0
            }
        except:
            freq = Counter(values)
            top = freq.most_common(1)[0]
            desc[col] = {
                "count": len(values),
                "unique": len(set(values)),
                "top": top[0],
                "top_freq": top[1]
            }
    return desc

def groupby(data, keys):
    groups = defaultdict(list)
    for row in data:
        k = tuple(row[k] for k in keys if k in row)
        groups[k].append(row)
    return groups

def save_stats(desc, file):
    with open(file, 'w', encoding='utf-8') as f:
        for col, stats in desc.items():
            f.write(f"{col}:\n")
            for k, v in stats.items():
                f.write(f"  {k}: {v}\n")
            f.write("\n")

def main():
    os.makedirs("outputs", exist_ok=True)
    path = sys.argv[1] if len(sys.argv) > 1 else "data/2024_fb_ads_president_scored_anon.csv"
    data = load_data(path)
    data = feature_engineer(data)

    save_stats(describe(data), "outputs/pure_python_overall.txt")

    for k, v in groupby(data, ["page_id"]).items():
        save_stats(describe(v), f"outputs/pure_python_pageid_{k}.txt")
    for k, v in groupby(data, ["page_id", "ad_id"]).items():
        save_stats(describe(v), f"outputs/pure_python_pageid_adid_{'_'.join(k)}.txt")

if __name__ == "__main__":
    main()
