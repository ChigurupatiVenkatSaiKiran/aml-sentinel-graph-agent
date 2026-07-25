<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=30&pause=1000&color=00D4FF&center=true&vCenter=true&width=800&lines=AML+Sentinel+—+Financial+Crime+Intelligence;Real-Time+Transaction+Monitoring+%7C+Agentic+AI;Graph-Based+Network+Analysis+%7C+Auto-SAR+Filing" alt="Typing SVG" />

<br/>

[![Python](https://img.shields.io/badge/Language-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Framework-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![NetworkX](https://img.shields.io/badge/Library-NetworkX-orange?style=for-the-badge)](https://networkx.org)
[![Scikit-Learn](https://img.shields.io/badge/ML%20Engine-Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![Plotly](https://img.shields.io/badge/Visualization-Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](LICENSE)

<br/>

| 👥 Team Name | 👤 Team Member | 🎓 Programme | 🆔 Registration Number | 📧 Email |
|:---:|:---|:---:|:---:|:---|
| **spirit** | **Palchuri Rama Anirudh** | Integrated M.Tech CSE | **22MIA1071** | [palchuriramaanirudh@gmail.com](mailto:palchuriramaanirudh@gmail.com) |
| | **Chigurupati Venkat Sai Kiran** | M.Tech CSE (AI & ML) | **25MAI1006** | [chigurupativenkatsai@gmail.com](mailto:chigurupativenkatsai@gmail.com) |

<br/>

> **AML Sentinel** is a state-of-the-art, agentic, multi-layer transaction monitoring and network intelligence platform designed for modern financial institutions. By combining deterministic natural language routing, deep graph community risk modeling, and machine learning, AML Sentinel delivers highly accurate threat detection with an **~88% reduction in compliance overhead and False Alerts**.

<br/>

</div>

---

## 🔗 Live Dashboard Workspace

Reviewers can access the live, interactive Streamlit workspace locally:
👉 **[http://localhost:8501](http://localhost:8501)** *(Run the Streamlit server before clicking)*

---

## ⚡ Key Highlights

<div align="center">

<table>
<tr>
<td align="center" width="200">
<img src="https://img.shields.io/badge/🛡️-Multi--Layer%20Stack-00D4FF?style=for-the-badge"/>
<br/><b>Hybrid Detection</b><br/>
Fuses rules, moving customer Z-scores, ML classifiers, and graph metrics.
</td>
<td align="center" width="200">
<img src="https://img.shields.io/badge/📡-Topological%20Motifs-FF6F00?style=for-the-badge"/>
<br/><b>AML Motifs</b><br/>
Automatically traces cycles, layering chains, fan-out, and aggregation networks.
</td>
<td align="center" width="200">
<img src="https://img.shields.io/badge/🧠-SHAP%20Explainable-7C3AED?style=for-the-badge"/>
<br/><b>Explainable AI</b><br/>
Provides exact feature risk contributions and action-oriented counterfactuals.
</td>
<td align="center" width="200">
<img src="https://img.shields.io/badge/📝-SAR%20Generator-FF4B4B?style=for-the-badge"/>
<br/><b>Compliance Narrative</b><br/>
Auto-drafts legal FinCEN Form 111 narratives mapping directly to FATF/BSA laws.
</td>
</tr>
</table>

</div>

---

## 🖥️ Interactive Dashboard Live View

The visual interface provides compliance officers and auditors with a unified threat workspace:

<div align="center">

| | |
|---|---|
| ![Alerts Workspace](figures/dashboard_main.png) | ![Model Performance & Evaluation](figures/dashboard_performance.png) |
| **🏠 Alerts Workspace & Network Graph** — dynamic natural language routing and live transaction networks | **📏 Performance Breakdown** — 5-fold cross-validation metrics, confusion matrix, and interactive PR curve |
| ![Regulatory Mapping](figures/dashboard_regulatory.png) | |
| **📜 Regulatory Compliance Directory** — FATF recommendations and BSA laws mapped directly to threat alerts | |

</div>

---

## 📌 Table of Contents

- [💡 System Innovation & Value Proposition](#-system-innovation--value-proposition)
- [🏗️ Pipeline Architecture](#️-pipeline-architecture)
- [📝 Real-Time Feature Dictionary & Schema](#-real-time-feature-dictionary--schema)
- [🔬 Core Detection Engines — Technical & Mathematical Breakdown](#-core-detection-engines--technical--mathematical-breakdown)
  - [1. Layer 1 & 2: Compliance Rules & Statistical Z-Score](#1-layer-1--2-compliance-rules--statistical-z-score)
  - [2. Layer 3: Supervised Classification with SHAP Explainability](#2-layer-3-supervised-classification-with-shap-explainability)
  - [3. Layer 4: Network Graph Topology Engine](#3-layer-4-network-graph-topology-engine)
- [⚙️ Model Hyperparameters & Configuration](#️-model-hyperparameters--configuration)
- [📊 System Evaluation Metrics & Ablation Studies](#-system-evaluation-metrics--ablation-studies)
- [🛡️ Engineering: Reliability & Performance Features](#️-engineering-reliability--performance-features)
- [📜 Regulatory Mapping Directory](#-regulatory-mapping-directory)
- [🚀 Quick Start & Installation](#-quick-start--installation)
- [📁 Repository Structure](#-repository-structure)
- [🧰 Tech Stack](#-tech-stack)

---

## 💡 System Innovation & Value Proposition

Traditional transaction monitoring software evaluates rows in isolation, generating massive volumes of False Positives. **AML Sentinel** introduces a hybrid, multi-layer intelligence approach that scores, visualizes, and documents threat vectors simultaneously:

* **⚡ Smart Intent Routing:** Natural language query routing lets analysts type questions (e.g. *"Show structuring alerts"*) and automatically directs the request to the correct sub-engine.
* **🌐 Network-Wide Topology:** Resolves shell account routing by tracking structural network motifs (cycles, pass-through chains).
* **📈 High Precision / High Recall:** Reaches an F1-Score of **`85.39%`** with **`~88%` fewer false alerts**, saving valuable compliance resources.

---

## 🏗️ Pipeline Architecture

Below is the query-to-explainability pipeline of AML Sentinel:

```mermaid
graph TD
    UserQuery[Analyst Query / Search Input] --> AgenticPlanner[Agentic Planner & Routing Engine]
    
    subgraph Multi-Layer Detection Stack
        AgenticPlanner --> Layer1[Layer 1: Compliance Rules Engine]
        AgenticPlanner --> Layer2[Layer 2: Statistical Baseline Profiling]
        AgenticPlanner --> Layer3[Layer 3: RandomForest ML Model]
        AgenticPlanner --> Layer4[Layer 4: Network Graph Topology Engine]
        
        Layer1 -->|Trigger Rule Flags| Scorer[Weighted Ensemble Scorer]
        Layer2 -->|Anomaly Z-Scores| Scorer
        Layer3 -->|ML Probabilities| Scorer
        Layer4 -->|PageRank, Louvain Risk & Motifs| Scorer
    end

    Scorer --> RiskScore[Ensemble Risk Score: 0-100]
    
    subgraph Explainability & Narrative Output
        RiskScore --> SHAP[Local SHAP Contributions]
        RiskScore --> Counterfactual[Counterfactual Recommendations]
        RiskScore --> Compliance[FATF / BSA Regulatory Mapper]
        RiskScore --> SAR[Auto-Generated SAR Narrative Draft]
    end

    SHAP --> UI[Premium Glassmorphic Analyst Dashboard]
    Counterfactual --> UI
    Compliance --> UI
    SAR --> UI
```

---

## 📝 Real-Time Feature Dictionary & Schema

The dataset loader extracts **20 features** covering transaction profiles, customer behavior, network centrality, and graph topology:

| Category | Feature Name | Data Type | Description |
|:---|:---|:---:|:---|
| **Transaction-Level** | `amount` | Float | Transaction value in USD. |
| | `is_round_amount` | Binary | Flag indicating if amount is divisible by 100 (common in shell routing). |
| | `is_structuring_amount` | Binary | Flag indicating if amount is between \$8,000 and \$9,999 (just below CTR limit). |
| | `hour_of_day` | Integer | Hour of transaction (0-23) for temporal anomaly analysis. |
| **Behavioral Windows** | `tx_count_1d` | Integer | Total transactions by sender in the last 24 hours. |
| | `tx_count_7d` | Integer | Total transactions by sender in the last 7 days. |
| | `tx_sum_1d` | Float | Total sum sent by sender in the last 24 hours. |
| | `tx_sum_7d` | Float | Total sum sent by sender in the last 7 days. |
| | `unique_recipients_7d` | Integer | Number of unique recipient accounts in the last 7 days. |
| | `time_since_last_tx_hours`| Float | Hours since sender's previous transaction (default 999.0 for new senders). |
| | `is_rapid_cashout` | Binary | Flag: account received money, then sent $\ge 85\%$ within 2 hours. |
| **Network Centrality** | `pagerank_score` | Float | PageRank centrality of sender in the transaction network. |
| | `in_degree` | Integer | Node in-degree (number of incoming transaction paths). |
| | `out_degree` | Integer | Node out-degree (number of outgoing transaction paths). |
| | `clustering_coefficient` | Float | Node clustering coefficient (local neighborhood density). |
| | `community_risk_score` | Float | **Leakage-free** Louvain community risk density (fitted on training labels). |
| **Graph Motifs** | `is_cycle_edge` | Binary | Flag indicating if the edge forms a round-tripping loop (length 3-5). |
| | `is_fan_out_edge` | Binary | Flag indicating if the edge originates from a fan-out (smurfing) node ($\ge 4$ receivers). |
| | `is_fan_in_edge` | Binary | Flag indicating if the edge routes into an aggregation node ($\ge 4$ senders). |
| | `is_chain_edge` | Binary | Flag indicating if the edge belongs to a linear pass-through chain ($\ge 3$ hops). |

---

## 🔬 Core Detection Engines — Technical & Mathematical Breakdown

### 1. Layer 1 & 2: Compliance Rules & Statistical Z-Score
* **Rules Engine:** Evaluates hard threshold rules such as rapid sweeps or transaction amounts just under reporting thresholds (e.g., structuring).
* **Statistical Profiling:** Computes rolling customer-specific historical baselines. Anomalies are detected via moving window Z-scores:
  $$Z = \frac{x_t - \mu_w}{\sigma_w}$$
  where $\mu_w$ and $\sigma_w$ represent the rolling transaction sum mean and standard deviation over a $W$-day window.

### 2. Layer 3: Supervised Classification with SHAP Explainability
* Trains a non-linear **RandomForestClassifier** on transactional, behavioral, and structural graph features.
* Avoids the "black-box" ML issue by using **TreeSHAP** to compute exact additive feature contributions for every alert. For a transaction $x$, the prediction $f(x)$ is decomposed as:
  $$f(x) = \phi_0 + \sum_{i=1}^{M} \phi_i(x)$$
  where $\phi_0$ is the base expectation and $\phi_i(x)$ is the SHAP value showing how feature $i$ shifted the risk score.

### 3. Layer 4: Network Graph Topology Engine
Constructs a directed, weighted transaction network $G = (V, E)$ where nodes $V$ represent bank accounts and edges $E$ represent money flows.

#### A. Weighted PageRank (Centrality)
Identifies core accounts funneling cash. PageRank is computed recursively:
$$PR(u) = \frac{1-d}{|V|} + d \sum_{v \in B_u} \frac{PR(v)}{L(v)}$$
where $B_u$ is the set of accounts sending money to $u$, $L(v)$ is the out-degree of $v$, and $d = 0.85$ is the damping factor.

#### B. Louvain Community Detection & Modularity
Groups accounts into transaction communities by maximizing Modularity ($Q$):
$$Q = \frac{1}{2m} \sum_{i,j} \left[ A_{ij} - \frac{k_i k_j}{2m} \right] \delta(c_i, c_j)$$
where $A_{ij}$ is the transaction volume between accounts $i$ and $j$, $k_i$ is the total volume of account $i$, $m$ is the network's total transaction volume, and $\delta$ flags community co-membership.
* **Guilt by Association:** Community Risk is computed as the percentage of training-set fraud labels located within community $c$:
  $$\text{Community Risk}(c) = \frac{\sum_{i \in c} y_{i}^{\text{train}}}{|c|}$$

#### C. Topological Motif Traversal
We traverse the graph to identify structural money laundering shapes:

| Motif | Target Typology | Structural Pattern | Graphical Representation |
| :--- | :--- | :--- | :--- |
| **Fan-Out** | Smurfing (Placements) | Single source $\rightarrow$ Many recipients ($\ge 4$) | `(A) --> (B, C, D, E)` |
| **Fan-In** | Aggregation (Layering) | Many senders $\rightarrow$ Single recipient ($\ge 4$) | `(B, C, D, E) --> (A)` |
| **Chains** | Pass-Through Layering | Multi-hop linear nodes (in=1, out=1, depth $\ge 3$) | `(A) --> (B) --> (C) --> (D)` |
| **Cycles** | Round-Tripping | Closed loop back to sender (length 3-5) | `(A) --> (B) --> (C) --> (A)` |

---

## ⚙️ Model Hyperparameters & Configuration

To ensure full reproducibility, the model parameters and ensemble fusion logic are configured as follows:

```
RandomForestClassifier Configuration:
  ├── n_estimators = 100
  ├── max_depth = 10
  ├── random_state = 42
  └── class_weight = 'balanced'

Ensemble Risk Scoring Weights (Fusing Layers 1-4):
  ├── Layer 1 (Compliance Rules)  Weight = 0.15
  ├── Layer 2 (Moving Z-Score)    Weight = 0.20
  ├── Layer 3 (Random Forest ML)  Weight = 0.35
  └── Layer 4 (Network Topology)  Weight = 0.30
  └── Ensemble Threshold Trigger  Score  >= 35.0
```

---

## 📊 System Evaluation Metrics & Ablation Studies

All metrics are measured on an **80/20 train/test split** and validated using **Stratified 5-Fold Cross-Validation** (with zero community label leakage) to simulate live compliance restrictions. 

### 1. Stratified 5-Fold Cross-Validation Metrics (Mean ± Std)
* **CV Recall:** **`85.23% ± 3.98%`**
* **CV Precision:** **`85.75% ± 4.26%`**
* **CV F1 Score:** **`85.39% ± 3.05%`**

### 2. Held-Out 80/20 Test Split Ablation Study
Tested on a held-out test split containing `51` positive fraud cases out of `1,691` total test transactions:

| Layer Mode | Recall (%) | Precision (%) | F1 Score (%) | False Positives |
| :--- | :---: | :---: | :---: | :---: |
| **Layer 1 (Rules Only)** | 45.1% | 20.4% | 28.0% | 90 |
| **Layer 2 (+ Statistical Profiling)** | 78.4% | 15.0% | 25.2% | 226 |
| **Layer 3 (+ RandomForest ML)** | 78.4% | 81.6% | 80.0% | 9 |
| **Layer 4 (+ Graph Network / Full Ensemble)** | **80.4%** | **77.4%** | **78.8%** | **11** |

---

## 🛡️ Engineering: Reliability & Performance Features

This platform was built to satisfy high performance and robustness benchmarks required by enterprise reviewers:

* **⚡ Ultra-Fast Vectorized Feature Caching:** Replaced slow iterative loops with vectorized pandas calculations and a high-speed disk cache (`data/processed_cache.parquet`). This brought the dashboard load time down from **~30 seconds to <2 seconds** for all subsequent runs.
* **🔒 Chronological Training Splits:** Transactions are sorted by time before splitting into train/test to prevent future transaction data from leaking into the historical training set.
* **🧠 Explainer Cache Resilience:** Features an automated check to bypass bitsandbytes quantization conflicts, ensuring RandomForest classification and SHAP explainer runs reliably across any standard environment.

---

## 📜 Regulatory Mapping Directory

Identified AML typologies map to official compliance recommendations and laws:

| Typology | FATF Standard Recommendation | BSA Legal Citation | Operational Compliance Protocol |
| :--- | :--- | :--- | :--- |
| **Structuring** | **Rec 20:** Suspicious Transaction Reporting | **31 U.S.C. § 5324** / **31 C.F.R. § 1010.314** | Flag under CTR threshold, prompt auto-SAR drafting. |
| **Layering** | **Rec 10-11:** CDD / Record Keeping | **31 U.S.C. § 5318(g)** | Freeze related accounts, trace hop distance, compile counterparty graph. |
| **Smurfing** | **Rec 16:** Wire Transfers / Originator Info | **31 C.F.R. § 1020.320** | Map fan-out cluster, analyze origin funds, check PEP registry. |
| **Rapid Cashout**| **Rec 20:** Immediate SAR filing | **31 C.F.R. § 1010.320** | High-velocity check, trigger temporary holding protocol. |
| **Round-Tripping**| **Rec 10:** CDD on Beneficial Ownership | **31 C.F.R. § 1010.230** | Identify Ultimate Beneficial Owner (UBO) of source/sink entities. |

---

## 🚀 Quick Start & Installation

### Prerequisites
* Python 3.9, 3.10, or 3.11 installed.

### 1. Clone & Install
```bash
git clone https://github.com/ChigurupatiVenkatSaiKiran/aml-sentinel-graph-agent.git
cd aml-sentinel-graph-agent
pip install -r requirements.txt
```

### 2. Run CLI Evaluation and Model Train
Trains the RandomForest model, evaluates metrics, and generates target files:
```bash
python evaluate.py
```

### 3. Launch Streamlit UI
Run the interactive analyst UI:
```bash
streamlit run app.py --server.port 8501
```
Open **`http://localhost:8501`** in your browser.

---

## 📁 Repository Structure

```
aml-sentinel-graph-agent/
├── app.py                      # Premium Streamlit web dashboard
├── evaluate.py                 # Evaluation metrics harness & model training
├── demo.py                     # Standalone CLI query demonstration
├── requirements.txt            # Package dependencies
├── .gitignore                  # Custom file exclusions
│
├── data/
│   ├── loader.py               # Aligned train/test splitting (zero leakage)
│   ├── feature_engineering.py  # Vectorized rolling & static feature engine
│   ├── synthetic_generator.py  # Bridged synthetic AML network generator
│   └── metrics_summary.csv     # Live data source for UI dashboard stats
│
├── graph/
│   ├── network_builder.py      # PageRank, Louvain community pre-computations
│   ├── motif_detector.py       # Traversal engine for chains, cycles, fan-in/out
│   └── visualizer.py           # PyVis HTML graph layout exporter
│
├── detection/
│   ├── rule_engine.py          # Legacy rule-matching threshold engine
│   ├── statistical.py          # Rolling customer Z-score profile detector
│   ├── ml_models.py            # RandomForest ML manager
│   └── ensemble_scorer.py      # Dynamic, weighted multi-layer scoring engine
│
├── explainability/
│   ├── counterfactual.py       # Analyst action guidance generator
│   └── sar_generator.py        # FinCEN Form 111 Narrative drafts builder
│
└── regulatory/
    └── compliance_mapper.py    # FATF/BSA regulatory citations lookup directory
```

---

## 🧰 Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Graph Theory** | NetworkX | Traversal engine for cycles, chains, communities |
| **ML Engine** | RandomForest | Dynamic classifier identifying transaction risks |
| **Explainable AI** | SHAP / Counterfactuals | Local feature log-odds & actionable guidance |
| **Compliance Engine** | Regex / Keyword routing | Query intent parsing & regulatory mapping |
| **Visual Dashboard** | Streamlit + Plotly | Dark-themed compliance analyst workspace |

---

<div align="center">

**Built with ❤️ by Team spirit**

| Member | Programme | Registration Number | Email |
|:---|:---:|:---:|:---|
| **Palchuri Rama Anirudh** | Integrated M.Tech CSE | **22MIA1071** | [palchuriramaanirudh@gmail.com](mailto:palchuriramaanirudh@gmail.com) |
| **Chigurupati Venkat Sai Kiran** | M.Tech CSE (AI & ML) | **25MAI1006** | [chigurupativenkatsai@gmail.com](mailto:chigurupativenkatsai@gmail.com) |

*Societe Generale Hackathon, Chennai Campus (Graduation 2027)*

<br/>

⭐ **Star this repo if you found it useful!**

<br/>

<img src="https://img.shields.io/github/stars/ChigurupatiVenkatSaiKiran/aml-sentinel-graph-agent?style=social"/>
<img src="https://img.shields.io/github/forks/ChigurupatiVenkatSaiKiran/aml-sentinel-graph-agent?style=social"/>

</div>
