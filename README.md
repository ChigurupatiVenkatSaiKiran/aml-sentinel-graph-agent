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

> **AML Sentinel** is an intelligent, multi-layer transaction monitoring and network investigation platform. By combining rules, machine learning, and network graph analysis, AML Sentinel slashes False Alerts by **~88%** while identifying complex money laundering patterns in real-time.

<br/>

</div>

---

## ⚙️ Performance at a Glance

<div align="center">

| 📊 Metric | 🎯 AML Sentinel Score |
| :--- | :---: |
| **Recall (5-Fold CV)** | 🏆 **85.23% ± 3.98%** |
| **Precision (5-Fold CV)** | 🏆 **85.75% ± 4.26%** |
| **F1-Score (5-Fold CV)** | 🏆 **85.39% ± 3.05%** |
| **False Positives Eliminated** | 🏆 **~88% Reduction** |
| **False Alert Count (Holdout)** | **11** *(down from 90 with rules-only baseline)* |

</div>

> ✅ **In plain English:** Out of every 100 real fraud cases, our system correctly catches **85**. Out of every 100 alerts it raises, **85 are genuine fraud** — compliance officers waste almost no time chasing false leads. The ± values show our results are **consistent across all 5 test folds**, not just a one-time lucky result.

---

## 🔗 Live Dashboard Access

Reviewers can access the live, interactive Streamlit workspace locally:
👉 **[http://localhost:8501](http://localhost:8501)** *(Ensure the Streamlit server is active before clicking)*

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
- [📝 Feature Dictionary (Simplified)](#-feature-dictionary-simplified)
- [🔬 Core Detection Layers (How It Works)](#-core-detection-layers-how-it-works)
- [⚙️ System Evaluation Metrics & Performance](#️-system-evaluation-metrics--performance)
- [🛡️ Engineering & Optimization Features](#️-engineering--optimization-features)
- [📜 Regulatory Mapping Directory](#-regulatory-mapping-directory)
- [🚀 Quick Start & Installation](#-quick-start--installation)
- [📁 Repository Structure](#-repository-structure)
- [🧰 Tech Stack](#-tech-stack)

---

## 💡 System Innovation & Value Proposition

Traditional transaction monitoring software evaluates rows in isolation, generating massive volumes of False Positives. **AML Sentinel** introduces a hybrid, multi-layer intelligence approach that scores, visualizes, and documents threat vectors simultaneously:

* **💬 Natural Language Agent Interface:** Analysts can type questions in plain English (e.g. *"Analyze dataset for suspicious activity"*), and the agent dynamically parses the query and routes it to the correct detection layers.
* **🌐 Network-Wide Topology:** Resolves shell account routing by tracking money flows across graph patterns (loops, pass-through chains).
* **📈 High Precision / High Recall:** Reaches a high F1-Score of **`85.39%`** with **`~88%` fewer false alerts**, saving valuable compliance resources.

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

## 📝 Feature Dictionary (Simplified)

AML Sentinel automatically extracts and analyzes the following metrics for every transaction:

| Category | Feature Name | Description |
|:---|:---|:---|
| **Transaction-Level** | `amount` | Transaction value in USD. |
| | `is_round_amount` | Indicates if amount is divisible by 100 (common in shell routing). |
| | `is_structuring_amount` | Indicates if amount is between \$8,000 and \$9,999 (just below CTR limit). |
| | `hour_of_day` | Hour of transaction (0-23) for temporal anomaly analysis. |
| **Customer Behavior** | `tx_count_1d` / `tx_count_7d` | Total transactions by sender in the last 24 hours / 7 days. |
| | `tx_sum_1d` / `tx_sum_7d` | Total sum sent by sender in the last 24 hours / 7 days. |
| | `unique_recipients_7d` | Number of unique recipient accounts in the last 7 days. |
| | `time_since_last_tx_hours`| Hours since sender's previous transaction. |
| | `is_rapid_cashout` | Indicates if account received money, then sent >= 85% within 2 hours. |
| **Network Position** | `pagerank_score` | PageRank score of the sender (identifies accounts funneling high traffic). |
| | `in_degree` / `out_degree` | Number of incoming / outgoing transaction paths. |
| | `clustering_coefficient` | Local neighborhood density (flags tightly-knit groups). |
| | `community_risk_score` | Risk score of the sender's community based on historical labels. |
| **Graph Motifs** | `is_cycle_edge` | Edge forms a circular round-tripping loop (length 3-5). |
| | `is_fan_out_edge` | Edge originates from a fan-out node (>= 4 receivers; flags smurfing). |
| | `is_fan_in_edge` | Edge routes into an aggregation node (>= 4 senders; flags collection). |
| | `is_chain_edge` | Edge belongs to a linear pass-through chain (>= 3 hops; flags layering). |

## 🔬 Core Detection Layers (How It Works)

AML Sentinel operates a sequential, four-layer intelligence funnel. Each layer adds a higher level of complexity, filtering out false alerts while capturing hidden anomalies:

### 🛡️ Layer 1: Rule-Based Compliance Engine
* **What it does:** Evaluates individual transactions against strict compliance thresholds (the traditional banking approach).
* **How it works:** Checks simple, high-confidence flags. For example, it checks if a transaction is between \$8,000 and \$9,999 (structuring), indicating an intentional attempt to bypass the \$10,000 Currency Transaction Report (CTR) filing limit.
* **Core Benefit:** Instantly catches obvious, high-risk threshold violations.

### 📈 Layer 2: Statistical Customer Profiling (Moving Z-Score)
* **What it does:** Tracks behavioral spikes tailored to each individual account.
* **How it works:** Rather than using universal limits, it calculates a customer's rolling 7-day average transaction amount. If a new transaction suddenly spikes multiple standard deviations above their typical historical baseline (their Z-Score), it triggers a behavioral flag.
* **Core Benefit:** Adapts dynamically to normal spending variations, catching anomalous account takeovers or sudden sweeps.

### 🧠 Layer 3: Machine Learning Model (RandomForest) with SHAP Explainability
* **What it does:** Analyzes complex, multi-dimensional correlations that traditional static rules miss.
* **How it works:** Fuses transaction limits, behavioral rolling windows, time intervals, and network features into a non-linear Random Forest classifier model.
* **💡 TreeSHAP local explainability:** To avoid "black-box" machine learning, we compute exact local feature contributions for every alert. The analyst sees exactly how much each feature shifted the risk score (e.g., a high amount increased risk by +18%, but a clean rolling frequency pulled it down by -5%), offering full compliance transparency.

### 📡 Layer 4: Network Graph Topology Engine
* **What it does:** Builds a directed transaction graph where accounts are nodes and transactions are edges, tracing money laundering paths.
* **How it works:** Computes three distinct graph theory metrics:
  1. **PageRank Centrality:** Traces the flow of funds to identify key accounts funneling high volumes of money.
  2. **Louvain Community Detection:** Automatically segments the entire network into transaction communities. It calculates "Guilt-by-Association" risk based on the density of known bad actors in a community, flagging accounts that interact in high-risk circles.
  3. **Topological Motif Traversal:** Scans the network structure to identify specific money routing shapes:
     * **Fan-Out (Smurfing):** A single source splitting funds into multiple accounts `(A) --> (B, C, D, E)`.
     * **Fan-In (Aggregation):** Multiple accounts funneling money into a single collector `(B, C, D, E) --> (A)`.
     * **Chains (Layering):** Multi-hop pass-through nodes designed to hide origins `(A) --> (B) --> (C) --> (D)`.
     * **Cycles (Round-Tripping):** Circular loops routing funds back to the sender `(A) --> (B) --> (C) --> (A)`.

---

## 🛡️ Engineering & Optimization Features

* **⚡ Parquet Disk Caching:** We cache engineered features to disk (`processed_cache.parquet`). The dashboard starts and runs in **<2 seconds** after the initial load.
* **🔒 Chronological Splitting:** Transactions are sorted by time before splitting into training/testing sets, ensuring no future transaction data leaks into the past.
* **Resilient Environment Setup:** Automatically resolves package scaling dependencies (e.g. bitsandbytes/PyArrow configs) to run smoothly on any developer laptop.

---

## 📜 Regulatory Mapping Directory

Identified AML typologies map directly to official compliance recommendations and laws:

| Typology | FATF Standard Recommendation | BSA Legal Citation | Operational Compliance Protocol |
| :--- | :--- | :--- | :--- |
| **Structuring** | **Rec 20:** Suspicious Transaction Reporting | **31 U.S.C. § 5324** / **31 C.F.R. § 1010.314** | Flag under CTR threshold, prompt auto-SAR drafting. |
| **Layering** | **Rec 10-11:** CDD / Record Keeping | **31 U.S.C. § 5318(g)** | Freeze related accounts, trace hop distance, compile counterparty graph. |
| **Smurfing** | **Rec 16:** Wire Transfers / Originator Info | **31 C.F.R. § 1020.320** | Map fan-out cluster, analyze origin funds, check PEP registry. |
| **Rapid Cashout**| **Rec 20:** Immediate SAR filing | **31 C.F.R. § 1010.320** | High-velocity check, trigger temporary holding protocol. |
| **Round-Tripping**| **Rec 10:** CDD on Beneficial Ownership | **31 C.F.R. § 1010.230** | Identify Ultimate Beneficial Owner (UBO) of source/sink entities. |

---

## 🚀 Quick Start & Installation

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
├── app.py                      # Streamlit web dashboard
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
