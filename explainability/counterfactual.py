"""
Counterfactual Explanation Generator
------------------------------------
Suggests concrete modifications a customer's behavior would need to exhibit
to avoid being flagged, directly mapped to compliance threshold rules.
"""

def generate_counterfactuals(row) -> list[str]:
    """
    Computes suggestions to bring transaction features below rule thresholds.
    Returns:
        suggestions (list): list of recommendations
    """
    suggestions = []
    
    # 1. Structuring boundary
    amount = float(row.get("amount", 0.0))
    if 8000.0 <= amount <= 9999.99:
        suggestions.append(
            f"Keep individual deposit/transfer amounts strictly below the $8,000 threshold, "
            f"or submit standard CTR form documentation."
        )
        
    # 2. Transaction count boundary
    tx_count_1d = int(row.get("tx_count_1d", 0))
    if tx_count_1d >= 8:
        suggestions.append(
            f"Limit daily transaction frequency (currently {tx_count_1d} tx/day) to less than 8 tx/day."
        )
        
    # 3. Rapid cash-out boundary
    is_rapid_cashout = int(row.get("is_rapid_cashout", 0))
    if is_rapid_cashout == 1:
        suggestions.append(
            f"Extend hold period on newly deposited funds. Outgoing transfers must be spaced "
            f"at least 2 hours apart from corresponding incoming deposits."
        )
        
    # 4. Graph neighborhood risks
    comm_risk = float(row.get("community_risk_score", 0.0))
    if comm_risk > 0.3:
        suggestions.append(
            f"Reduce transaction links to highly connected hub nodes or accounts within community groups "
            f"exhibiting high historical fraud ratios (current community risk: {comm_risk:.1%})."
        )
        
    if not suggestions:
        suggestions.append("Transaction behavior is within normal baseline parameters. No changes required.")
        
    return suggestions
