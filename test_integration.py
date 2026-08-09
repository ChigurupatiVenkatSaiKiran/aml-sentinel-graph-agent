"""
AML Sentinel - Full Integration Test Suite
Validates every module, data pipeline, detection engine, orchestrator, and output.
"""
import sys, os
import pandas as pd
os.chdir(r'c:\Users\chigu\OneDrive\Desktop\hackathon\aml-sentinel')

passed = 0
failed = 0

def check(name, expr, detail=''):
    global passed, failed
    if expr:
        print(f'  [PASS] {name}')
        passed += 1
    else:
        print(f'  [FAIL] {name} -- {detail}')
        failed += 1

print('='*60)
print('     AML SENTINEL -- FULL INTEGRATION TEST')
print('='*60)

# 1. Imports
print('\n--- MODULE IMPORTS ---')
try:
    from data.synthetic_generator import build_dataset
    check('data.synthetic_generator', True)
except Exception as e:
    check('data.synthetic_generator', False, str(e))

try:
    from data.feature_engineering import compute_transaction_features, compute_rolling_features
    check('data.feature_engineering', True)
except Exception as e:
    check('data.feature_engineering', False, str(e))

try:
    from data.loader import get_train_test_splits, FEATURE_COLS
    check('data.loader', True)
except Exception as e:
    check('data.loader', False, str(e))

try:
    from graph.network_builder import TransactionGraph
    check('graph.network_builder', True)
except Exception as e:
    check('graph.network_builder', False, str(e))

try:
    from graph.motif_detector import MotifDetector
    check('graph.motif_detector', True)
except Exception as e:
    check('graph.motif_detector', False, str(e))

try:
    from graph.visualizer import generate_interactive_graph
    check('graph.visualizer', True)
except Exception as e:
    check('graph.visualizer', False, str(e))

try:
    from detection.rule_engine import ComplianceRuleEngine
    check('detection.rule_engine', True)
except Exception as e:
    check('detection.rule_engine', False, str(e))

try:
    from detection.statistical import StatisticalAnomalyDetector
    check('detection.statistical', True)
except Exception as e:
    check('detection.statistical', False, str(e))

try:
    from detection.ml_models import MLModelManager
    check('detection.ml_models', True)
except Exception as e:
    check('detection.ml_models', False, str(e))

try:
    from detection.ensemble_scorer import EnsembleScorer
    check('detection.ensemble_scorer', True)
except Exception as e:
    check('detection.ensemble_scorer', False, str(e))

try:
    from explainability.counterfactual import generate_counterfactuals
    check('explainability.counterfactual', True)
except Exception as e:
    check('explainability.counterfactual', False, str(e))

try:
    from explainability.sar_generator import generate_sar_narrative
    check('explainability.sar_generator', True)
except Exception as e:
    check('explainability.sar_generator', False, str(e))

try:
    from regulatory.compliance_mapper import get_regulation_details
    check('regulatory.compliance_mapper', True)
except Exception as e:
    check('regulatory.compliance_mapper', False, str(e))

try:
    from agents.orchestrator import AMLOrchestrator
    check('agents.orchestrator', True)
except Exception as e:
    check('agents.orchestrator', False, str(e))

# 2. Data Pipeline
print('\n--- DATA PIPELINE ---')
X_train, y_train, X_test, y_test, df, graph, n_train = get_train_test_splits()
check('Dataset loaded', len(df) > 0, 'len=%d' % len(df))
check('Feature cols count', len(FEATURE_COLS) == 20, '%d cols' % len(FEATURE_COLS))
check('X_train shape', X_train.shape[1] == 20, 'shape=%s' % str(X_train.shape))
check('X_test shape', X_test.shape[1] == 20, 'shape=%s' % str(X_test.shape))
check('Train-test split aligned', n_train == len(X_train))
check('No NaN in X_train', X_train.isna().sum().sum() == 0, '%d NaNs' % X_train.isna().sum().sum())
check('No NaN in X_test', X_test.isna().sum().sum() == 0, '%d NaNs' % X_test.isna().sum().sum())
check('Fraud in train', int(y_train.sum()) > 0, 'fraud=%d' % int(y_train.sum()))
check('Fraud in test', int(y_test.sum()) > 0, 'fraud=%d' % int(y_test.sum()))
check('Graph has nodes', graph.G.number_of_nodes() > 0)
check('Graph has edges', graph.G.number_of_edges() > 0)

# 3. Detection Engines
print('\n--- DETECTION ENGINES ---')
ml = MLModelManager()
ml.load_model()
check('Model loaded from disk', hasattr(ml.model, 'feature_importances_'))
check('Feature importance dim', len(ml.model.feature_importances_) == 20)

probs = ml.predict_probabilities(X_test)
check('ML predict shape', len(probs) == len(X_test))
check('ML probs in [0,1]', probs.min() >= 0 and probs.max() <= 1)

rule = ComplianceRuleEngine()
r_flags = rule.evaluate_transaction(df.iloc[0])
check('Rule engine returns rule_score', 'rule_score' in r_flags)

stat = StatisticalAnomalyDetector()
stat.fit(df.iloc[:n_train])
s_flags = stat.evaluate_transaction(df.iloc[0])
check('Stat detector returns statistical_score', 'statistical_score' in s_flags)

ens = EnsembleScorer()
row_dict = {**df.iloc[0].to_dict(), **r_flags, **s_flags}
score, cat = ens.calculate_score(row_dict, float(probs[0]))
check('Ensemble score in [0,100]', 0 <= score <= 100, 'score=%.1f' % score)
check('Ensemble category valid', cat in ['LOW', 'MEDIUM', 'HIGH'], 'cat=%s' % cat)

# 4. Orchestrator
print('\n--- ORCHESTRATOR ---')
orch = AMLOrchestrator(df, graph, ml, n_train=n_train)

plan1 = orch.parse_intent('Find structuring patterns')
check('Parse: structuring', plan1['intent'] == 'structuring')

plan2 = orch.parse_intent('Is customer ACC10822 suspicious?')
check('Parse: entity', plan2['intent'] == 'entity')
check('Parse: ACC filter', plan2['filters'].get('account_id') == 'ACC10822')

plan3 = orch.parse_intent('Show transaction network for community')
check('Parse: network', plan3['intent'] == 'network')

plan4 = orch.parse_intent('Analyse whole dataset')
check('Parse: broad', plan4['intent'] == 'broad')

# Execute a real entity query
fraud_row = df[df['is_fraud'] == 1].iloc[0]
real_acc = fraud_row['sender_id']
plan_real = orch.parse_intent('Is customer %s suspicious?' % real_acc)
res = orch.execute_plan(plan_real)
check('Execute: flagged df not empty', not res['flagged_transactions'].empty)
check('Execute: selected_row exists', res['selected_row'] is not None)
check('Execute: SAR narrative exists', len(res.get('sar_narrative', '')) > 100)
check('Execute: counterfactuals exist', len(res.get('counterfactuals', [])) > 0)
check('Execute: graph HTML path', len(res.get('graph_html_path', '')) > 0)

# 5. Explainability
print('\n--- EXPLAINABILITY ---')
cfs = generate_counterfactuals(fraud_row)
check('Counterfactuals non-empty', len(cfs) > 0)

sar = generate_sar_narrative(fraud_row, 85.0, 'HIGH', cfs)
check('SAR contains header', 'SUSPICIOUS ACTIVITY REPORT' in sar)
check('SAR contains FATF ref', 'FATF' in sar)
check('SAR contains BSA ref', 'BSA' in sar or 'U.S.C.' in sar)

# 6. Regulatory Mapper
print('\n--- REGULATORY MAPPER ---')
for typ in ['structuring', 'layering', 'smurfing', 'rapid_cashout', 'round_tripping', 'normal']:
    info = get_regulation_details(typ)
    check('Reg: %s' % typ, 'title' in info and 'fatf' in info and 'bsa' in info)

# 7. Metrics File
print('\n--- SAVED METRICS ---')
if os.path.exists('data/metrics_summary.csv'):
    m = pd.read_csv('data/metrics_summary.csv').iloc[0]
    rec = float(m['recall'])
    prec = float(m['precision'])
    f1v = float(m['f1'])
    check('Recall > 0.75', rec > 0.75, '%.3f' % rec)
    check('Precision > 0.75', prec > 0.75, '%.3f' % prec)
    check('F1 > 0.75', f1v > 0.75, '%.3f' % f1v)
else:
    check('metrics_summary.csv exists', False, 'MISSING')

# 8. Files Check
print('\n--- FILE PRESENCE ---')
required_files = [
    'app.py', 'evaluate.py', 'demo.py', 'requirements.txt', 'README.md',
    'data/__init__.py', 'data/loader.py', 'data/feature_engineering.py', 'data/synthetic_generator.py',
    'detection/__init__.py', 'detection/rule_engine.py', 'detection/statistical.py',
    'detection/ml_models.py', 'detection/ensemble_scorer.py',
    'graph/__init__.py', 'graph/network_builder.py', 'graph/motif_detector.py', 'graph/visualizer.py',
    'explainability/__init__.py', 'explainability/counterfactual.py', 'explainability/sar_generator.py',
    'regulatory/__init__.py', 'regulatory/compliance_mapper.py',
    'agents/__init__.py', 'agents/orchestrator.py',
]
for f in required_files:
    check('File: %s' % f, os.path.exists(f))

# Summary
print('\n' + '=' * 60)
if failed == 0:
    print('  ALL %d CHECKS PASSED' % passed)
else:
    print('  %d PASSED, %d FAILED out of %d checks' % (passed, failed, passed + failed))
print('=' * 60)

if failed > 0:
    sys.exit(1)
