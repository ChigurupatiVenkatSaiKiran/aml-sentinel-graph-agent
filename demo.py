"""
AML Sentinel CLI Demo
----------------------
Standalone command-line demonstration.
Loads system, discovers real fraud account IDs from the dataset,
and runs the orchestrator against representative queries.
"""

from data.loader import get_train_test_splits
from detection.ml_models import MLModelManager
from agents.orchestrator import AMLOrchestrator


def main():
    print("=" * 64)
    print("             AML SENTINEL -- STANDALONE DEMO")
    print("=" * 64)

    # 1. Load splits (7-tuple)
    X_train, y_train, X_test, y_test, full_df, graph, n_train = get_train_test_splits()

    # 2. Train / load model
    ml_manager = MLModelManager()
    if not ml_manager.load_model():
        ml_manager.train(X_train, y_train)

    # 3. Orchestrator
    orchestrator = AMLOrchestrator(full_df, graph, ml_manager, n_train=n_train)

    # 4. Pick real fraud account IDs from the dataset for reliable demo queries
    fraud_rows = full_df[full_df["is_fraud"] == 1]
    demo_account = (
        fraud_rows["sender_id"].iloc[0] if not fraud_rows.empty else "ACC10822"
    )

    # PS1 Example Queries - each routes to a DIFFERENT set of tools
    # demonstrating the agent's dynamic, non-fixed pipeline behavior
    test_queries = [
        "Find structuring patterns in the last 30 days",               # -> rule_engine + graph_detector only, with date filter
        f"Is customer {demo_account} suspicious?",                     # -> entity_lookup + ml_model + graph + explainer only
        "Which customers made 10+ transactions under $10,000?",        # -> rule_engine + statistical only, skips ML
        "Analyze dataset for suspicious activity",                     # -> all 4 layers (broad sweep)
        "Show transaction network for key community",                  # -> graph_detector + visualizer only
    ]

    for i, query in enumerate(test_queries, 1):
        print(f"\n{'-'*64}")
        print(f"  DEMO QUERY {i}: {query}")
        print(f"{'-'*64}")

        plan    = orchestrator.parse_intent(query)
        print(f"  Intent    : {plan['intent'].upper()}")
        print(f"  Reasoning : {plan['reasoning'][:120]}...")

        results = orchestrator.execute_plan(plan)
        flagged = results["flagged_transactions"]

        print(f"  Flagged   : {len(flagged)} transactions")
        if not flagged.empty:
            cols = [c for c in ["transaction_id","sender_id","receiver_id","amount","typology","risk_score","risk_category"] if c in flagged.columns]
            print(flagged[cols].head(3).to_string(index=False))

        if results["selected_row"] is not None:
            print(f"\n  SAR NARRATIVE (excerpt):\n")
            print(results["sar_narrative"][:800])
            print("\n  COUNTERFACTUALS:")
            for cf in results["counterfactuals"]:
                print(f"    • {cf}")

    print(f"\n{'='*64}")
    print("  Demo complete. Launch the full dashboard: streamlit run app.py")
    print(f"{'='*64}\n")


if __name__ == "__main__":
    main()
