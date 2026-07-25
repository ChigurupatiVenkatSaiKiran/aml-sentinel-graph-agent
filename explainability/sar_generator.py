"""
Suspicious Activity Report (SAR) Generator
-------------------------------------------
Generates well-structured regulatory narrative text mapped to real
FATF Recommendations and BSA statutory codes.
Handles both pandas Timestamp and raw string timestamps safely.
"""

from datetime import datetime
import pandas as pd
from regulatory.compliance_mapper import get_regulation_details


def _fmt_ts(ts) -> str:
    """Safely formats any timestamp value to a display string."""
    if isinstance(ts, pd.Timestamp):
        return ts.strftime("%Y-%m-%d %H:%M:%S")
    if isinstance(ts, datetime):
        return ts.strftime("%Y-%m-%d %H:%M:%S")
    try:
        return pd.to_datetime(ts).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return str(ts)


def generate_sar_narrative(
    row,
    final_score: float,
    risk_cat: str,
    counterfactuals: list,
) -> str:
    """
    Generates a professional SAR filing draft with all required regulatory sections.
    """
    sender   = row.get("sender_id",       "UNKNOWN")
    receiver = row.get("receiver_id",     "UNKNOWN")
    amount   = float(row.get("amount",    0.0))
    ts       = _fmt_ts(row.get("timestamp", datetime.now()))
    typology = str(row.get("typology",    "UNKNOWN"))
    tx_id    = row.get("transaction_id",  "UNKNOWN")
    category = row.get("category",        "transfer")
    motif    = row.get("motif_typology",  "none")

    reg = get_regulation_details(typology)

    narrative = f"""\
================================================================================
                    SUSPICIOUS ACTIVITY REPORT (SAR)
                       CONFIDENTIAL COMPLIANCE FILING
================================================================================
REPORT ID     : SAR-{tx_id}
DATE OF FILING: {datetime.now().strftime("%Y-%m-%d")}
ORGANIZATION  : AML SENTINEL COMPLIANCE LABS
FILING TYPE   : SUSPICIOUS ACTIVITY REPORT (SAR)

--------------------------------------------------------------------------------
 1. SUBJECT DETAILS
--------------------------------------------------------------------------------
  Primary Account (Suspect) : {sender}
  Counterparty Account      : {receiver}
  Composite Risk Score      : {final_score:.1f} / 100.0
  Risk Category             : {risk_cat}

--------------------------------------------------------------------------------
 2. TRANSACTION SUMMARY
--------------------------------------------------------------------------------
  Transaction Reference ID  : {tx_id}
  Transaction Amount        : ${amount:,.2f}
  Timestamp                 : {ts}
  Category                  : {category}

--------------------------------------------------------------------------------
 3. DETECTED COMPLIANCE TYPOLOGY & REGULATORY CODES
--------------------------------------------------------------------------------
  Pattern Detected          : {reg['title']}
  FATF Reference            : {reg['fatf']}
  BSA Statutory Clause      : {reg['bsa']}
  FinCEN Advisory           : {reg['fincen']}

--------------------------------------------------------------------------------
 4. DETAILED COMPLIANCE NARRATIVE
--------------------------------------------------------------------------------
  On {ts}, account {sender} conducted a {category} to account
  {receiver} totaling ${amount:,.2f}.

  AML Sentinel's multi-layer detection system flagged this transaction
  under the pattern: "{reg['title']}".

  Key Risk Indicators Observed:
    · PageRank Centrality     : {row.get('pagerank_score', 0.0):.6f}
    · Community Risk Factor   : {row.get('community_risk_score', 0.0):.1%}
    · Structural Motif        : {motif}
    · Transactions (1-day)    : {row.get('tx_count_1d', 0)} tx
    · Structuring Amount Flag : {'Yes' if row.get('is_structuring_amount', 0) == 1 else 'No'}
    · Rapid Cash-Out Flag     : {'Yes' if row.get('is_rapid_cashout',       0) == 1 else 'No'}
    · Cycle/Ring Edge         : {'Yes' if row.get('is_cycle_edge',          0) == 1 else 'No'}

--------------------------------------------------------------------------------
 5. CORRECTIVE GUIDANCE (COUNTERFACTUAL ANALYSIS)
--------------------------------------------------------------------------------
  To align with standard retail banking behavioral norms, the subject
  account would be required to exhibit the following changes:

"""
    for cf in counterfactuals:
        narrative += f"    • {cf}\n"

    narrative += f"""
--------------------------------------------------------------------------------
 6. RECOMMENDATION & CORRECTIVE ACTION
--------------------------------------------------------------------------------
  Action Required           : {reg['action_required']}
  Filing Agent              : AML SENTINEL -- AUTOMATED COMPLIANCE OFFICER
  Classification            : CONFIDENTIAL -- FOR AUTHORIZED PERSONNEL ONLY
================================================================================
"""
    return narrative
