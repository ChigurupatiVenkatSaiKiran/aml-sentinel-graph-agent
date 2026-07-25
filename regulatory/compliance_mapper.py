"""
Regulatory Compliance Mapper
----------------------------
Maps detected AML topologies to standard regulatory definitions,
FATF Recommendations, and Bank Secrecy Act (BSA) codes.
"""

REGULATORY_MAP = {
    "structuring": {
        "title": "Structuring to Avoid Reporting Thresholds",
        "fatf": "FATF Recommendation 20 (Suspicious Transaction Reporting)",
        "bsa": "31 U.S.C. § 5324 & 31 C.F.R. § 1010.314 (Structuring prohibition)",
        "fincen": "FinCEN Advisory FIN-2014-A005 (Structuring Guidance)",
        "action_required": "File Suspicious Activity Report (SAR) within 30 days. Log for Currency Transaction Report (CTR) audit."
    },
    "layering": {
        "title": "Multi-Hop Layering / Transaction Laundering",
        "fatf": "FATF Recommendation 16 (Wire Transfers / Travel Rule)",
        "bsa": "31 C.F.R. § 1010.410 (Travel Rule Recordkeeping)",
        "fincen": "FinCEN Advisory FIN-2010-A012 (Wire Transfer Laundering)",
        "action_required": "Conduct Enhanced Due Diligence (EDD) on all accounts in chain. Suspend pass-through nodes."
    },
    "smurfing": {
        "title": "Mule Network Dispersion (Fan-Out / Fan-In)",
        "fatf": "FATF Recommendation 10 (Customer Due Diligence / Ultimate Beneficial Owner)",
        "bsa": "31 U.S.C. § 5313 (Reports of Currency Transactions)",
        "fincen": "FinCEN Guidance on Smurfing & Money Mule Networks (2020-032)",
        "action_required": "Identify ultimate beneficial owner (UBO). Flag all associated mule accounts for closure."
    },
    "rapid_cashout": {
        "title": "Rapid Cash-Out / Placement Liquidation",
        "fatf": "FATF Recommendation 15 (New Technologies / Virtual Asset Services)",
        "bsa": "31 C.F.R. Part 1020 (Rules for Banks)",
        "fincen": "FinCEN Alert on Instant Payment Exploits",
        "action_required": "Initiate temporary freeze on outgoing funds. Request source-of-funds verification."
    },
    "round_tripping": {
        "title": "Round-Tripping / Circular Transactions",
        "fatf": "FATF Recommendation 12 (Politically Exposed Persons / Corporate Vehicles)",
        "bsa": "31 U.S.C. § 5318(g) (Reporting of Suspicious Transactions)",
        "fincen": "FinCEN Advisory on Trade-Based Money Laundering",
        "action_required": "Investigate corporate relationships. Perform cross-border transaction audit."
    },
    "normal": {
        "title": "Standard Transaction Profile",
        "fatf": "N/A",
        "bsa": "N/A",
        "fincen": "N/A",
        "action_required": "No action required. Standard monitoring baseline."
    }
}

def get_regulation_details(typology: str) -> dict:
    """Returns regulatory details for a typology."""
    return REGULATORY_MAP.get(typology.lower(), REGULATORY_MAP["normal"])
