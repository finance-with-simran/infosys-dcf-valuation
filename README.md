# Infosys Ltd — DCF Valuation Model

A ground-up Discounted Cash Flow (DCF) valuation of **Infosys Ltd (NSE: INFY)**, built entirely in Excel, to estimate the company's intrinsic fair value per share and compare it against its current market price.

## 📌 Project Overview

This project values Infosys using the **Free Cash Flow to Firm (FCFF)** approach — projecting the company's future cash flows, discounting them back to present value using a calculated WACC, and deriving a fair value per share. The model also includes a full **Sensitivity Analysis** to test how the valuation holds up across a range of key assumptions.

**Objective:** Determine whether Infosys is fairly valued, undervalued, or overvalued relative to its current market price, using a fundamentals-driven approach.

## 🔑 Key Result

| Metric | Value |
|---|---|
| **Fair Value per Share (Base Case)** | ₹1,764.43 |
| **Current Market Price** | ₹1,130.00 |
| **Implied Upside** | ~56% |
| **Sensitivity Range (WACC 10.36%–12.36%, Growth 4%–6%)** | ₹1,389 – ₹2,481 |

Even under the most conservative assumptions tested, the model's fair value estimate stays above the current market price — suggesting Infosys may be undervalued based on this analysis.

## 🛠️ Methodology

The model is built across 6 structured tabs, following a standard institutional DCF framework:

1. **Historical Financials** — 5 years of Infosys's actuals (FY2022–FY2026) sourced from screener.in, covering Sales, EBIT, Tax Rate, Depreciation, Capex, and Working Capital changes.

2. **FCFF Calculation** — Historical Free Cash Flow to Firm computed as:
   `FCFF = EBIT × (1 − Tax Rate) + Depreciation − Capex − Δ Working Capital`

3. **Projections** — 5-year forward forecast (FY2027–FY2031) using a tapering revenue growth rate (10% → 6%), stable EBIT margin (~24%), and reinvestment ratios (Depreciation, Capex, Working Capital) held at historical averages as a % of Sales.

4. **WACC** — Discount rate calculated using CAPM for Cost of Equity (Risk-Free Rate + Beta × Market Risk Premium) blended with post-tax Cost of Debt, weighted by Infosys's actual capital structure (~98% equity-funded).

5. **DCF Valuation** — Each year's projected FCFF and a Gordon Growth Terminal Value (5% perpetual growth) discounted back to present value, aggregated into Enterprise Value, then adjusted for Debt and Cash to reach Equity Value and Fair Value per Share.

6. **Sensitivity Analysis** — A 5×5 data table testing Fair Value per Share across a range of WACC and Terminal Growth Rate combinations, to assess how dependent the conclusion is on key assumptions.

## 📊 Key Assumptions

| Assumption | Value | Basis |
|---|---|---|
| Forecast Period | 5 years (FY2027–FY2031) | Standard DCF horizon |
| Revenue Growth | Tapers 10% → 6% | Reflects slowing growth as base scales |
| EBIT Margin | ~24% | 5-year historical average |
| Tax Rate | ~27% | 5-year historical average |
| Risk-Free Rate | 6.8% | India 10-Year G-Sec yield |
| Beta | 0.85 | Typical for large-cap Indian IT services |
| Market Risk Premium | 5.5% | Standard assumption, Indian equities |
| WACC | 11.36% | CAPM-based, weighted by actual capital structure |
| Terminal Growth Rate | 5.0% | Long-term India nominal GDP growth proxy |

## 🧰 Tools Used

- **Microsoft Excel** — full model build, formula-driven (no hardcoded outputs)
- **Screener.in** — source for historical financial statements
- Data table / What-If Analysis for Sensitivity testing

## ⚠️ Limitations

- DCF outputs are highly sensitive to WACC and Terminal Growth assumptions, as shown in the Sensitivity Analysis — small shifts materially move the valuation.
- Margins and reinvestment ratios are assumed stable; the model does not explicitly account for structural shifts (e.g., AI's impact on IT services demand, currency volatility, macro slowdowns).
- Beta and Market Risk Premium are assumed based on industry norms due to inconsistent reporting across data sources.

## 📁 Files

- `Infosys_DCF_Valuation.xlsx` — full model with all 6 tabs, formulas, and notes

---

*This project was built as part of an independent finance portfolio to demonstrate applied valuation and financial modeling skills.*
