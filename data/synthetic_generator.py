"""
Synthetic AML Dataset Generator
--------------------------------
Generates realistic banking transactions with planted, labeled AML patterns.
To create a realistic, non-trivial machine learning boundary and prevent
artificial separability, fraud accounts are linked to the legitimate transaction
graph (e.g. money mules spending cash at retail shops).
"""

import pandas as pd
import numpy as np
import random
import uuid
from datetime import datetime, timedelta

random.seed(42)
np.random.seed(42)

# Global pool to track fraud-associated accounts
FRAUD_ACCOUNTS = set()


def _acc() -> str:
    """Generate a random account ID."""
    return f"ACC{random.randint(10000, 99999)}"


def _ts(base: datetime, offset_hours: float) -> datetime:
    return base + timedelta(hours=offset_hours)


def _amount(lo, hi):
    return round(random.uniform(lo, hi), 2)


# ─── normal transactions ───────────────────────────────────────────────────────

def generate_normal(n: int = 10000, base_date: datetime = None) -> pd.DataFrame:
    """
    Generate realistic legitimate transactions including large ones
    (mortgages, tuition, business payments) and complex network structures.
    To prevent graph separability, 20% of normal transactions link to the
    known fraud accounts, creating realistic community risk overlaps.
    """
    if base_date is None:
        base_date = datetime(2024, 1, 1)

    categories = [
        ("payroll",   5000,  8000,  0.20),
        ("retail",    10,    500,   0.30),
        ("bills",     50,    600,   0.20),
        ("p2p",       20,    2000,  0.15),
        ("mortgage",  15000, 40000, 0.05),
        ("tuition",   8000,  25000, 0.05),
        ("business",  5000,  50000, 0.05),
    ]

    rows = []
    fraud_list = list(FRAUD_ACCOUNTS)
    
    # Helper to pick account, occasionally bridging to a fraud node
    def get_sender():
        if fraud_list and random.random() < 0.15:
            return random.choice(fraud_list)
        return _acc()

    def get_receiver():
        if fraud_list and random.random() < 0.15:
            return random.choice(fraud_list)
        return _acc()

    # ─── 1. Basic Single Transactions ──────────────────────────────────────────
    n_basic = int(n * 0.75)
    for _ in range(n_basic):
        cat, lo, hi, _ = random.choices(categories, weights=[c[3] for c in categories])[0]
        src = get_sender()
        dst = get_receiver()
        ts  = _ts(base_date, random.uniform(0, 720))
        amt = _amount(lo, hi)
        rows.append({
            "transaction_id":  str(uuid.uuid4())[:8],
            "timestamp":       ts,
            "sender_id":       src,
            "receiver_id":     dst,
            "amount":          amt,
            "category":        cat,
            "is_fraud":        0,
            "typology":        "normal",
        })

    # ─── 2. Legitimate Payroll Fan-Outs ────────────────────────────────────────
    n_payroll_runs = 20
    for _ in range(n_payroll_runs):
        corp_hub = get_sender()
        n_employees = random.randint(12, 18)
        t0 = _ts(base_date, random.uniform(50, 650))
        for idx in range(n_employees):
            rows.append({
                "transaction_id":  str(uuid.uuid4())[:8],
                "timestamp":       _ts(t0, idx * random.uniform(0.1, 0.5)),
                "sender_id":       corp_hub,
                "receiver_id":     get_receiver(),
                "amount":          _amount(3000, 7500),
                "category":        "payroll",
                "is_fraud":        0,
                "typology":        "normal",
            })

    # ─── 3. Legitimate Treasury Sweeps ─────────────────────────────────────────
    n_sweeps = 25
    for _ in range(n_sweeps):
        depth = random.randint(3, 5)
        nodes = [get_sender() if idx % 2 == 0 else get_receiver() for idx in range(depth + 1)]
        amount = _amount(10000, 90000)
        t0 = _ts(base_date, random.uniform(50, 650))
        for idx in range(depth):
            amount *= random.uniform(0.995, 1.0)
            rows.append({
                "transaction_id":  str(uuid.uuid4())[:8],
                "timestamp":       _ts(t0, idx * random.uniform(0.5, 2.0)),
                "sender_id":       nodes[idx],
                "receiver_id":     nodes[idx + 1],
                "amount":          round(amount, 2),
                "category":        "business",
                "is_fraud":        0,
                "typology":        "normal",
            })

    # ─── 4. Family Expense Cycles ───────────────────────────────────────────────
    n_cycles = 20
    for _ in range(n_cycles):
        cycle_len = random.randint(3, 4)
        cycle = [get_sender() if idx % 2 == 0 else get_receiver() for idx in range(cycle_len)]
        amount = _amount(2000, 8000)
        t0 = _ts(base_date, random.uniform(50, 650))
        for idx in range(cycle_len):
            rows.append({
                "transaction_id":  str(uuid.uuid4())[:8],
                "timestamp":       _ts(t0, idx * random.uniform(1.0, 5.0)),
                "sender_id":       cycle[idx],
                "receiver_id":     cycle[(idx + 1) % cycle_len],
                "amount":          amount,
                "category":        "p2p",
                "is_fraud":        0,
                "typology":        "normal",
            })

    # ─── 5. Hard Negatives: Legitimate Cash Structuring-Lookalikes ─────────────
    n_cash_lookalikes = 30
    for _ in range(n_cash_lookalikes):
        merchant = get_receiver()
        t0 = _ts(base_date, random.uniform(50, 600))
        n_deposits = random.randint(4, 7)
        for idx in range(n_deposits):
            rows.append({
                "transaction_id":  str(uuid.uuid4())[:8],
                "timestamp":       _ts(t0, idx * random.uniform(12, 36)),
                "sender_id":       get_sender(),
                "receiver_id":     merchant,
                "amount":          _amount(8100, 9900),
                "category":        "retail",
                "is_fraud":        0,
                "typology":        "normal",
            })

    # ─── 6. Hard Negatives: Legitimate Rapid Treasury Sweeps ────────────────────
    n_rapid_sweeps = 40
    for sweep_num in range(n_rapid_sweeps):
        hq_acc = get_sender()
        sub_acc = get_receiver()
        holding_acc = get_receiver()
        amount = _amount(12000, 95000)
        t0 = _ts(base_date, random.uniform(50, 650))
        gap = random.uniform(0.1, 1.9)
        
        rows.append({
            "transaction_id":  str(uuid.uuid4())[:8],
            "timestamp":       t0,
            "sender_id":       sub_acc,
            "receiver_id":     hq_acc,
            "amount":          amount,
            "category":        "business",
            "is_fraud":        0,
            "typology":        "normal",
        })
        rows.append({
            "transaction_id":  str(uuid.uuid4())[:8],
            "timestamp":       _ts(t0, gap),
            "sender_id":       hq_acc,
            "receiver_id":     holding_acc,
            "amount":          amount,
            "category":        "business",
            "is_fraud":        0,
            "typology":        "normal",
        })

    return pd.DataFrame(rows)


# ─── aml pattern generators ───────────────────────────────────────────────────

def generate_structuring(n_cases: int = 8, base_date: datetime = None) -> pd.DataFrame:
    """Structuring: repeated deposits just below $10,000 reporting threshold."""
    if base_date is None:
        base_date = datetime(2024, 1, 15)

    rows = []
    for _ in range(n_cases):
        src  = _acc()
        FRAUD_ACCOUNTS.add(src)
        n_tx = random.randint(8, 18)
        t0   = _ts(base_date, random.uniform(0, 400))

        for i in range(n_tx):
            dst = _acc()
            FRAUD_ACCOUNTS.add(dst)
            rows.append({
                "transaction_id": str(uuid.uuid4())[:8],
                "timestamp":      _ts(t0, i * random.uniform(0.5, 6)),
                "sender_id":      src,
                "receiver_id":    dst,
                "amount":         _amount(8200, 9800),
                "category":       "transfer",
                "is_fraud":       1,
                "typology":       "structuring",
            })
    return pd.DataFrame(rows)


def generate_smurfing(n_cases: int = 6, base_date: datetime = None) -> pd.DataFrame:
    """Smurfing / Fan-Out: one source pushes money to many mule accounts."""
    if base_date is None:
        base_date = datetime(2024, 1, 20)

    rows = []
    for _ in range(n_cases):
        src       = _acc()
        collector = _acc()
        FRAUD_ACCOUNTS.add(src)
        FRAUD_ACCOUNTS.add(collector)
        
        n_mules   = random.randint(5, 12)
        mules     = [_acc() for _ in range(n_mules)]
        for m in mules:
            FRAUD_ACCOUNTS.add(m)
            
        total_amt = _amount(50000, 200000)
        mule_amts = np.random.dirichlet(np.ones(n_mules)) * total_amt
        t0        = _ts(base_date, random.uniform(0, 300))

        # source → mules
        for j, (mule, amt) in enumerate(zip(mules, mule_amts)):
            rows.append({
                "transaction_id": str(uuid.uuid4())[:8],
                "timestamp":      _ts(t0, j * random.uniform(0.2, 2)),
                "sender_id":      src,
                "receiver_id":    mule,
                "amount":         round(amt, 2),
                "category":       "transfer",
                "is_fraud":       1,
                "typology":       "smurfing",
            })
        # mules → collector
        for j, (mule, amt) in enumerate(zip(mules, mule_amts)):
            rows.append({
                "transaction_id": str(uuid.uuid4())[:8],
                "timestamp":      _ts(t0, n_mules * 2 + j * random.uniform(0.5, 3)),
                "sender_id":      mule,
                "receiver_id":    collector,
                "amount":         round(amt * random.uniform(0.85, 0.98), 2),
                "category":       "transfer",
                "is_fraud":       1,
                "typology":       "smurfing",
            })
    return pd.DataFrame(rows)


def generate_layering(n_cases: int = 6, base_date: datetime = None) -> pd.DataFrame:
    """Layering: money moves through a chain of accounts A→B→C→D→E."""
    if base_date is None:
        base_date = datetime(2024, 2, 1)

    rows = []
    for _ in range(n_cases):
        depth  = random.randint(4, 7)
        chain  = [_acc() for _ in range(depth + 1)]
        for node in chain:
            FRAUD_ACCOUNTS.add(node)
            
        amount = _amount(20000, 150000)
        t0     = _ts(base_date, random.uniform(0, 400))

        for i in range(depth):
            amount *= random.uniform(0.92, 0.99)
            rows.append({
                "transaction_id": str(uuid.uuid4())[:8],
                "timestamp":      _ts(t0, i * random.uniform(1, 5)),
                "sender_id":      chain[i],
                "receiver_id":    chain[i + 1],
                "amount":         round(amount, 2),
                "category":       "transfer",
                "is_fraud":       1,
                "typology":       "layering",
            })
    return pd.DataFrame(rows)


def generate_rapid_cashout(n_cases: int = 10, base_date: datetime = None) -> pd.DataFrame:
    """Rapid Cash-Out: large deposit immediately followed by withdrawal."""
    if base_date is None:
        base_date = datetime(2024, 2, 10)

    rows = []
    for case_num in range(n_cases):
        acc    = _acc()
        src    = _acc()
        dst    = _acc()
        FRAUD_ACCOUNTS.add(acc)
        FRAUD_ACCOUNTS.add(src)
        FRAUD_ACCOUNTS.add(dst)
        
        amount = _amount(10000, 80000)
        t0     = _ts(base_date, random.uniform(0, 500))
        gap    = random.uniform(0.25, 1.5)
        case_id = "RC_%04d" % case_num

        # deposit leg
        rows.append({
            "transaction_id": str(uuid.uuid4())[:8],
            "timestamp":      t0,
            "sender_id":      src,
            "receiver_id":    acc,
            "amount":         amount,
            "category":       "transfer",
            "is_fraud":       1,
            "typology":       "rapid_cashout",
            "case_id":        case_id,
        })
        # withdrawal leg
        rows.append({
            "transaction_id": str(uuid.uuid4())[:8],
            "timestamp":      _ts(t0, gap),
            "sender_id":      acc,
            "receiver_id":    dst,
            "amount":         round(amount * random.uniform(0.90, 0.99), 2),
            "category":       "withdrawal",
            "is_fraud":       1,
            "typology":       "rapid_cashout",
            "case_id":        case_id,
        })
    return pd.DataFrame(rows)


def generate_round_tripping(n_cases: int = 5, base_date: datetime = None) -> pd.DataFrame:
    """Round-Tripping: money flows in a cycle A→B→C→A."""
    if base_date is None:
        base_date = datetime(2024, 2, 20)

    rows = []
    for _ in range(n_cases):
        cycle_len = random.randint(3, 5)
        cycle     = [_acc() for _ in range(cycle_len)]
        for node in cycle:
            FRAUD_ACCOUNTS.add(node)
            
        amount    = _amount(15000, 100000)
        t0        = _ts(base_date, random.uniform(0, 400))

        for i in range(cycle_len):
            amount *= random.uniform(0.95, 0.99)
            rows.append({
                "transaction_id": str(uuid.uuid4())[:8],
                "timestamp":      _ts(t0, i * random.uniform(2, 12)),
                "sender_id":      cycle[i],
                "receiver_id":    cycle[(i + 1) % cycle_len],
                "amount":         round(amount, 2),
                "category":       "transfer",
                "is_fraud":       1,
                "typology":       "round_tripping",
            })
    return pd.DataFrame(rows)


# ─── main generator ───────────────────────────────────────────────────────────

def build_dataset(save_path: str = "data/transactions.csv") -> pd.DataFrame:
    """Build full dataset and save to CSV."""
    print("Generating synthetic AML dataset...")
    
    # Reset fraud pool between runs
    FRAUD_ACCOUNTS.clear()

    # 1. Run fraud generators first to collect active fraud node IDs
    dfs_fraud = [
        generate_structuring(8),
        generate_smurfing(6),
        generate_layering(6),
        generate_rapid_cashout(10),
        generate_round_tripping(5),
    ]
    df_fraud = pd.concat(dfs_fraud, ignore_index=True)

    # 2. Run normal generator which now links to fraud nodes to create realistic bridges
    df_normal = generate_normal(10000)

    df = pd.concat([df_normal, df_fraud], ignore_index=True)

    # Fill case_id for non-rapid_cashout rows (each is its own case)
    if "case_id" not in df.columns:
        df["case_id"] = ""
    df["case_id"] = df["case_id"].fillna("").astype(str)
    mask = df["case_id"] == ""
    df.loc[mask, "case_id"] = ["TX_%06d" % i for i in range(mask.sum())]

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)

    import os
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    df.to_csv(save_path, index=False)

    fraud_count  = int(df["is_fraud"].sum())
    normal_count = len(df) - fraud_count
    print("  Total transactions : %d" % len(df))
    print("  Normal             : %d" % normal_count)
    print("  Fraudulent         : %d" % fraud_count)
    print("  Typologies         : %s" % str(df[df.is_fraud==1]["typology"].value_counts().to_dict()))
    print("  Saved to           : %s" % save_path)
    return df


if __name__ == "__main__":
    build_dataset()
