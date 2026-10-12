<p align="center">
  <img src="assets/banner.svg?v=7" alt="Tuhin Bhattacharya: data analyst and AI builder" width="100%">
</p>

<p align="center">
  <a href="mailto:tuhin.gim@gmail.com"><img src="https://img.shields.io/badge/Email-tuhin.gim%40gmail.com-0b1020?style=for-the-badge&logo=gmail&logoColor=2dd4bf&labelColor=0b1020&color=151a33" alt="Email"></a>
  <a href="https://unique-rugelach-c75c88.netlify.app/"><img src="https://img.shields.io/badge/Live_demo-CLV_Story-0b1020?style=for-the-badge&logo=netlify&logoColor=a78bfa&labelColor=0b1020&color=151a33" alt="Live demo"></a>
  <img src="https://img.shields.io/badge/Status-open_to_roles-0b1020?style=for-the-badge&logo=target&logoColor=fbbf24&labelColor=0b1020&color=151a33" alt="Open to roles">
</p>

<p align="center">
  <img src="assets/about.svg?v=2" alt="Terminal card: whoami, focus, shipped projects, status" width="520">
</p>

<h3 align="center">I find the story hiding in the data, then build the thing that lets people see it.</h3>

<p align="center"><sub><b>ACTIVITY</b></sub></p>
<p align="center">
  <img src="assets/kpi-1.svg?v=7" alt="KPI 1" width="140">
  <img src="assets/kpi-2.svg?v=7" alt="KPI 2" width="140">
  <img src="assets/kpi-3.svg?v=7" alt="KPI 3" width="140">
  <img src="assets/kpi-4.svg?v=7" alt="KPI 4" width="140">
</p>
<p align="center"><sub><b>WORK IN NUMBERS</b></sub></p>
<p align="center">
  <img src="assets/kpi-5.svg?v=7" alt="KPI 5" width="140">
  <img src="assets/kpi-6.svg?v=7" alt="KPI 6" width="140">
  <img src="assets/kpi-7.svg?v=7" alt="KPI 7" width="140">
  <img src="assets/kpi-8.svg?v=7" alt="KPI 8" width="140">
</p>

---

## 🚀 What I've built

<p align="center">
  <a href="https://github.com/Karma1028/CLV_IBM-project"><img src="assets/card-clv.svg?v=7" alt="Customer Lifetime Value" width="400"></a>
  <a href="https://github.com/Karma1028/Stock_App"><img src="assets/card-quant.svg?v=7" alt="Quant Terminal" width="400"></a>
  <a href="https://github.com/Karma1028/Karma-OS"><img src="assets/card-os.svg?v=7" alt="KARMA-OS" width="400"></a>
  <a href="https://github.com/Karma1028/hostel-vibes-radio"><img src="assets/card-radio.svg?v=7" alt="Hostel Vibes Radio" width="400"></a>
  <img src="assets/card-case.svg?v=7" alt="Case-Comp Engine (private)" width="400">
  <img src="assets/card-reel.svg?v=7" alt="Reel Crew (private)" width="400">
</p>

<p align="center"><sub>Cards link to the repos. The bottom row is private. Client and employer work stays private too, and I'm happy to walk through the thinking in an interview.</sub></p>

---

## 📖 Four stories, in order of how much they taught me

### 1. The customers who bleed money
**The question.** An insurer has 9,134 policyholders. What is each one actually worth, and who should it stop chasing?

**What I did.** Forensic EDA first. Then I removed `Total Claim Amount` and the customer ID before touching a model, because both leak the answer. Then a ladder of models, each one justified by the failure of the one before.

**What I found.**
- Linear models scored a *negative* R². The relationships were non-linear, so the simple story was wrong.
- A tuned Random Forest reached **R² ≈ 0.68 (±0.02, cross-validated)** with **~$1,378 mean error**, against **~$4,100** for the "just guess the average" baseline. That's about a third of the error.
- **Monthly premium drove ~84%** of the prediction, and agent-acquired customers were worth **23% more** than digital ones.
- K-Means turned the model into four customer personas, including "bleeding neck" segments with loss ratios above 150%.

**So what.** The report projects more than **$3.4M a year** of value from treating those personas differently. That figure is a projection from my own assumptions, not a realised result, and the report says so. I shipped it as a 10-chapter interactive story with a CLV predictor you can play with: **[open the live site](https://unique-rugelach-c75c88.netlify.app/)**.

### 2. A ticker that vanished overnight
**The question.** In January 2025 Tata Motors split in two, and the old ticker was delisted. Does a machine-learning overlay beat buy-and-hold on the new companies?

**What I did.** Rebuilt the data pipeline around five new series (the two demerged entities, Maruti as a peer, NIFTY 50 and NIFTY Auto as benchmarks) and tagged five market regimes. 23 notebooks later: feature selection, XGBoost and LightGBM, an LSTM with Monte-Carlo-dropout uncertainty, a GARCH volatility gate, an HMM regime router and an LLM agent that writes the report. The research lives in the notebooks, and a Streamlit app wraps the models, the volatility gate and the agent.

**What I found.**
- The best classifier hit **~55% directional accuracy**. In an efficient market that is a real edge and also a small one.
- **Fewer features won.** 30+ shrank to 10-15, and volume and rolling volatility carried the most SHAP weight.
- **ML helped risk more than return.** After costs, buy-and-hold was hard to beat. The overlay's gain was lower drawdowns.

**So what.** The most valuable output was knowing exactly how small the edge is. See the [repo](https://github.com/Karma1028/Stock_App) for the full write-up and the honest limitations section.

### 3. My own data, in one place
**The question.** I lift, I listen to a lot of music, I write notes, and I run AI agents. Why were all of that in different apps?

**What I did.** Built **KARMA-OS**, a 10-view dashboard (Today, Fitness, Vault, Spotify, Memory, Agents, Intel, Tasks, Analytics and an Overview). It has load-ramp charts, a knowledge-vault treemap, an agent delegation graph and a correlation lab across my own streams.

**So what.** It's the project where I practise product thinking on a user I can interview any time. Data currently flows in through a manual pipeline. Live sync is the next milestone.

### 4. A radio for 2 AM corridors
**The idea.** Indian hostel life has a soundtrack and a mood for every hour: the 2 AM corridor, the mess line, exam-night grind, power-cut jam.

**What I did.** Built **Hostel Vibes Radio**, where tapping a room swaps the whole scene *and* the music. A Supabase realtime presence counter shows how many people are awake right now, and the copy is Hinglish throughout.

**So what.** A reminder that some products win on feel, not features.

---

## 🧭 Build log

<p align="center">
  <img src="assets/timeline.svg?v=7" alt="Timeline of public repositories" width="440">
</p>

---

## 🧠 How I think

| Principle | What it looks like in practice |
|---|---|
| **Say the uncertainty out loud** | 55% accuracy is reported as 55%. A $3.4M projection is labelled a projection. |
| **Kill leakage before tuning** | I drop the columns that give the answer away *first*, then see how good the model really is. |
| **If they can't click it, it isn't finished** | Every analysis ends as an app or a story a non-technical reader can use. |
| **Agents are leverage, humans decide** | I wire LLMs into analysis workflows to speed up the boring parts, and keep a person on the call. |

---

## 🧰 Toolbox

<p align="center">
  <img src="assets/langs.svg?v=7" alt="Language breakdown" width="440">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white" alt="pandas">
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white" alt="scikit-learn">
  <img src="https://img.shields.io/badge/XGBoost-337AB7?style=flat-square" alt="XGBoost">
  <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white" alt="PyTorch">
  <img src="https://img.shields.io/badge/SQL-4479A1?style=flat-square&logo=postgresql&logoColor=white" alt="SQL">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Plotly-3F4F75?style=flat-square&logo=plotly&logoColor=white" alt="Plotly">
  <img src="https://img.shields.io/badge/React-20232A?style=flat-square&logo=react&logoColor=61DAFB" alt="React">
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white" alt="TypeScript">
  <img src="https://img.shields.io/badge/D3.js-F9A03C?style=flat-square&logo=d3dotjs&logoColor=white" alt="D3.js">
  <img src="https://img.shields.io/badge/Supabase-3ECF8E?style=flat-square&logo=supabase&logoColor=white" alt="Supabase">
  <img src="https://img.shields.io/badge/LangGraph-1C3C3C?style=flat-square" alt="LangGraph">
  <img src="https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white" alt="Git">
</p>

---

## 🌱 Recent activity

<p align="center">
  <img src="assets/activity.svg?v=7" alt="Contribution heatmap for the last 20 weeks" width="440">
</p>

---

## 🎯 Right now

- **Building:** a case-competition engine that turns a messy brief into a defended deck, and a crew of agents that makes short videos.
- **Going deeper on:** uncertainty in forecasting (MC-dropout, GARCH) and statistical testing for business segments.
- **Looking for:** a **data analyst, analytics engineering or AI engineering** role where the work ends in a decision someone actually makes.

### 💬 Ask me about
`avoiding data leakage` · `why 55% accuracy can still matter` · `LSTM uncertainty with MC-dropout` · `turning models into customer segments` · `wiring LLM agents into analysis workflows`

---

<h3 align="center">Let's talk 📬</h3>

<p align="center">
  <a href="mailto:tuhin.gim@gmail.com"><b>tuhin.gim@gmail.com</b></a><br>
  <sub>I reply. Charts above regenerate daily from my GitHub data, no third-party widgets.</sub>
</p>
