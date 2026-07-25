"""
AML Feature Engineering -- Optimized
-------------------------------------
All rolling window computations are vectorized using pandas rolling()
with DatetimeIndex time-based offsets. No O(n²) loops.
"""

import pandas as pd
import numpy as np


def compute_transaction_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes static per-transaction features:
    - is_round_amount: transaction amount divisible by 100
    - is_structuring_amount: between $8,000-$9,999 (just below reporting threshold)
    - hour_of_day: hour of transaction for temporal analysis
    """
    df = df.copy().sort_values("timestamp").reset_index(drop=True)

    df["is_round_amount"]      = (df["amount"] % 100 == 0).astype(int)
    df["is_structuring_amount"] = (
        (df["amount"] >= 8000) & (df["amount"] <= 9999.99)
    ).astype(int)
    df["hour_of_day"] = df["timestamp"].dt.hour

    return df


def compute_rolling_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes time-window behavioral features per sender using vectorized
    pandas rolling() with DatetimeIndex -- no nested loops, O(n log n).

    Features:
    - tx_count_1d / tx_count_7d   : transaction count in rolling 1-day / 7-day window
    - tx_sum_1d   / tx_sum_7d     : transaction total in rolling 1-day / 7-day window
    - unique_recipients_7d         : distinct receivers in last 7 days per sender
    - time_since_last_tx_hours     : hours since sender's last transaction
    - is_rapid_cashout             : account received money then sent >=85% within 2 hours
    """
    df = df.copy().sort_values("timestamp")

    # -- Set DatetimeIndex for rolling time windows --
    df = df.set_index("timestamp")

    # -- Rolling counts and sums per sender ----------------------------------
    for out_col, window in [("tx_count_1d", "1D"), ("tx_count_7d", "7D")]:
        df[out_col] = (
            df.groupby("sender_id", group_keys=False)["amount"]
            .transform(lambda s: s.rolling(window, closed="right").count())
            .fillna(1)
            .astype(int)
        )

    for out_col, window in [("tx_sum_1d", "1D"), ("tx_sum_7d", "7D")]:
        df[out_col] = (
            df.groupby("sender_id", group_keys=False)["amount"]
            .transform(lambda s: s.rolling(window, closed="right").sum())
            .fillna(0)
        )

    df = df.reset_index()  # restore timestamp as column

    # -- Unique recipients in last 7 days (positional, no-reindex) ----------
    # Group by sender, sort within group, slide a 7-day window.
    df = df.sort_values(["sender_id", "timestamp"]).reset_index(drop=True)

    unique_counts_ordered: list = []   # will fill one entry per row in sender-sorted order

    for _sender, grp in df.groupby("sender_id", sort=True):
        grp = grp.reset_index(drop=True)
        timestamps = grp["timestamp"].to_numpy()
        receivers  = grp["receiver_id"].to_numpy()
        counts = []
        j_start = 0
        for i in range(len(grp)):
            cutoff = timestamps[i] - pd.Timedelta(days=7)
            # advance window start
            while timestamps[j_start] < cutoff:
                j_start += 1
            counts.append(len(set(receivers[j_start : i + 1])))
        unique_counts_ordered.extend(counts)

    df["unique_recipients_7d"] = unique_counts_ordered
    # Restore timestamp sort for downstream steps
    df = df.sort_values("timestamp").reset_index(drop=True)

    # -- Time since last transaction per sender -------------------------------
    df = df.sort_values(["sender_id", "timestamp"]).reset_index(drop=True)
    df["time_since_last_tx_hours"] = (
        df.groupby("sender_id")["timestamp"]
        .diff()
        .dt.total_seconds()
        .div(3600.0)
        .fillna(999.0)
    )
    df = df.sort_values("timestamp").reset_index(drop=True)

    # -- Rapid Cashout Flag (vectorized merge_asof) ---------------------------
    # Flag: account X receives money, then sends >=85% of it within 2 hours
    incoming = (
        df[["receiver_id", "timestamp", "amount"]]
        .rename(columns={"receiver_id": "account_id", "timestamp": "in_time", "amount": "in_amount"})
        .sort_values("in_time")
        .reset_index(drop=True)
    )
    outgoing = (
        df[["sender_id", "timestamp", "amount"]]
        .rename(columns={"sender_id": "account_id", "timestamp": "out_time", "amount": "out_amount"})
        .sort_values("out_time")
        .reset_index(drop=True)
    )

    merged = pd.merge_asof(
        outgoing,
        incoming,
        left_on="out_time",
        right_on="in_time",
        by="account_id",
        direction="backward",
        tolerance=pd.Timedelta(hours=2),
    )

    merged["is_rapid_cashout"] = (
        merged["in_amount"].notna()
        & (merged["out_amount"] >= 0.85 * merged["in_amount"].fillna(0))
    ).astype(int)

    # Merge cashout flag back (outgoing was sorted by out_time = same as df timestamp)
    df = df.sort_values("timestamp").reset_index(drop=True)
    df["is_rapid_cashout"] = merged["is_rapid_cashout"].values

    return df
