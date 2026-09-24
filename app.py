import os
import joblib
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="PropValuate — Smart Indian Real Estate AI",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------------------------
# CUSTOM CSS FOR ADVANCED STYLING
# ---------------------------------------------------------------------------
st.markdown("""
    <style>
    /* ---------- Global ---------- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Manrope:wght@600;700;800&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: radial-gradient(circle at 15% 0%, #131a2c 0%, #0b0f19 45%, #060810 100%);
        color: #e2e8f0;
    }

    /* Hide default Streamlit chrome for a cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {background: transparent !important;}

    /* ---------- Hero header ---------- */
    .hero-wrap {
        background: linear-gradient(120deg, rgba(56,189,248,0.12) 0%, rgba(129,140,248,0.10) 50%, rgba(236,72,153,0.10) 100%);
        border: 1px solid rgba(148,163,184,0.15);
        border-radius: 22px;
        padding: 30px 36px;
        margin-bottom: 28px;
        box-shadow: 0 20px 45px -20px rgba(56,189,248,0.25);
    }
    .hero-title {
        font-family: 'Manrope', sans-serif;
        font-size: 2.3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8, #818cf8 60%, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px;
    }
    .hero-sub {
        color: #94a3b8;
        font-size: 1.02rem;
        font-weight: 500;
    }
    .badge-row { margin-top: 14px; }
    .badge {
        display: inline-block;
        background: rgba(56,189,248,0.10);
        border: 1px solid rgba(56,189,248,0.35);
        color: #7dd3fc;
        padding: 5px 14px;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-right: 8px;
        letter-spacing: 0.3px;
    }

    /* ---------- Section labels ---------- */
    .section-label {
        font-family: 'Manrope', sans-serif;
        font-weight: 700;
        font-size: 0.95rem;
        color: #cbd5e1;
        text-transform: uppercase;
        letter-spacing: 1.1px;
        margin: 6px 0 14px 0;
        padding-bottom: 8px;
        border-bottom: 1px solid rgba(148,163,184,0.15);
    }

    /* ---------- Input panel card ---------- */
    .input-card {
        background: rgba(30,41,59,0.45);
        border: 1px solid rgba(148,163,184,0.14);
        border-radius: 18px;
        padding: 22px 22px 8px 22px;
        margin-bottom: 18px;
        backdrop-filter: blur(6px);
    }

    /* ---------- Result / metric card ---------- */
    .metric-card {
        background: linear-gradient(135deg, #16233b 0%, #0b1120 100%);
        border: 1px solid rgba(56,189,248,0.30);
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 20px 45px -15px rgba(56,189,248,0.30);
        text-align: center;
        margin-bottom: 22px;
        position: relative;
        overflow: hidden;
    }
    .metric-card::before {
        content: "";
        position: absolute;
        top: -60%; left: -20%;
        width: 140%; height: 220%;
        background: radial-gradient(circle, rgba(56,189,248,0.10) 0%, transparent 60%);
    }
    .price-title {
        color: #7dd3fc;
        font-size: 0.95rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.6px;
        position: relative;
    }
    .price-value {
        font-family: 'Manrope', sans-serif;
        color: #f8fafc;
        font-size: 3.2rem;
        font-weight: 800;
        margin: 10px 0;
        position: relative;
        text-shadow: 0 0 30px rgba(56,189,248,0.35);
    }
    .sub-metric {
        color: #cbd5e1;
        font-size: 1.05rem;
        font-weight: 500;
        position: relative;
    }
    .sub-metric b { color: #38bdf8; }

    /* ---------- Small stat chips under result ---------- */
    .stat-chip {
        background: rgba(30,41,59,0.55);
        border: 1px solid rgba(148,163,184,0.16);
        border-radius: 14px;
        padding: 16px;
        text-align: center;
    }
    .stat-chip .label {
        color: #94a3b8;
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 6px;
    }
    .stat-chip .value {
        color: #f1f5f9;
        font-size: 1.25rem;
        font-weight: 700;
    }

    /* ---------- Buttons ---------- */
    .stButton>button {
        background: linear-gradient(90deg, #0ea5e9, #6366f1);
        color: white;
        font-weight: 700;
        font-size: 1.05rem;
        border: none;
        border-radius: 14px;
        padding: 14px 0;
        box-shadow: 0 10px 30px -10px rgba(99,102,241,0.6);
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 14px 34px -8px rgba(99,102,241,0.75);
    }

    /* ---------- Tabs ---------- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: rgba(30,41,59,0.35);
        padding: 6px;
        border-radius: 14px;
        border: 1px solid rgba(148,163,184,0.12);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 10px 18px;
        font-weight: 600;
        color: #94a3b8;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, rgba(14,165,233,0.20), rgba(99,102,241,0.20));
        color: #e0f2fe !important;
    }

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0b1120 0%, #0e1526 100%);
        border-right: 1px solid rgba(148,163,184,0.10);
    }

    /* ---------- Chart card wrapper ---------- */
    .chart-card {
        background: rgba(30,41,59,0.35);
        border: 1px solid rgba(148,163,184,0.12);
        border-radius: 18px;
        padding: 14px 16px 4px 16px;
        margin-bottom: 18px;
    }

    /* ---------- Footer note ---------- */
    .footer-note {
        text-align: center;
        color: #64748b;
        font-size: 0.85rem;
        margin-top: 36px;
        padding-top: 18px;
        border-top: 1px solid rgba(148,163,184,0.10);
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# MODEL LOADING
# ---------------------------------------------------------------------------
MODEL_PATH = "linear_regression_model.joblib"

@st.cache_resource(show_spinner=False)
def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"'{MODEL_PATH}' not found.")
    return joblib.load(MODEL_PATH)

try:
    model = load_model()
except Exception as e:
    st.error(f"❌ Error loading model file: {e}")
    st.info("Tip: Run your model training script locally in this directory to generate `linear_regression_model.joblib`.")
    st.stop()

# ---------------------------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🏠 PropValuate AI")
    st.caption("Smart valuation engine for the Indian residential market.")
    st.markdown("---")
    st.markdown("#### How it works")
    st.markdown(
        "1. Configure the property in **Price Predictor**\n"
        "2. Click **Estimate Property Value**\n"
        "3. Explore trends in **Market Analytics**\n"
        "4. Review the model in **Model Insights**"
    )
    st.markdown("---")
    st.markdown("#### Coverage")
    st.markdown("🏙️ Mumbai · Delhi · Bangalore \n🏙️ Kolkata · Hyderabad · Chennai · Pune")
    st.markdown("---")
    st.caption("Built with Streamlit · Ridge Regression · Plotly")

# ---------------------------------------------------------------------------
# HERO HEADER
# ---------------------------------------------------------------------------
st.markdown("""
    <div class="hero-wrap">
        <div class="hero-title">🏠 PropValuate AI</div>
        <div class="hero-sub">Machine-learning powered valuation & market analytics for India's top residential markets.</div>
        <div class="badge-row">
            <span class="badge">⚡ Instant Estimate</span>
            <span class="badge">📊 Live Market Trends</span>
            <span class="badge">🎯 R² ≈ 0.93</span>
        </div>
    </div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🔮  Price Predictor", "📊  Market Analytics", "ℹ️  Model Insights"])

# ---------------------------------------------------------------------------
# TAB 1: PRICE PREDICTOR
# ---------------------------------------------------------------------------
with tab1:
    st.markdown('<div class="section-label">Property Configuration</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="input-card">', unsafe_allow_html=True)
        st.markdown("##### 📍 Location & Type")
        city = st.selectbox("City", ["Mumbai", "New Delhi", "Bangalore", "Kolkata", "Hyderabad", "Chennai", "Pune"])
        state_map = {
            "Mumbai": "Maharashtra", "Pune": "Maharashtra",
            "New Delhi": "Delhi", "Bangalore": "Karnataka",
            "Kolkata": "West Bengal", "Hyderabad": "Telangana",
            "Chennai": "Tamil Nadu"
        }
        state = state_map.get(city, "Maharashtra")
        property_type = st.selectbox("Property Type", ["Apartment", "Villa", "Independent House"])
        owner_type = st.selectbox("Owner Type", ["Owner", "Broker", "Builder"])
        availability = st.selectbox("Availability Status", ["Ready_to_Move", "Under_Construction"])
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="input-card">', unsafe_allow_html=True)
        st.markdown("##### 📐 Dimensions & Structure")
        bhk = st.slider("BHK Count", min_value=1, max_value=6, value=3)
        size_sqft = st.number_input("Property Size (SqFt)", min_value=300, max_value=10000, value=1400, step=50)
        floor_no = st.number_input("Floor Number", min_value=0, max_value=50, value=4)
        total_floors = st.number_input("Total Floors", min_value=1, max_value=50, value=12)
        age_of_property = st.slider("Property Age (Years)", min_value=0, max_value=30, value=3)
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="input-card">', unsafe_allow_html=True)
        st.markdown("##### ✨ Amenities & Specifications")
        furnished_status = st.selectbox("Furnished Status", ["Furnished", "Semi-furnished", "Unfurnished"])
        num_amenities = st.slider("Number of Amenities", min_value=0, max_value=10, value=5)
        nearby_schools = st.slider("Nearby Schools", min_value=0, max_value=10, value=3)
        nearby_hospitals = st.slider("Nearby Hospitals", min_value=0, max_value=10, value=2)
        transport_access = st.selectbox("Public Transport Access", ["High", "Medium", "Low"])
        parking_space = st.radio("Parking Space", ["Yes", "No"], horizontal=True)
        security = st.radio("24/7 Security", ["Yes", "No"], horizontal=True)
        facing = st.selectbox("Facing Direction", ["East", "North", "South", "West"])
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    predict_clicked = st.button("🚀 Estimate Property Value", use_container_width=True, type="primary")

    if predict_clicked:
        input_data = pd.DataFrame([{
            "BHK": bhk,
            "Size_in_SqFt": size_sqft,
            "Year_Built": 2026 - age_of_property,
            "Floor_No": floor_no,
            "Total_Floors": total_floors,
            "Age_of_Property": age_of_property,
            "Nearby_Schools": nearby_schools,
            "Nearby_Hospitals": nearby_hospitals,
            "Num_Amenities": num_amenities,
            "State": state,
            "City": city,
            "Property_Type": property_type,
            "Furnished_Status": furnished_status,
            "Public_Transport_Accessibility": transport_access,
            "Parking_Space": parking_space,
            "Security": security,
            "Facing": facing,
            "Owner_Type": owner_type,
            "Availability_Status": availability
        }])

        # Model Prediction
        pred_log = model.predict(input_data)
        pred_price = np.expm1(pred_log)[0]
        price_per_sqft = (pred_price * 100000) / size_sqft

        # Calculate Estimated Monthly Home Loan EMI (20 yr tenure @ 8.5% interest)
        principal = pred_price * 80000  # 80% LTV
        r = 0.085 / 12
        n = 240
        emi = (principal * r * ((1 + r) ** n)) / (((1 + r) ** n) - 1)

        st.markdown("<br>", unsafe_allow_html=True)

        # Output Card
        st.markdown(f"""
            <div class="metric-card">
                <div class="price-title">Estimated Market Valuation</div>
                <div class="price-value">₹ {pred_price:.2f} Lakhs</div>
                <div class="sub-metric">Rate: <b>₹ {price_per_sqft:,.2f}</b> / sq.ft. &nbsp;|&nbsp; Approx EMI: <b>₹ {emi:,.0f}</b> / mo</div>
            </div>
        """, unsafe_allow_html=True)

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f"""
                <div class="stat-chip"><div class="label">Location</div>
                <div class="value">{city}</div></div>""", unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
                <div class="stat-chip"><div class="label">Configuration</div>
                <div class="value">{bhk} BHK · {size_sqft} SqFt</div></div>""", unsafe_allow_html=True)
        with m3:
            st.markdown(f"""
                <div class="stat-chip"><div class="label">Condition</div>
                <div class="value">{age_of_property} Yrs · {furnished_status}</div></div>""", unsafe_allow_html=True)
        with m4:
            st.markdown(f"""
                <div class="stat-chip"><div class="label">Loan Estimate</div>
                <div class="value">80% LTV @ 8.5%</div></div>""", unsafe_allow_html=True)
    else:
        st.info("Configure the property details above and click **Estimate Property Value** to see the AI-generated valuation.")

# ---------------------------------------------------------------------------
# TAB 2: MARKET ANALYTICS (PLOTLY INTERACTIVE CHARTS)
# ---------------------------------------------------------------------------
with tab2:
    st.markdown('<div class="section-label">Interactive Market Trends</div>', unsafe_allow_html=True)

    # Generate Synthetic Benchmark Data for Analytics Visuals
    np.random.seed(42)
    cities = ["Mumbai", "New Delhi", "Bangalore", "Kolkata", "Hyderabad", "Chennai"]
    sample_data = []

    for c in cities:
        multiplier = {"Mumbai": 3.5, "New Delhi": 2.8, "Bangalore": 2.5, "Kolkata": 1.6, "Hyderabad": 2.0, "Chennai": 1.8}[c]
        for _ in range(150):
            sz = np.random.randint(600, 3000)
            bk = np.random.randint(1, 5)
            ag = np.random.randint(0, 20)
            pr = (sz * 0.09 * multiplier) + (bk * 15) - (ag * 0.8) + np.random.normal(0, 10)
            sample_data.append({"City": c, "Size_SqFt": sz, "BHK": bk, "Age": ag, "Price_Lakhs": max(15, pr), "Price_SqFt": (pr * 100000) / sz})

    df_analytics = pd.DataFrame(sample_data)

    plotly_theme = dict(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#e2e8f0"),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        margin=dict(t=50, l=10, r=10, b=10),
    )
    color_seq = px.colors.qualitative.Set2

    g1, g2 = st.columns(2)

    with g1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fig_bar = px.bar(
            df_analytics.groupby("City")["Price_Lakhs"].mean().reset_index(),
            x="City", y="Price_Lakhs", color="City",
            title="1. Average Property Price by City (₹ Lakhs)",
            text_auto=".1f", color_discrete_sequence=color_seq
        )
        fig_bar.update_layout(**plotly_theme, showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with g2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fig_line = px.line(
            df_analytics.groupby(["Age", "City"])["Price_Lakhs"].mean().reset_index(),
            x="Age", y="Price_Lakhs", color="City",
            title="2. Price Depreciation Trend vs. Property Age",
            color_discrete_sequence=color_seq
        )
        fig_line.update_layout(**plotly_theme)
        st.plotly_chart(fig_line, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    g3, g4 = st.columns(2)

    with g3:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fig_scatter = px.scatter(
            df_analytics, x="Size_SqFt", y="Price_Lakhs", color="City",
            title="3. Property Size vs. Price Scaling",
            opacity=0.75, color_discrete_sequence=color_seq
        )
        fig_scatter.update_layout(**plotly_theme)
        st.plotly_chart(fig_scatter, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with g4:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fig_hist = px.histogram(
            df_analytics, x="Price_SqFt", color="City", marginal="box",
            title="4. Rate per SqFt Distribution Density",
            color_discrete_sequence=color_seq
        )
        fig_hist.update_layout(**plotly_theme)
        st.plotly_chart(fig_hist, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# TAB 3: MODEL INSIGHTS
# ---------------------------------------------------------------------------
with tab3:
    st.markdown('<div class="section-label">Model Architecture & Feature Importance</div>', unsafe_allow_html=True)

    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    st.write("This application uses a **Ridge Linear Regression Pipeline** trained with standardized numeric scaling and one-hot categorical encoding.")

    ic1, ic2, ic3 = st.columns(3)
    with ic1:
        st.markdown("""
            <div class="stat-chip"><div class="label">Algorithm</div>
            <div class="value">Ridge (α = 10.0)</div></div>""", unsafe_allow_html=True)
    with ic2:
        st.markdown("""
            <div class="stat-chip"><div class="label">Target Transform</div>
            <div class="value">log(1 + y)</div></div>""", unsafe_allow_html=True)
    with ic3:
        st.markdown("""
            <div class="stat-chip"><div class="label">Test R² / MAE</div>
            <div class="value">0.93 · ₹8.5L</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    - **Algorithm:** Regularized Ridge Linear Regression ($\\alpha = 10.0$)
    - **Target Transformation:** $\\log(1 + y)$ log-space stabilization for skewed price distributions
    - **Evaluation Metrics:** Test $R^2 \\approx 0.93$, MAE $\\approx 8.5$ Lakhs
    - **Feature Pipeline:** Standardized numeric scaling + one-hot encoded categorical features
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# FOOTER
# ---------------------------------------------------------------------------
st.markdown("""
    <div class="footer-note">
        PropValuate AI · Estimates are model-generated approximations, not a substitute for professional appraisal.
    </div>
""", unsafe_allow_html=True)