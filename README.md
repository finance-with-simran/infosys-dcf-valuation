# 📈 Infosys Ltd. — Discounted Cash Flow (DCF) Valuation Model & Interactive Analytics Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-streamlit-app-url-here.streamlit.app)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An institutional-grade **Discounted Cash Flow (DCF) valuation** and **interactive equity research application** for **Infosys Ltd (NSE: INFY)**. 

Built using the **Free Cash Flow to Firm (FCFF)** methodology, this project bridges fundamental corporate finance modeling (Excel) with modern financial analytics and interactive web engineering (Python & Streamlit).

---

## 🚀 Live Interactive Dashboard

Explore the live valuation model with dynamic sensitivity sliders and scenario testing:

https://finance-with-simran-infosys-dcf-valuation-app-lvgbrr.streamlit.app/

*(Replace this URL with your live Streamlit Cloud link after deploying)*

---

## 📌 Executive Summary & Key Results

| Metric | Model Estimate | Benchmark / Market | Variance / Implication |
| :--- | :---: | :---: | :---: |
| **Intrinsic Fair Value per Share** | **₹1,764.45** | ₹1,130.00 (CMP) | **+56.1% Margin of Safety** |
| **Valuation Verdict** | **STRONG BUY** | — | Substantially Undervalued |
| **Implied Enterprise Value (EV)** | **₹702,972 Cr** | — | 5-Yr PV + Terminal Value |
| **Implied Equity Value** | **₹715,997 Cr** | ₹458,547 Cr (Mkt Cap) | Net Cash Position Adds Value |
| **Discount Rate (WACC)** | **11.36%** | Cost of Equity: 11.48% | 98.0% Equity / 2.0% Debt |
| **Perpetual Terminal Growth ($g$)**| **5.00%** | India Long-Term GDP Trend | Conservative Horizon Target |

---

## 🔑 Key Features of the Analytics Portal

1. **Enterprise Value to Equity Value Bridge (Waterfall Chart):**
   * Breaks down explicit 5-year cash flow present value (₹173.8K Cr / 24.7%) vs. terminal value present value (₹529.2K Cr / 75.3%).
   * Adjusts for Balance Sheet cash (₹22,201 Cr) and total borrowings (₹9,176 Cr) to establish intrinsic equity value.
2. **Interactive Valuation Simulator (Sidebar Sliders):**
   * Allows users to stress-test the model by dynamically altering the **WACC discount rate (9.5%–13.5%)**, **terminal growth rate (3.5%–6.5%)**, and **EBIT operating margins (20%–28%)**.
   * Instantaneous recalculation of fair value per share across Base, Bull, and Bear case scenarios.
3. **5x5 Sensitivity Matrix Heatmap:**
   * Evaluates 25 distinct valuation permutations crossing WACC ($\pm 100$ bps) against terminal growth rates ($\pm 100$ bps).
   * Confirms margin-of-safety resilience: Fair value remains above current market price (₹1,389 to ₹2,481) across all tested scenarios.
4. **Detailed 5-Year Forecast Schedule (FY2027–FY2031):**
   * Transparent forecasting of Sales, EBIT, NOPAT, Depreciation, Capex, and Net Working Capital changes.
5. **Cost of Capital (WACC / CAPM) Breakdown:**
   * Rigorous documentation of India 10Y G-Sec risk-free rate, Beta, Equity Risk Premium, and asset-light capital structure weighting.

---

## 📐 Financial Methodology & Valuation Architecture

### 1. Free Cash Flow to Firm (FCFF) Formula
$$\text{FCFF} = \text{NOPAT} + \text{Depreciation} - \text{Capital Expenditures (Capex)} - \Delta \text{Net Working Capital (NWC)}$$
Where:
* $\text{NOPAT} = \text{EBIT} \times (1 - \text{Effective Tax Rate})$
* Normalized EBIT Margin: **24.0%**
* Effective Tax Rate: **27.0%**
* Depreciation Rate: **2.9% of Sales**
* Capital Expenditures: **1.6% of Sales** (Asset-light IT services model)
* Working Capital Requirement: **-2.1% of Sales**

### 2. Weighted Average Cost of Capital (WACC) via CAPM
$$\text{Cost of Equity } (K_e) = R_f + \beta \times (\text{ERP}) = 6.80\% + 0.85 \times 5.50\% = 11.48\%$$
$$\text{WACC} = \left(\frac{E}{V} \times K_e\right) + \left(\frac{D}{V} \times K_d \times (1 - t)\right)$$
* **Risk-Free Rate ($R_f$):** 6.80% (Benchmark India 10-Year Government Bond Yield as of July 2026)
* **Beta ($\beta$):** 0.85 (Defensive large-cap IT services, lower market volatility)
* **Equity Risk Premium (ERP):** 5.50%
* **Pre-Tax Cost of Debt ($K_d$):** 7.50% (Post-tax: 5.48%)
* **Capital Structure:** 98.04% Equity ($E/V$) / 1.96% Debt ($D/V$)
* **Derived WACC:** **11.36%**

### 3. Terminal Value (Gordon Growth Model)
$$\text{Terminal Value}_{FY2031} = \frac{\text{FCFF}_{FY2032}}{\text{WACC} - g} = \frac{\text{FCFF}_{FY2031} \times (1 + g)}{\text{WACC} - g}$$
* Terminal Growth Rate ($g$): **5.00%**
* Terminal Value at FY2031: **₹906,203 Cr**
* Present Value of Terminal Value: **₹529,151 Cr**

---

## 📂 Project Repository Structure

```
├── app.py                         # Streamlit Interactive Valuation Portal
├── Infosys_DCF_Valuation.xlsx      # Original 7-tab Excel financial model
├── requirements.txt               # Python package dependencies for deployment
└── README.md                      # Comprehensive project documentation
```

---

## 💻 Running the Application Locally

### Prerequisites
* Python 3.9 or higher installed on your machine.

### Installation & Launch Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/finance-with-simran/infosys-dcf-valuation.git
   cd infosys-dcf-valuation
   ```

2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit dashboard:**
   ```bash
   streamlit run app.py
   ```
   *The application will launch automatically in your browser at `http://localhost:8501`.*

---

## ☁️ How to Deploy to Streamlit Community Cloud (Free)

1. Fork or push this repository to your GitHub account (`finance-with-simran/infosys-dcf-valuation`).
2. Visit **[share.streamlit.io](https://share.streamlit.io)** and sign in with your GitHub account.
3. Click **"New app"**, select your repository: `finance-with-simran/infosys-dcf-valuation`.
4. Set Main file path to: `app.py`.
5. Click **"Deploy"**.
6. Once deployed, copy your live link (e.g., `https://infosys-dcf-valuation.streamlit.app`) and paste it into the placeholder at the top of this `README.md`!

---

## 👤 Author

**Syeda Simran Sarwardi**  
*Aspiring Financial Analyst | Financial Modeling & Quantitative Analytics*  
* Kolkata, India  
* [LinkedIn](https://linkedin.com/in/syedasimran) | [GitHub](https://github.com/finance-with-simran)
