# Infosys Ltd. (NSE: INFY) — Discounted Cash Flow (DCF) Valuation & Equity Research Terminal

A fundamental Discounted Cash Flow (DCF) valuation and interactive financial analytics application for **Infosys Limited (NSE: INFY)**. 

This project bridges **rigorous institutional financial modeling in Microsoft Excel** with **modern financial engineering and interactive data visualization in Python (Streamlit & Plotly)**.

---

## 🚀 Live Interactive Valuation Terminal

Explore the live valuation model with dynamic scenario sliders, real-time market data, and interactive sensitivity matrices:

👉 **[Launch Live Streamlit Dashboard](https://your-streamlit-app-url-here.streamlit.app)**  
*(Deploy via Streamlit Community Cloud and update this link with your live URL)*

---

## 📌 Executive Summary & Investment Thesis

| Metric | Model Estimate | Market Benchmark | Variance / Indication |
| :--- | :---: | :---: | :---: |
| **Intrinsic Fair Value per Share** | **₹1,764.45** | ₹1,130.00 (CMP) | **+56.1% Margin of Safety** |
| **Valuation Recommendation** | **STRONG BUY** | — | Substantially Undervalued |
| **Implied Enterprise Value (EV)** | **₹702,972 Cr** | — | Core Operating Business Value |
| **Implied Equity Value** | **₹715,997 Cr** | ₹458,547 Cr (Mkt Cap) | Net Cash Position Adds Value |
| **Discount Rate (WACC)** | **11.36%** | Cost of Equity: 11.48% | 98.04% Equity / 1.96% Debt |
| **Perpetual Terminal Growth Rate ($g$)** | **5.00%** | Long-Term GDP Trend | Conservative Perpetual Horizon |

### Core Valuation Thesis:
1. **Durable Operating Margins:** Infosys maintains resilient normalized operating margins (~24.0% EBIT), driven by high-margin digital transformation contracts, cloud migrations, and automation efficiencies.
2. **Robust Cash Conversion:** Operating cash conversion remains superior due to an asset-light corporate structure, with Capital Expenditures requiring only ~1.6% of sales.
3. **Pristine Balance Sheet (Net Cash):** Infosys operates with virtually zero net financial leverage, holding **₹22,201 Crore in Cash & Cash Equivalents** against **₹9,176 Crore in total borrowings**, providing a substantial liquidity cushion.
4. **Significant Valuation Asymmetry:** At current market trading levels of ~₹1,130, the market is pricing in steep growth deceleration that ignores Infosys's long-term margin resilience and steady free cash flow compounding.

---

## 📊 End-to-End Excel Financial Modeling Architecture

The valuation engine is grounded in a comprehensive, 7-tab financial model built from audited annual filings:

```
Infosys_DCF_Valuation.xlsx
 │
 ├── 1. Historical Financials ── Audited actuals (FY2022–FY2026)
 ├── 2. Projections ───────────── 5-Year forecast schedule (FY2027–FY2031)
 ├── 3. FCFF Calculation ──────── Unlevered Free Cash Flow engine
 ├── 4. WACC ──────────────────── CAPM & Capital Structure discount rate
 ├── 5. Terminal Value ────────── Gordon Growth Model capitalization
 ├── 6. DCF Valuation ─────────── Enterprise to Equity Value Bridge
 └── 7. Sensitivity Analysis ──── 5x5 Stress-testing matrix
```

### 1. Historical Financial Analysis (FY2022 – FY2026)
* Analyzed 5 years of historical financial performance from audited annual reports:
  * **Revenue:** Scaled from ₹121,641 Cr (FY22) to ₹178,650 Cr (FY26).
  * **Operating Profit (EBIT):** Grew from ₹31,491 Cr to ₹42,280 Cr, maintaining stable operating margins between 23.7% and 25.9%.
  * **Reinvestment Rates:** Evaluated historical Capex (averaging 1.6% of sales) and working capital swings to derive baseline operational intensity.

### 2. Five-Year Forecast Schedule (FY2027 – FY2031)
* **Revenue Growth Trajectory:** Modeled tapering growth rates reflecting mature large-cap IT expansion:
  * FY2027: **10.0%** (₹196,515 Cr)
  * FY2028: **9.0%** (₹214,201 Cr)
  * FY2029: **8.0%** (₹231,337 Cr)
  * FY2030: **7.0%** (₹247,531 Cr)
  * FY2031: **6.0%** (₹262,383 Cr)
* **Normalized EBIT Margin:** Fixed at **24.0%**, consistent with management guidance and historical median performance.
* **Effective Tax Rate:** Modeled at **27.0%**, reflecting corporate tax obligations and export incentives.

### 3. Free Cash Flow to Firm (FCFF) Engine
Free Cash Flow to Firm represents unlevered cash available to all capital providers:
$$\text{FCFF} = \text{NOPAT} + \text{Depreciation} - \text{Capex} - \Delta \text{Net Working Capital}$$
Where:
* $\text{NOPAT} = \text{EBIT} \times (1 - \text{Tax Rate})$
* **Depreciation:** Modeled at **2.9% of Sales** (aligned with historical fixed asset replacement).
* **Capital Expenditures:** Modeled at **1.6% of Sales** (asset-light delivery centers and software licensing).
* **Change in Working Capital ($\Delta \text{NWC}$):** Modeled at **-2.1% of Sales**, reflecting billing schedules and trade receivables cycles.

| Metric (₹ Cr) | FY2027 | FY2028 | FY2029 | FY2030 | FY2031 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Sales** | ₹196,515 | ₹214,201 | ₹231,337 | ₹247,531 | ₹262,383 |
| **EBIT** | ₹47,164 | ₹51,408 | ₹55,521 | ₹59,407 | ₹62,972 |
| **NOPAT** | ₹34,429 | ₹37,528 | ₹40,530 | ₹43,367 | ₹45,970 |
| **+ Depreciation** | ₹5,699 | ₹6,212 | ₹6,709 | ₹7,178 | ₹7,609 |
| **− Capex** | ₹3,144 | ₹3,427 | ₹3,701 | ₹3,960 | ₹4,198 |
| **− Δ NWC** | -₹4,127 | -₹4,498 | -₹4,858 | -₹5,198 | -₹5,510 |
| **FCFF** | **₹41,111** | **₹44,811** | **₹48,396** | **₹51,783** | **₹54,891** |

### 4. Cost of Capital (WACC & CAPM Methodology)
To discount projected cash flows, a **Weighted Average Cost of Capital (WACC)** of **11.36%** was derived using the Capital Asset Pricing Model (CAPM):

$$\text{Cost of Equity } (K_e) = R_f + \beta \times (\text{ERP}) = 6.80\% + (0.85 \times 5.50\%) = 11.48\%$$
$$\text{WACC} = \left(\frac{E}{V} \times K_e\right) + \left(\frac{D}{V} \times K_d \times (1 - t)\right)$$

* **Risk-Free Rate ($R_f$):** **6.80%**, benchmarked to India's 10-Year Government Bond (G-Sec) yield as of July 2026.
* **Beta ($\beta$):** **0.85**, reflecting Infosys's defensive cash profile and lower volatility relative to the broader NIFTY 50 index.
* **Equity Market Risk Premium (ERP):** **5.50%**, the standard institutional expectation for Indian equities.
* **Cost of Debt ($K_d$):** **7.50% pre-tax** (post-tax: $7.50\% \times (1 - 0.27) = \mathbf{5.48\%}$).
* **Capital Structure:** **98.04% Equity ($E/V$)** and **1.96% Debt ($D/V$)**, reflecting Infosys's asset-light, virtually debt-free balance sheet.
* **Resulting WACC:** **11.36%**.

### 5. Terminal Value Calculation (Gordon Growth Model)
All cash flows beyond FY2031 are captured using the Gordon Growth Model:
$$\text{Terminal Value}_{FY2031} = \frac{\text{FCFF}_{FY2032}}{\text{WACC} - g} = \frac{\text{₹54,891 Cr} \times (1 + 0.05)}{0.1136 - 0.05} = \mathbf{₹906,203 \text{ Cr}}$$
* **Perpetual Growth Rate ($g$):** **5.00%**, bounded by long-term Indian GDP growth expectations.
* **Discount Factor ($n=5$):** $1 / (1 + 0.1136)^5 = \mathbf{0.5839}$.
* **Present Value of Terminal Value:** $\text{₹906,203 Cr} \times 0.5839 = \mathbf{₹529,151 \text{ Cr}}$ (75.3% of Enterprise Value).

### 6. Enterprise Value to Equity Value Bridge
$$\text{Enterprise Value} = \sum_{t=1}^5 \text{PV of FCFF} + \text{PV of Terminal Value} = \text{₹173,820 Cr} + \text{₹529,151 Cr} = \mathbf{₹702,972 \text{ Cr}}$$
$$\text{Equity Value} = \text{Enterprise Value} - \text{Total Debt} + \text{Cash \& Equivalents}$$
$$\text{Equity Value} = \text{₹702,972 Cr} - \text{₹9,176 Cr} + \text{₹22,201 Cr} = \mathbf{₹715,997 \text{ Cr}}$$
$$\text{Fair Value per Share} = \frac{\text{₹715,997 Cr}}{405.7938 \text{ Cr Shares}} = \mathbf{₹1,764.45 \text{ per share}}$$

---

### 7. 5x5 Sensitivity Analysis Matrix
A sensitivity matrix was constructed varying the discount rate ($\text{WACC} \pm 100 \text{ bps}$) against the perpetual growth rate ($g \pm 100 \text{ bps}$):

| WACC \ Terminal $g$ | 4.00% | 4.50% | 5.00% | 5.50% | 6.00% |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **10.36%** | ₹1,823 | ₹1,945 | ₹2,091 | ₹2,266 | ₹2,481 |
| **10.86%** | ₹1,691 | ₹1,793 | ₹1,914 | ₹2,056 | ₹2,228 |
| **11.36% (Base)** | ₹1,577 | ₹1,664 | **₹1,764** | ₹1,882 | ₹2,022 |
| **11.86%** | ₹1,477 | ₹1,552 | ₹1,637 | ₹1,736 | ₹1,852 |
| **12.36%** | ₹1,389 | ₹1,454 | ₹1,527 | ₹1,611 | ₹1,708 |

> **Key Takeaway:** Across all 25 tested scenarios, the lowest calculated fair value is **₹1,389 per share**, which remains **~23% above the market price of ₹1,130**, proving significant fundamental downside protection.

---

## 💻 From Excel to Interactive Python Web Application (`app.py`)

To transform the static financial model into an interactive executive tool, the model was engineered into a **Streamlit & Plotly analytics application**:

### Visual Features:
1. **Side-by-Side Command Center:**
   * **Left:** Interactive **TradingView-style Candlestick Chart** (daily OHLC from NSE via `yfinance`, volume bars, 50-day and 200-day Simple Moving Averages, and the **gold DCF Fair Value line at ₹1,764.45** overlaid directly across market price action).
   * **Right:** Dynamic **Plotly Waterfall Bridge** tracking explicit cash flows, terminal value, net debt adjustment, and final equity value.
2. **Interactive Scenario Testing (Sidebar Sliders):**
   * Instant recalculation across **Base Case**, **Bull Case (+200 bps growth)**, and **Bear Case (-200 bps growth)** presets.
   * Sliders for WACC, Terminal Growth, and EBIT operating margins that update all valuation metrics in real time.
3. **Interactive 5x5 Sensitivity Heatmap:**
   * Color-coded matrix annotating exact per-share values across all discount rate and growth rate permutations.

---

## 🛠️ Technology Stack & Dependencies

* **Financial Modeling:** Microsoft Excel (FCFF Modeling, What-If Data Tables, WACC/CAPM)
* **Application Framework:** Streamlit (`>= 1.30.0`)
* **Financial Data & Visuals:** Plotly (`>= 5.15.0`), `yfinance` (`>= 0.2.35`)
* **Numerical Computing:** Pandas (`>= 2.0.0`), NumPy (`>= 1.24.0`)
* **Spreadsheet Parsing:** OpenPyXL (`>= 3.1.0`)

---

## 🏃 Running the Application Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/finance-with-simran/infosys-dcf-valuation.git
   cd infosys-dcf-valuation
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the Streamlit portal:**
   ```bash
   streamlit run app.py
   ```
   *The application will open automatically in your browser at `http://localhost:8501`.*

---

## ☁️ Deploying to Streamlit Community Cloud (Free)

1. Push all files (`app.py`, `requirements.txt`, `README.md`, `Infosys_DCF_Valuation.xlsx`) to your GitHub repository.
2. Go to **[share.streamlit.io](https://share.streamlit.io)** and log in with your GitHub account.
3. Click **"New app"** $\rightarrow$ Select your repository: `finance-with-simran/infosys-dcf-valuation`.
4. Set Main file path to `app.py` and click **"Deploy"**.
5. Copy your live URL and paste it into the placeholder at the top of this `README.md`.

---

## 👤 Author

**Syeda Simran Sarwardi**  
*Aspiring Financial Analyst | Valuation, Corporate Finance & Quantitative Analytics*  
* Kolkata, India  
* [LinkedIn](https://linkedin.com/in/syedasimran) | [GitHub](https://github.com/finance-with-simran)
