"""Harborlight incident analysis pipeline (stages 3-7).

Fetches incidents from the statustracker API, cleans them, and writes
every CSV, PNG, and statistic into ./output. All data is synthetic.

Run:  API_URL=http://localhost:8092 python3 pipeline.py
"""
import os
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # no display on the VM
import matplotlib.pyplot as plt
import pandas as pd
import requests
from scipy import stats

API_URL = os.environ.get("API_URL", "http://localhost:8092")
PAGE_SIZE = 1000
OUT = Path(__file__).resolve().parent / "output"


# ---------- stage 3: extract ----------
def fetch_all():
    rows, offset = [], 0
    while True:
        resp = requests.get(f"{API_URL}/incidents",
                            params={"limit": PAGE_SIZE, "offset": offset}, timeout=30)
        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break
        rows.extend(batch)
        offset += PAGE_SIZE
    return pd.DataFrame(rows)


# ---------- cleaning ----------
def clean(raw):
    df = raw.drop_duplicates(subset="id").copy()
    df["created_at"] = pd.to_datetime(df["created_at"], utc=True, format="ISO8601")
    df["resolved_at"] = pd.to_datetime(df["resolved_at"], utc=True, format="ISO8601")
    df = df[df["category"].notna()].copy()  # drop any rows without a category
    df["resolution_hours"] = (df["resolved_at"] - df["created_at"]).dt.total_seconds() / 3600
    df["week_start"] = df["created_at"].dt.tz_convert(None).dt.to_period("W-SUN").dt.start_time
    return df


# ---------- stage 4: data quality ----------
def write_quality(raw, df):
    closed = df["status"].eq("closed")
    first, last = df["created_at"].min(), df["created_at"].max()
    span_days = (last - first).total_seconds() / 86400
    rows = [
        ("rows_fetched", len(raw)),
        ("duplicate_ids_removed", len(raw) - raw["id"].nunique()),
        ("rows_without_category_dropped", int(raw["category"].isna().sum())),
        ("rows_analyzed", len(df)),
        ("null_title", int(df["title"].isna().sum())),
        ("null_status", int(df["status"].isna().sum())),
        ("null_created_at", int(df["created_at"].isna().sum())),
        ("null_category", int(df["category"].isna().sum())),
        ("closed_rows", int(closed.sum())),
        ("closed_rows_missing_resolved_at", int((closed & df["resolved_at"].isna()).sum())),
        ("open_or_in_progress_rows", int((~closed).sum())),
        ("negative_resolution_times", int((df["resolution_hours"] < 0).sum())),
        ("first_created_at", first.isoformat()),
        ("last_created_at", last.isoformat()),
        ("date_span_days", round(span_days, 2)),
        ("meets_10000_rows", len(df) >= 10000),
        ("meets_90_days", span_days >= 90),
    ]
    pd.DataFrame(rows, columns=["metric", "value"]).to_csv(OUT / "data_quality.csv", index=False)


# ---------- stage 5: aggregate ----------
def weekly_volume(df):
    weekly = df.groupby("week_start").size().rename("incidents").reset_index()
    first = df["created_at"].min().tz_convert(None).normalize()
    last = df["created_at"].max().tz_convert(None).normalize()
    week_end = weekly["week_start"] + pd.Timedelta(days=6)
    # first and last weeks are partial; flag them so the trend ignores them
    weekly["complete_week"] = (weekly["week_start"] >= first) & (week_end <= last)
    weekly.to_csv(OUT / "weekly_volume.csv", index=False)
    return weekly


def resolution_by_category(closed_df):
    res = (closed_df.groupby("category")["resolution_hours"]
           .agg(closed_incidents="count",
                median_hours="median",
                p90_hours=lambda s: s.quantile(0.9))
           .round(2).sort_values("median_hours", ascending=False).reset_index())
    res.to_csv(OUT / "resolution_by_category.csv", index=False)
    return res


def category_counts(df):
    counts = df["category"].value_counts().rename_axis("category").reset_index(name="incidents")
    counts["share_pct"] = (counts["incidents"] / counts["incidents"].sum() * 100).round(1)
    counts.insert(0, "rank", range(1, len(counts) + 1))
    counts.to_csv(OUT / "category_counts.csv", index=False)
    return counts


def hourly_volume(df, weekly):
    """Average weekday arrivals per hour (UTC), complete weeks only. Feeds the staffing math."""
    full_weeks = weekly.loc[weekly["complete_week"], "week_start"]
    sub = df[df["week_start"].isin(full_weeks) & (df["created_at"].dt.dayofweek < 5)]
    n_weekdays = 5 * len(full_weeks)
    hourly = (sub.groupby(sub["created_at"].dt.hour).size()
              .reindex(range(24), fill_value=0) / n_weekdays).round(2)
    out = hourly.rename_axis("hour_utc").reset_index(name="avg_incidents_per_weekday_hour")
    out.to_csv(OUT / "hourly_volume.csv", index=False)
    return out


# ---------- stage 7: statistical checks ----------
def statistical_checks(weekly, closed_df):
    full = weekly[weekly["complete_week"]].reset_index(drop=True)
    lr = stats.linregress(range(len(full)), full["incidents"])
    mean_week = full["incidents"].mean()

    net = closed_df.loc[closed_df["category"] == "Network", "resolution_hours"]
    prn = closed_df.loc[closed_df["category"] == "Printers and labels", "resolution_hours"]
    mw = stats.mannwhitneyu(net, prn, alternative="two-sided")

    rows = [
        ("trend", "weeks_used", len(full)),
        ("trend", "slope_incidents_per_week", round(lr.slope, 2)),
        ("trend", "slope_pct_of_mean_week", round(lr.slope / mean_week * 100, 2)),
        ("trend", "p_value", f"{lr.pvalue:.3g}"),
        ("trend", "r_squared", round(lr.rvalue ** 2, 3)),
        ("network_vs_printers", "network_median_hours", round(net.median(), 2)),
        ("network_vs_printers", "printers_median_hours", round(prn.median(), 2)),
        ("network_vs_printers", "mann_whitney_U", round(mw.statistic, 1)),
        ("network_vs_printers", "p_value", f"{mw.pvalue:.3g}"),
    ]
    pd.DataFrame(rows, columns=["check", "metric", "value"]).to_csv(OUT / "stats.csv", index=False)

    sentences = [
        f"Weekly incident volume rose by about {lr.slope:.0f} incidents per week "
        f"({lr.slope / mean_week * 100:.1f}% of the average week; p = {lr.pvalue:.3g}, "
        f"{len(full)} complete weeks), so the increase is very unlikely to be chance; "
        "it does not tell us why volume is rising or whether it will continue.",
        f"Network incidents take a median of {net.median():.1f} hours to close versus "
        f"{prn.median():.1f} hours for printers and labels (Mann-Whitney p = {mw.pvalue:.3g}); "
        "that gap is real, but it measures time open, not hours of agent work.",
    ]
    (OUT / "stats_summary.txt").write_text("\n\n".join(sentences) + "\n")
    return lr, full, sentences


# ---------- stage 6: charts ----------
def chart_volume(full, lr):
    fig, ax = plt.subplots(figsize=(9, 5))
    x = range(len(full))
    ax.plot(full["week_start"], full["incidents"], marker="o", label="Weekly incidents")
    ax.plot(full["week_start"], [lr.intercept + lr.slope * i for i in x],
            linestyle="--", label=f"Trend: {lr.slope:+.0f} incidents/week")
    ax.set_title("Weekly incident volume (complete weeks only)")
    ax.set_xlabel("Week starting (Monday, UTC)")
    ax.set_ylabel("Incidents per week (count)")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(OUT / "chart_volume_trend.png", dpi=150)
    plt.close(fig)


def chart_resolution(closed_df, res):
    order = list(res["category"])
    data = [closed_df.loc[closed_df["category"] == c, "resolution_hours"] for c in order]
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.boxplot(data, showfliers=False)
    ax.set_xticks(range(1, len(order) + 1), order, rotation=20, ha="right")
    ax.set_yscale("log")
    ax.set_title("Time to resolve by category (closed incidents)")
    ax.set_xlabel("Category (slowest median on the left)")
    ax.set_ylabel("Hours to resolve (log scale)")
    ax.grid(axis="y", alpha=0.3)
    fig.text(0.01, 0.01, "Box = middle 50%, line = median, whiskers = 1.5x IQR; outliers not drawn",
             fontsize=7)
    fig.tight_layout()
    fig.savefig(OUT / "chart_resolution_distribution.png", dpi=150)
    plt.close(fig)


def chart_categories(counts):
    c = counts.sort_values("incidents")
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.barh(c["category"], c["incidents"])
    ax.bar_label(bars, labels=[f"{n:,} ({s}%)" for n, s in zip(c["incidents"], c["share_pct"])],
                 padding=3)
    ax.set_title("Busiest incident categories (all incidents)")
    ax.set_xlabel("Incidents (count)")
    ax.set_ylabel("Category")
    ax.set_xlim(0, c["incidents"].max() * 1.2)
    fig.tight_layout()
    fig.savefig(OUT / "chart_busiest_categories.png", dpi=150)
    plt.close(fig)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    raw = fetch_all()
    print(f"fetched {len(raw)} rows from {API_URL}")
    df = clean(raw)
    write_quality(raw, df)

    closed_df = df[df["status"].eq("closed") & df["resolution_hours"].notna()]
    weekly = weekly_volume(df)
    res = resolution_by_category(closed_df)
    counts = category_counts(df)
    hourly_volume(df, weekly)

    lr, full, sentences = statistical_checks(weekly, closed_df)
    chart_volume(full, lr)
    chart_resolution(closed_df, res)
    chart_categories(counts)

    print(f"analyzed {len(df)} rows; outputs written to {OUT}")
    for s in sentences:
        print("-", s)


if __name__ == "__main__":
    main()
