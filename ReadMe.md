# Task_03_Descriptive_Stats

This repository contains solutions to **Research Task 03**:  
**Descriptive Statistics with and without 3rd Party Libraries**, focused on analyzing 2024 US presidential election-related social media data.

---

## 📁 Repository Structure

| File                        | Description                                                   |
|-----------------------------|---------------------------------------------------------------|
| `python.py`     | Descriptive statistics using only base Python (no libraries)  |
| `pandas.py`          | Same analysis using the Pandas library                        |
| `polars.py`          | Same analysis using the Polars library                        |
| `data/`                    | Place the `2024_fb_ads_president_scored_anon.csv` file here   |
| `.gitignore`               | Prevents dataset and output files from being committed        |
| `README.md`                | Overview, setup, and execution instructions                   |

---

## 🧠 Objective

The goal is to produce identical descriptive summaries using three approaches:

- Pure Python (no libraries)
- Pandas
- Polars

Each script:

- Handles missing values (`NA`, `null`, blank)
- Performs optional feature engineering:
  - `spend_midpoint`
  - `text_length`
  - `duration_days`
- Computes statistics:
  - Count, Mean, Min, Max, Std for numeric fields
  - Unique values and Most Frequent for categorical fields
- Groups statistics by:
  - Entire dataset
  - `page_id`
  - `page_id`, `ad_id`

---

## 📦 Setup

### Prerequisites
Python 3.8 or higher

### Install dependencies
```bash
pip install pandas polars python-dateutil
