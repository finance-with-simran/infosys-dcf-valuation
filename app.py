import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime

# ==========================================
# PAGE CONFIGURATION (Institutional Theme)
# ==========================================
st.set_page_config(
    page_title="Infosys Ltd. | DCF Valuation & Market Terminal",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Institutional CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 14px 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }
    .metric-label {
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748b;
        margin-bottom: 3px;
    }
    .metric-value {
        font-size: 1.45rem;
        font-weight: 700;
        color: #0f172a;
    }
    .metric-sub {
        font-size: 0.78rem;
        font-weight: 500;
        margin-top: 2px;
    }
    .metric-positive {
        color: #16a34a;
    }
    .metric-neutral {
        color: #0284c7;
    }
    
    .company-header {
        background: linear-gradient(90deg, #0f172a 0%, #1e293b 100%);
        color: white;
        padding: 18px 24px;
        border-radius: 8px;
        margin-bottom: 18px;
    }
    .company-title {
        font-size: 1.6rem;
        font-weight: 700;
        margin: 0;
    }
    .company-subtitle {
        font-size: 0.88rem;
        color: #94a3b8;
        margin-top: 3px;
    }
    .badge {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 0.72rem;
        font-weight: 600;
        margin-right: 6px;
        background-color: #334155;
        color: #f1f5f9;
    }
    
    .section-box {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 18px;
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
st.sidebar.markdown("### ⚙️ Valuation Drivers")
st.sidebar.markdown("*Adjust drivers below to run live simulations.*")

scenario = st.sidebar.selectbox(
    "Scenario Preset",
    ["Base Case (Management Guidance)", "Bull Case (Optimistic Tech Demand)", "Bear Case (Macro Slowdown)"],
    index=0
)

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
st.sidebar.markdown("**Cost of Capital & Terminal Growth**")
wacc_input = st.sidebar.slider("WACC Discount Rate (%)", min_value=9.5, max_value=13.5, value=default_wacc, step=0.1) / 100
terminal_growth_input = st.sidebar.slider("Terminal Growth Rate (%)", min_value=3.5, max_value=6.5, value=default_g, step=0.1) / 100

st.sidebar.markdown("---")
st.sidebar.markdown("**Operating Assumptions**")
ebit_margin_input = st.sidebar.slider("Normalized EBIT Margin (%)", min_value=20.0, max_value=28.0, value=default_margin, step=0.5) / 100
tax_rate_input = st.sidebar.slider("Effective Tax Rate (%)", min_value=22.0, max_value=30.0, value=27.0, step=0.5) / 100

depr_rate = 2.9 / 100
capex_rate = 1.6 / 100
nwc_rate = -2.1 / 100

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
    
    fcff_forecast = [
        nopat + depr - capex - nwc
        for nopat, depr, capex, nwc in zip(nopat_forecast, depr_forecast, capex_forecast, nwc_forecast)
    ]
    
    discount_factors = [1 / ((1 + wacc) ** (i + 1)) for i in range(len(forecast_years))]
    pv_fcff = [fcff * df for fcff, df in zip(fcff_forecast, discount_factors)]
    sum_pv_fcff = sum(pv_fcff)
    
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
        "Growth (%)": [f"{r*100:.1f}%" for r in growth_rates],
        "Sales (₹ Cr)": sales_forecast,
        "EBIT (₹ Cr)": ebit_forecast,
        "NOPAT (₹ Cr)": nopat_forecast,
        "Depreciation (₹ Cr)": depr_forecast,
        "Capex (₹ Cr)": capex_forecast,
        "Δ NWC (₹ Cr)": nwc_forecast,
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
        "forecast_df": forecast_df
    }

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
# 1. HEADER BANNER
# ==========================================
st.markdown(f"""
<div class="company-header">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 class="company-title">INFOSYS LIMITED (NSE: INFY)</h1>
            <div class="company-subtitle">DCF Valuation Model & Interactive Market Terminal</div>
            <div style="margin-top: 8px;">
                <span class="badge">Sector: IT Services</span>
                <span class="badge">Currency: INR (₹ Crores)</span>
                <span class="badge">Model: FCFF + Gordon Growth</span>
                <span class="badge">Scenario: {scenario}</span>
            </div>
        </div>
        <div style="text-align: right;">
            <div style="font-size: 0.8rem; color: #94a3b8;">CURRENT MARKET PRICE</div>
            <div style="font-size: 1.9rem; font-weight: 700; color: #ffffff;">₹{CURRENT_MARKET_PRICE:,.2f}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 2. TOP KPI CARDS
# ==========================================
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Intrinsic Fair Value</div>
        <div class="metric-value">₹{val_results['fair_value']:,.2f}</div>
        <div class="metric-sub metric-neutral">Per Share (DCF Engine)</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    color_class = "metric-positive" if val_results['upside_pct'] > 0 else "text-danger"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Margin of Safety</div>
        <div class="metric-value {color_class}">{val_results['upside_pct']:+.1f}%</div>
        <div class="metric-sub">Versus CMP ₹{CURRENT_MARKET_PRICE:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    verdict = "STRONG BUY" if val_results['upside_pct'] > 25 else ("BUY" if val_results['upside_pct'] > 10 else "HOLD")
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Recommendation</div>
        <div class="metric-value metric-positive">{verdict}</div>
        <div class="metric-sub">Fundamentals-Driven</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Enterprise Value</div>
        <div class="metric-value">₹{val_results['enterprise_value']/1000:,.1f}K Cr</div>
        <div class="metric-sub">WACC: {wacc_input*100:.2f}% | g: {terminal_growth_input*100:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 3. UNIFIED VISUAL COMMAND CENTER
# (TradingView Candlestick Chart + Valuation Waterfall Bridge together!)
# ==========================================
col_left, col_right = st.columns([1.2, 1.0])

# --- LEFT: TRADINGVIEW CANDLESTICK CHART ---
with col_left:
    st.markdown("#### 🕯️ Market Trading Chart vs. DCF Fair Value")
    
    @st.cache_data(ttl=3600)
    def fetch_stock_data():
        try:
            import yfinance as yf
            ticker = yf.Ticker("INFY.NS")
            df = ticker.history(period="1y").reset_index()
            if df.empty:
                raise ValueError("No data")
            return df
        except Exception:
            dates = pd.date_range(end=datetime.date.today(), periods=250, freq='B')
            base = 1050 + np.cumsum(np.random.randn(250) * 8)
            return pd.DataFrame({
                "Date": dates,
                "Open": base - 3,
                "High": base + 7,
                "Low": base - 6,
                "Close": base,
                "Volume": np.random.randint(5000000, 15000000, size=250)
            })

    stock_df = fetch_stock_data()
    stock_df['MA50'] = stock_df['Close'].rolling(50).mean()
    stock_df['MA200'] = stock_df['Close'].rolling(200).mean()

    candle_fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.04,
        row_heights=[0.72, 0.28]
    )

    candle_fig.add_trace(go.Candlestick(
        x=stock_df['Date'],
        open=stock_df['Open'], high=stock_df['High'], low=stock_df['Low'], close=stock_df['Close'],
        name="INFY.NS",
        increasing_line_color="#22c55e", decreasing_line_color="#ef4444"
    ), row=1, col=1)

    candle_fig.add_trace(go.Scatter(
        x=stock_df['Date'], y=stock_df['MA50'],
        name="50-Day SMA",
        line=dict(color="#38bdf8", width=1.5)
    ), row=1, col=1)

    candle_fig.add_trace(go.Scatter(
        x=stock_df['Date'], y=stock_df['MA200'],
        name="200-Day SMA",
        line=dict(color="#f97316", width=1.5)
    ), row=1, col=1)

    # Gold Fair Value Target Line
    candle_fig.add_hline(
        y=val_results['fair_value'],
        line_dash="dash",
        line_color="#eab308",
        line_width=2.5,
        annotation_text=f"DCF Fair Value: ₹{val_results['fair_value']:,.0f}",
        annotation_position="top right",
        annotation_font_color="#eab308",
        row=1, col=1
    )

    # CMP Anchor
    candle_fig.add_hline(
        y=CURRENT_MARKET_PRICE,
        line_dash="dot",
        line_color="#94a3b8",
        annotation_text=f"CMP: ₹{CURRENT_MARKET_PRICE:,.0f}",
        annotation_position="bottom right",
        row=1, col=1
    )

    vol_colors = ["#22c55e" if c >= o else "#ef4444" for c, o in zip(stock_df['Close'], stock_df['Open'])]
    candle_fig.add_trace(go.Bar(
        x=stock_df['Date'], y=stock_df['Volume'],
        name="Volume",
        marker_color=vol_colors,
        opacity=0.65
    ), row=2, col=1)

    candle_fig.update_layout(
        height=480,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis_rangeslider_visible=False,
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        yaxis_title="Price (₹)",
        yaxis2_title="Vol",
        font=dict(family="Inter, sans-serif"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(candle_fig, use_container_width=True)

# --- RIGHT: ENTERPRISE TO EQUITY VALUE WATERFALL BRIDGE ---
with col_right:
    st.markdown("#### 📊 Enterprise Value to Equity Value Bridge")
    
    waterfall_fig = go.Figure(go.Waterfall(
        name="Valuation Bridge",
        orientation="v",
        measure=["relative", "relative", "total", "relative", "relative", "total"],
        x=["PV Cash Flows", "PV Terminal Val", "Enterprise Val", "Less: Debt", "Add: Cash", "Equity Value"],
        textposition="outside",
        text=[
            f"₹{val_results['sum_pv_fcff']/1000:,.0f}K",
            f"₹{val_results['pv_terminal_value']/1000:,.0f}K",
            f"₹{val_results['enterprise_value']/1000:,.0f}K",
            f"-₹{TOTAL_DEBT_CR/1000:,.1f}K",
            f"+₹{CASH_AND_EQUIV_CR/1000:,.1f}K",
            f"₹{val_results['equity_value']/1000:,.0f}K"
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
        height=480,
        margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        yaxis_title="₹ Crores",
        font=dict(family="Inter, sans-serif")
    )
    st.plotly_chart(waterfall_fig, use_container_width=True)

st.markdown("---")

# ==========================================
# 4. LOWER SECTION: DETAILED TABLES & SENSITIVITY
# ==========================================
col_sec1, col_sec2 = st.columns([1.1, 1.0])

with col_sec1:
    st.markdown("#### 📈 5-Year Forecast Schedule (FY2027–FY2031)")
    display_df = val_results['forecast_df'].copy()
    format_dict = {
        "Sales (₹ Cr)": "{:,.0f}",
        "EBIT (₹ Cr)": "{:,.0f}",
        "NOPAT (₹ Cr)": "{:,.0f}",
        "Depreciation (₹ Cr)": "{:,.0f}",
        "Capex (₹ Cr)": "{:,.0f}",
        "Δ NWC (₹ Cr)": "{:,.0f}",
        "FCFF (₹ Cr)": "{:,.0f}",
        "Discount Factor": "{:.4f}",
        "Present Value (₹ Cr)": "{:,.0f}"
    }
    st.dataframe(display_df.style.format(format_dict), use_container_width=True, height=230)

with col_sec2:
    st.markdown("#### 🎯 5x5 Valuation Sensitivity Grid (Fair Value ₹)")
    wacc_steps = [wacc_input - 0.01, wacc_input - 0.005, wacc_input, wacc_input + 0.005, wacc_input + 0.01]
    g_steps = [terminal_growth_input - 0.01, terminal_growth_input - 0.005, terminal_growth_input, terminal_growth_input + 0.005, terminal_growth_input + 0.01]
    
    matrix_data = []
    matrix_labels = []
    for w in wacc_steps:
        row_vals = []
        row_labels = []
        for g_val in g_steps:
            res = run_dcf(w, g_val, ebit_margin_input, tax_rate_input, depr_rate, capex_rate, nwc_rate, growth_bump)
            row_vals.append(res['fair_value'])
            row_labels.append(f"₹{res['fair_value']:,.0f}")
        matrix_data.append(row_vals)
        matrix_labels.append(row_labels)
        
    y_axis = [f"WACC: {w*100:.1f}%" for w in wacc_steps]
    x_axis = [f"g: {g*100:.1f}%" for g in g_steps]
    
    heatmap_fig = go.Figure(data=go.Heatmap(
        z=matrix_data, x=x_axis, y=y_axis,
        text=matrix_labels, texttemplate="%{text}",
        textfont={"size": 13, "family": "Inter"},
        colorscale="Blues", showscale=False
    ))
    heatmap_fig.update_layout(
        height=230,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis_title="Terminal Growth Rate",
        yaxis_title="Discount Rate (WACC)"
    )
    st.plotly_chart(heatmap_fig, use_container_width=True)

# Final Capital Structure strip
st.markdown("---")
st.markdown(
    f"**Model Parameters:** Risk-Free Rate = 6.80% (10Y G-Sec) | Beta = 0.85 | Equity Risk Premium = 5.50% | "
    f"Cost of Equity = 11.48% | Capital Structure = 98.0% Equity / 2.0% Debt | WACC = {wacc_input*100:.2f}% | "
    f"Shares Outstanding = {SHARES_OUTSTANDING_CR:.2f} Cr"
)
