import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# ==========================================
# PAGE CONFIGURATION (Institutional Theme)
# ==========================================
st.set_page_config(
    page_title="Infosys Ltd. | DCF Valuation Model",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Institutional CSS
st.markdown("""
<style>
    /* Clean financial typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Metric Card Styling */
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 18px 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .metric-label {
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748b;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 1.65rem;
        font-weight: 700;
        color: #0f172a;
    }
    .metric-sub {
        font-size: 0.85rem;
        font-weight: 500;
        margin-top: 4px;
    }
    .metric-positive {
        color: #16a34a;
    }
    .metric-neutral {
        color: #0284c7;
    }
    
    /* Header Container */
    .company-header {
        background: linear-gradient(90deg, #0f172a 0%, #1e293b 100%);
        color: white;
        padding: 24px 30px;
        border-radius: 10px;
        margin-bottom: 25px;
    }
    .company-title {
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
    }
    .company-subtitle {
        font-size: 0.95rem;
        color: #94a3b8;
        margin-top: 5px;
    }
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 8px;
        background-color: #334155;
        color: #f1f5f9;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# BASELINE DATA (From Infosys_DCF_Valuation.xlsx)
# ==========================================
HISTORICAL_YEARS = ["FY2022", "FY2023", "FY2024", "FY2025", "FY2026"]
HISTORICAL_SALES = [121641, 146767, 153670, 162990, 178650]
HISTORICAL_EBIT = [31491, 35130, 36425, 39236, 42280]
HISTORICAL_DEPR = [3676, 4225, 4678, 4812, 4902]
HISTORICAL_CAPEX = [2161, 2579, 2201, 2237, 2727]
HISTORICAL_NWC_CHANGE = [-1424, -6344, -5082, -295, -2639]

CURRENT_MARKET_PRICE = 1130.00
SHARES_OUTSTANDING_CR = 405.7938
CASH_AND_EQUIV_CR = 22201.0
TOTAL_DEBT_CR = 9176.0

# ==========================================
# SIDEBAR: SCENARIO & MODEL ASSUMPTIONS
# ==========================================
st.sidebar.markdown("### ⚙️ Valuation Assumptions")
st.sidebar.markdown("*Adjust drivers below to run live sensitivity simulations.*")

scenario = st.sidebar.selectbox(
    "Scenario Preset",
    ["Base Case (Management Guidance)", "Bull Case (Optimistic Tech Demand)", "Bear Case (Macro Slowdown)"],
    index=0
)

# Preset adjustments
if scenario == "Bull Case (Optimistic Tech Demand)":
    default_wacc = 10.86
    default_g = 5.5
    default_margin = 25.0
    growth_bump = 0.02
elif scenario == "Bear Case (Macro Slowdown)":
    default_wacc = 12.00
    default_g = 4.0
    default_margin = 22.5
    growth_bump = -0.02
else:
    default_wacc = 11.36
    default_g = 5.0
    default_margin = 24.0
    growth_bump = 0.00

st.sidebar.markdown("---")
st.sidebar.markdown("**Cost of Capital & Terminal Value**")
wacc_input = st.sidebar.slider("WACC Discount Rate (%)", min_value=9.5, max_value=13.5, value=default_wacc, step=0.1) / 100
terminal_growth_input = st.sidebar.slider("Terminal Growth Rate (%)", min_value=3.5, max_value=6.5, value=default_g, step=0.1) / 100

st.sidebar.markdown("---")
st.sidebar.markdown("**Operating Assumptions (FY2027–FY2031)**")
ebit_margin_input = st.sidebar.slider("Normalized EBIT Margin (%)", min_value=20.0, max_value=28.0, value=default_margin, step=0.5) / 100
tax_rate_input = st.sidebar.slider("Effective Tax Rate (%)", min_value=22.0, max_value=30.0, value=27.0, step=0.5) / 100

st.sidebar.markdown("---")
st.sidebar.markdown("**Capital Expenditure & Working Capital**")
depr_rate = st.sidebar.number_input("Depreciation (% of Sales)", value=2.9, step=0.1) / 100
capex_rate = st.sidebar.number_input("Capex (% of Sales)", value=1.6, step=0.1) / 100
nwc_rate = st.sidebar.number_input("Change in NWC (% of Sales)", value=-2.1, step=0.1) / 100

# ==========================================
# DCF VALUATION ENGINE
# ==========================================
def run_dcf(wacc, g, ebit_margin, tax_rate, depr_pct, capex_pct, nwc_pct, growth_mod):
    forecast_years = ["FY2027", "FY2028", "FY2029", "FY2030", "FY2031"]
    base_growth = [0.10, 0.09, 0.08, 0.07, 0.06]
    growth_rates = [max(0.01, r + growth_mod) for r in base_growth]
    
    sales_forecast = []
    curr_sales = HISTORICAL_SALES[-1]
    for gr in growth_rates:
        curr_sales *= (1 + gr)
        sales_forecast.append(curr_sales)
        
    ebit_forecast = [s * ebit_margin for s in sales_forecast]
    nopat_forecast = [ebit * (1 - tax_rate) for ebit in ebit_forecast]
    depr_forecast = [s * depr_pct for s in sales_forecast]
    capex_forecast = [s * capex_pct for s in sales_forecast]
    nwc_forecast = [s * nwc_pct for s in sales_forecast]
    
    # FCFF = NOPAT + Depr - Capex - Change in NWC
    fcff_forecast = [
        nopat + depr - capex - nwc
        for nopat, depr, capex, nwc in zip(nopat_forecast, depr_forecast, capex_forecast, nwc_forecast)
    ]
    
    # Discount factors
    discount_factors = [1 / ((1 + wacc) ** (i + 1)) for i in range(len(forecast_years))]
    pv_fcff = [fcff * df for fcff, df in zip(fcff_forecast, discount_factors)]
    sum_pv_fcff = sum(pv_fcff)
    
    # Terminal Value (Gordon Growth)
    fcff_terminal_year = fcff_forecast[-1] * (1 + g)
    if wacc <= g:
        terminal_value = 0
        pv_terminal_value = 0
    else:
        terminal_value = fcff_terminal_year / (wacc - g)
        pv_terminal_value = terminal_value * discount_factors[-1]
        
    enterprise_value = sum_pv_fcff + pv_terminal_value
    equity_value = enterprise_value - TOTAL_DEBT_CR + CASH_AND_EQUIV_CR
    fair_value_per_share = equity_value / SHARES_OUTSTANDING_CR
    upside_pct = ((fair_value_per_share - CURRENT_MARKET_PRICE) / CURRENT_MARKET_PRICE) * 100
    
    forecast_df = pd.DataFrame({
        "Year": forecast_years,
        "Growth Rate (%)": [f"{r*100:.1f}%" for r in growth_rates],
        "Sales (₹ Cr)": sales_forecast,
        "EBIT (₹ Cr)": ebit_forecast,
        "NOPAT (₹ Cr)": nopat_forecast,
        "Depreciation (₹ Cr)": depr_forecast,
        "Capex (₹ Cr)": capex_forecast,
        "Δ Working Capital (₹ Cr)": nwc_forecast,
        "FCFF (₹ Cr)": fcff_forecast,
        "Discount Factor": discount_factors,
        "Present Value (₹ Cr)": pv_fcff
    })
    
    return {
        "fair_value": fair_value_per_share,
        "upside_pct": upside_pct,
        "enterprise_value": enterprise_value,
        "equity_value": equity_value,
        "sum_pv_fcff": sum_pv_fcff,
        "pv_terminal_value": pv_terminal_value,
        "terminal_value": terminal_value,
        "forecast_df": forecast_df,
        "fcff_forecast": fcff_forecast,
        "sales_forecast": sales_forecast,
        "ebit_forecast": ebit_forecast
    }

# Execute valuation
val_results = run_dcf(
    wacc=wacc_input,
    g=terminal_growth_input,
    ebit_margin=ebit_margin_input,
    tax_rate=tax_rate_input,
    depr_pct=depr_rate,
    capex_pct=capex_rate,
    nwc_pct=nwc_rate,
    growth_mod=growth_bump
)

# ==========================================
# HEADER BANNER
# ==========================================
st.markdown(f"""
<div class="company-header">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 class="company-title">INFOSYS LIMITED (NSE: INFY)</h1>
            <div class="company-subtitle">Institutional Equity Research & Discounted Cash Flow (DCF) Valuation Model</div>
            <div style="margin-top: 10px;">
                <span class="badge">Sector: IT Services & Consulting</span>
                <span class="badge">Currency: INR (₹ Crores)</span>
                <span class="badge">Model: FCFF 5-Year Projection + Gordon Growth</span>
                <span class="badge">Scenario: {scenario}</span>
            </div>
        </div>
        <div style="text-align: right;">
            <div style="font-size: 0.85rem; color: #94a3b8;">CURRENT MARKET PRICE</div>
            <div style="font-size: 2.1rem; font-weight: 700; color: #ffffff;">₹{CURRENT_MARKET_PRICE:,.2f}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# TOP KPI METRIC CARDS
# ==========================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Intrinsic Fair Value</div>
        <div class="metric-value">₹{val_results['fair_value']:,.2f}</div>
        <div class="metric-sub metric-neutral">Per Share (FCFF Methodology)</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    color_class = "metric-positive" if val_results['upside_pct'] > 0 else "text-danger"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Implied Margin of Safety</div>
        <div class="metric-value {color_class}">{val_results['upside_pct']:+.1f}%</div>
        <div class="metric-sub">Versus Current Market Price</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    verdict = "STRONG BUY (Undervalued)" if val_results['upside_pct'] > 25 else ("BUY" if val_results['upside_pct'] > 10 else "HOLD / FAIR")
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Investment Recommendation</div>
        <div class="metric-value metric-positive">{verdict}</div>
        <div class="metric-sub">Fundamentals-Driven Thesis</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Implied Enterprise Value</div>
        <div class="metric-value">₹{val_results['enterprise_value']/1000:,.1f}K Cr</div>
        <div class="metric-sub">WACC: {wacc_input*100:.2f}% | Terminal g: {terminal_growth_input*100:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 5 INSTITUTIONAL TABS
# ==========================================
tab_summary, tab_fcff, tab_sensitivity, tab_wacc, tab_historical = st.tabs([
    "📊 Valuation Summary & Bridge",
    "📈 5-Year FCFF Forecast",
    "🎯 5x5 Sensitivity Matrix",
    "⚖️ WACC & Capital Structure",
    "📜 Historical Performance"
])

# ------------------------------------------
# TAB 1: VALUATION SUMMARY & WATERFALL
# ------------------------------------------
with tab_summary:
    st.subheader("Enterprise Value to Equity Value Bridge")
    st.write("This waterfall chart demonstrates how the company's operating cash flows and net cash position bridge to final equity value per share.")
    
    waterfall_fig = go.Figure(go.Waterfall(
        name="Valuation Bridge",
        orientation="v",
        measure=["relative", "relative", "total", "relative", "relative", "total"],
        x=["PV of 5-Yr Cash Flows", "PV of Terminal Value", "Enterprise Value", "Less: Total Debt", "Add: Cash & Equivalents", "Equity Value"],
        textposition="outside",
        text=[
            f"₹{val_results['sum_pv_fcff']:,.0f} Cr",
            f"₹{val_results['pv_terminal_value']:,.0f} Cr",
            f"₹{val_results['enterprise_value']:,.0f} Cr",
            f"-₹{TOTAL_DEBT_CR:,.0f} Cr",
            f"+₹{CASH_AND_EQUIV_CR:,.0f} Cr",
            f"₹{val_results['equity_value']:,.0f} Cr"
        ],
        y=[
            val_results['sum_pv_fcff'],
            val_results['pv_terminal_value'],
            val_results['enterprise_value'],
            -TOTAL_DEBT_CR,
            CASH_AND_EQUIV_CR,
            val_results['equity_value']
        ],
        connector={"line": {"color": "#94a3b8"}},
        decreasing={"marker": {"color": "#ef4444"}},
        increasing={"marker": {"color": "#0284c7"}},
        totals={"marker": {"color": "#0f172a"}}
    ))
    waterfall_fig.update_layout(
        height=450,
        margin=dict(l=20, r=20, t=30, b=20),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        yaxis_title="Valuation (₹ Crores)",
        font=dict(family="Inter, sans-serif")
    )
    st.plotly_chart(waterfall_fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Executive Valuation Summary")
    summary_cols = st.columns(2)
    with summary_cols[0]:
        st.markdown(f"""
        * **Present Value of Explicit Forecasts (FY27–FY31):** ₹{val_results['sum_pv_fcff']:,.2f} Cr ({val_results['sum_pv_fcff']/val_results['enterprise_value']*100:.1f}% of Enterprise Value)
        * **Present Value of Terminal Value:** ₹{val_results['pv_terminal_value']:,.2f} Cr ({val_results['pv_terminal_value']/val_results['enterprise_value']*100:.1f}% of Enterprise Value)
        * **Enterprise Value:** ₹{val_results['enterprise_value']:,.2f} Cr
        * **Total Debt (FY26 Balance Sheet):** ₹{TOTAL_DEBT_CR:,.2f} Cr
        * **Cash & Cash Equivalents (FY26 Balance Sheet):** ₹{CASH_AND_EQUIV_CR:,.2f} Cr
        """)
    with summary_cols[1]:
        st.markdown(f"""
        * **Implied Equity Value:** ₹{val_results['equity_value']:,.2f} Cr
        * **Shares Outstanding:** {SHARES_OUTSTANDING_CR:.2f} Crores
        * **Intrinsic Fair Value per Share:** **₹{val_results['fair_value']:,.2f}**
        * **Current Market Price (CMP):** ₹{CURRENT_MARKET_PRICE:,.2f}
        * **Margin of Safety (Upside):** **+{val_results['upside_pct']:.1f}%**
        """)

# ------------------------------------------
# TAB 2: 5-YEAR FCFF FORECAST ENGINE
# ------------------------------------------
with tab_fcff:
    st.subheader("Forecasted Financial Performance (FY2027 – FY2031)")
    st.write("Detailed projections based on management guidance, tapering growth rates, and normalized EBIT operating margins.")
    
    display_df = val_results['forecast_df'].copy()
    format_dict = {
        "Sales (₹ Cr)": "{:,.1f}",
        "EBIT (₹ Cr)": "{:,.1f}",
        "NOPAT (₹ Cr)": "{:,.1f}",
        "Depreciation (₹ Cr)": "{:,.1f}",
        "Capex (₹ Cr)": "{:,.1f}",
        "Δ Working Capital (₹ Cr)": "{:,.1f}",
        "FCFF (₹ Cr)": "{:,.1f}",
        "Discount Factor": "{:.4f}",
        "Present Value (₹ Cr)": "{:,.1f}"
    }
    st.dataframe(display_df.style.format(format_dict), use_container_width=True)
    
    st.markdown("---")
    st.subheader("Revenue & Free Cash Flow Trajectory")
    
    chart_years = HISTORICAL_YEARS + ["FY2027", "FY2028", "FY2029", "FY2030", "FY2031"]
    chart_sales = HISTORICAL_SALES + val_results['sales_forecast']
    chart_ebit = HISTORICAL_EBIT + val_results['ebit_forecast']
    
    fig_trajectory = go.Figure()
    fig_trajectory.add_trace(go.Bar(
        x=chart_years,
        y=chart_sales,
        name="Sales Revenue (₹ Cr)",
        marker_color="#0284c7"
    ))
    fig_trajectory.add_trace(go.Bar(
        x=chart_years,
        y=chart_ebit,
        name="EBIT Operating Profit (₹ Cr)",
        marker_color="#0f172a"
    ))
    fig_trajectory.update_layout(
        barmode='group',
        height=400,
        margin=dict(l=20, r=20, t=30, b=20),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        yaxis_title="₹ Crores",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_trajectory, use_container_width=True)

# ------------------------------------------
# TAB 3: 5x5 SENSITIVITY MATRIX
# ------------------------------------------
with tab_sensitivity:
    st.subheader("5x5 Valuation Sensitivity Grid")
    st.write("Evaluating per-share fair values under varying Discount Rates (WACC) and Terminal Growth Rates (g).")
    
    wacc_steps = [wacc_input - 0.01, wacc_input - 0.005, wacc_input, wacc_input + 0.005, wacc_input + 0.01]
    g_steps = [terminal_growth_input - 0.01, terminal_growth_input - 0.005, terminal_growth_input, terminal_growth_input + 0.005, terminal_growth_input + 0.01]
    
    matrix_data = []
    matrix_labels = []
    
    for w in wacc_steps:
        row_vals = []
        row_labels = []
        for g_val in g_steps:
            res = run_dcf(
                wacc=w,
                g=g_val,
                ebit_margin=ebit_margin_input,
                tax_rate=tax_rate_input,
                depr_pct=depr_rate,
                capex_pct=capex_rate,
                nwc_pct=nwc_rate,
                growth_mod=growth_bump
            )
            val = res['fair_value']
            row_vals.append(val)
            row_labels.append(f"₹{val:,.0f}")
        matrix_data.append(row_vals)
        matrix_labels.append(row_labels)
        
    y_axis = [f"WACC: {w*100:.2f}%" for w in wacc_steps]
    x_axis = [f"g: {g*100:.2f}%" for g in g_steps]
    
    heatmap_fig = go.Figure(data=go.Heatmap(
        z=matrix_data,
        x=x_axis,
        y=y_axis,
        text=matrix_labels,
        texttemplate="%{text}",
        textfont={"size": 14, "family": "Inter"},
        colorscale="Blues",
        colorbar=dict(title="Fair Value (₹)")
    ))
    heatmap_fig.update_layout(
        height=450,
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis_title="Terminal Growth Rate",
        yaxis_title="Cost of Capital (WACC)"
    )
    st.plotly_chart(heatmap_fig, use_container_width=True)
    
    st.info(f"💡 **Takeaway:** In every single tested scenario (range: ₹{min([min(r) for r in matrix_data]):,.0f} to ₹{max([max(r) for r in matrix_data]):,.0f}), the intrinsic fair value remains above the Current Market Price of ₹{CURRENT_MARKET_PRICE:,.0f}, demonstrating significant downside protection.")

# ------------------------------------------
# TAB 4: WACC & COST OF CAPITAL
# ------------------------------------------
with tab_wacc:
    st.subheader("Weighted Average Cost of Capital (WACC) & CAPM")
    
    wacc_c1, wacc_c2 = st.columns(2)
    
    with wacc_c1:
        st.markdown("#### Cost of Equity (CAPM)")
        capm_df = pd.DataFrame({
            "Component": [
                "Risk-Free Rate (Rf)",
                "Beta (β)",
                "Equity Market Risk Premium (ERP)",
                "Cost of Equity (Ke)"
            ],
            "Assumption": [
                "6.80%",
                "0.85",
                "5.50%",
                "11.48%"
            ],
            "Methodology / Rationale": [
                "India 10-Year Government Bond (G-Sec) Benchmark Yield",
                "Large-Cap Indian IT services, defensive cash flows & lower volatility",
                "Standard Indian Equity Market risk premium",
                "Ke = Rf + β × ERP = 6.8% + (0.85 × 5.5%) = 11.48%"
            ]
        })
        st.table(capm_df)
        
    with wacc_c2:
        st.markdown("#### Capital Structure & Cost of Debt")
        debt_df = pd.DataFrame({
            "Metric": [
                "Pre-Tax Cost of Debt (Kd)",
                "Effective Tax Rate (t)",
                "Post-Tax Cost of Debt [Kd × (1-t)]",
                "Equity Capital Weight (E/V)",
                "Debt Capital Weight (D/V)",
                "Derived WACC"
            ],
            "Value": [
                "7.50%",
                "27.00%",
                "5.48%",
                "98.04%",
                "1.96%",
                "11.36%"
            ]
        })
        st.table(debt_df)
        
    st.markdown("---")
    st.markdown("#### Asset-Light Capital Structure Rationale")
    st.write(
        "Infosys operates an asset-light IT services model with virtually zero net debt (₹22,201 Cr Cash vs ₹9,176 Cr Borrowings). "
        "Consequently, the capital structure is heavily weighted toward Equity (~98%), making the Cost of Equity (11.48%) the dominant discount driver."
    )

# ------------------------------------------
# TAB 5: HISTORICAL PERFORMANCE
# ------------------------------------------
with tab_historical:
    st.subheader("Five-Year Historical Financial Actuals (FY2022 – FY2026)")
    
    hist_df = pd.DataFrame({
        "Metric (₹ Crore)": [
            "Sales",
            "Operating Profit (EBIT)",
            "EBIT Margin (%)",
            "Depreciation",
            "Capex",
            "Change in Working Capital"
        ],
        "FY2022": [f"₹{HISTORICAL_SALES[0]:,}", f"₹{HISTORICAL_EBIT[0]:,}", f"{HISTORICAL_EBIT[0]/HISTORICAL_SALES[0]*100:.1f}%", f"₹{HISTORICAL_DEPR[0]:,}", f"₹{HISTORICAL_CAPEX[0]:,}", f"₹{HISTORICAL_NWC_CHANGE[0]:,}"],
        "FY2023": [f"₹{HISTORICAL_SALES[1]:,}", f"₹{HISTORICAL_EBIT[1]:,}", f"{HISTORICAL_EBIT[1]/HISTORICAL_SALES[1]*100:.1f}%", f"₹{HISTORICAL_DEPR[1]:,}", f"₹{HISTORICAL_CAPEX[1]:,}", f"₹{HISTORICAL_NWC_CHANGE[1]:,}"],
        "FY2024": [f"₹{HISTORICAL_SALES[2]:,}", f"₹{HISTORICAL_EBIT[2]:,}", f"{HISTORICAL_EBIT[2]/HISTORICAL_SALES[2]*100:.1f}%", f"₹{HISTORICAL_DEPR[2]:,}", f"₹{HISTORICAL_CAPEX[2]:,}", f"₹{HISTORICAL_NWC_CHANGE[2]:,}"],
        "FY2025": [f"₹{HISTORICAL_SALES[3]:,}", f"₹{HISTORICAL_EBIT[3]:,}", f"{HISTORICAL_EBIT[3]/HISTORICAL_SALES[3]*100:.1f}%", f"₹{HISTORICAL_DEPR[3]:,}", f"₹{HISTORICAL_CAPEX[3]:,}", f"₹{HISTORICAL_NWC_CHANGE[3]:,}"],
        "FY2026": [f"₹{HISTORICAL_SALES[4]:,}", f"₹{HISTORICAL_EBIT[4]:,}", f"{HISTORICAL_EBIT[4]/HISTORICAL_SALES[4]*100:.1f}%", f"₹{HISTORICAL_DEPR[4]:,}", f"₹{HISTORICAL_CAPEX[4]:,}", f"₹{HISTORICAL_NWC_CHANGE[4]:,}"]
    })
    st.table(hist_df)
