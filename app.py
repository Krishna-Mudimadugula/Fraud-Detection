import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------------------------
# Page Config
# ------------------------------------------------
st.set_page_config(
    page_title="Bank Fraud Detection Dashboard",
    page_icon="🏦",
    layout="wide"
)

repo_url = "https://github.com/Krishna-Mudimadugula/Fraud-Detection"

st.markdown(f"""
<div style="position: fixed; top: 15px; right: 20px; z-index: 9999; display: flex; gap: 18px; align-items: center;">

    <a href="{repo_url}" target="_blank">
        <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png"
             style="width:22px; filter: invert(1);">
    </a>

</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<style>
.top-right {{
    position: fixed;
    top: 15px;
    right: 20px;
    z-index: 9999;
    display: flex;
    align-items: center;
    gap: 18px;
    font-family: sans-serif;
}}

/* Fork Text */
.fork-text {{
    color: white;
    font-size: 15px;
    cursor: pointer;
}}

/* GitHub Icon */
.github-icon {{
    width: 22px;
    filter: invert(1);  /* makes icon white for dark theme */
    cursor: pointer;
}}

.top-right a {{
    text-decoration: none;
}}
</style>

<div class="top-right">

    <!-- Fork Text -->
    <a href="{fork_url}" target="_blank">
        <span class="fork-text">Fork</span>
    </a>

    <!-- GitHub Icon -->
    <a href="{repo_url}" target="_blank">
        <img class="github-icon"
        src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png">
    </a>

</div>
""", unsafe_allow_html=True)

# ------------------------------------------------
# 🌌 UI + ANIMATIONS
# ------------------------------------------------
st.markdown("""
<style>

/* 🌌 Dark Blue Gradient */
.stApp {
    background: linear-gradient(180deg, #020617 0%, #021a3a 50%, #031d44 100%);
}

/* ✨ Moving Sparkles */
.stApp::before {
    content: "";
    position: fixed;
    width: 200%;
    height: 200%;
    background-image:
        radial-gradient(circle, rgba(0,195,255,0.12) 2px, transparent 2px),
        radial-gradient(circle, rgba(0,120,255,0.08) 1px, transparent 1px);
    background-size: 80px 80px, 60px 60px;
    animation: sparkleMove 40s linear infinite;
    z-index: 0;
}

@keyframes sparkleMove {
    0% { transform: translate(0,0); }
    100% { transform: translate(-200px,-200px); }
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(0,0,40,0.85);
}

/* 🔁 Scrolling Title */
.marquee-container {
    width: 100%;
    overflow: hidden;
    padding: 15px 0;
    margin-bottom: 10px;
}

.marquee {
    display: inline-block;
    white-space: nowrap;
    animation: scrollText 14s linear infinite;
    font-size: 30px;
    font-weight: bold;
    color: white;
    text-shadow: 0px 0px 12px #00c3ff;
}

@keyframes scrollText {
    0% { transform: translateX(100%); }
    100% { transform: translateX(-100%); }
}

/* Section Titles */
.section-title {
    color: #00c3ff;
    font-weight: 600;
    margin-top: 15px;
}

/* Chart Cards */
.chart-card {
    background: rgba(255,255,255,0.03);
    padding: 12px;
    border-radius: 15px;
    margin-bottom: 20px;
    backdrop-filter: blur(10px);
}

/* Metrics */
[data-testid="stMetricValue"] {
    color: #00c3ff;
    text-shadow: 0px 0px 10px #00c3ff;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# Load Data
# ------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("bank_fraud_processed.csv", encoding="latin1")

df = load_data()

# ------------------------------------------------
# 🔁 Scrolling Title
# ------------------------------------------------
st.markdown("""
<div class="marquee-container">
    <div class="marquee">🏦 Bank Transaction Fraud Monitoring Dashboard</div>
</div>
""", unsafe_allow_html=True)

st.caption("✨ AI-powered fraud analytics system")

# ------------------------------------------------
# Filters
# ------------------------------------------------
st.sidebar.markdown("### 🔎 Filters")

with st.sidebar.expander("📍 City", True):
    city_filter = [c for c in df["City"].dropna().unique() if st.checkbox(c, True)]

with st.sidebar.expander("📱 Device Type"):
    device_filter = [d for d in df["Device_Type"].dropna().unique() if st.checkbox(d, True)]

with st.sidebar.expander("🏬 Merchant Category"):
    merchant_filter = [m for m in df["Merchant_Category"].dropna().unique() if st.checkbox(m, True)]

score_filter = st.sidebar.slider(
    "Minimum Fraud Score",
    float(df["combined_score"].min()),
    float(df["combined_score"].max()),
    0.5
)

# ------------------------------------------------
# Apply Filters
# ------------------------------------------------
filtered_df = df[
    (df["City"].isin(city_filter)) &
    (df["Device_Type"].isin(device_filter)) &
    (df["Merchant_Category"].isin(merchant_filter)) &
    (df["combined_score"] >= score_filter)
]

# ------------------------------------------------
# Alert
# ------------------------------------------------
high_risk = filtered_df[filtered_df["combined_score"] > 0.85]

if len(high_risk) > 0:
    st.error(f"🚨 {len(high_risk)} HIGH-RISK FRAUD TRANSACTIONS DETECTED")
else:
    st.success("✅ No high-risk fraud alerts")

# ------------------------------------------------
# Metrics
# ------------------------------------------------
st.markdown('<div class="section-title">📊 Key Metrics</div>', unsafe_allow_html=True)

c1,c2,c3,c4 = st.columns(4)

c1.metric("📈 Total Transactions", len(filtered_df))
c2.metric("⚠ Fraud Transactions", int(filtered_df["Class"].sum()))
c3.metric("📊 Fraud Rate", f"{filtered_df['Class'].mean()*100:.2f}%")
c4.metric("🧠 Avg Fraud Score", f"{filtered_df['combined_score'].mean():.3f}")

# ------------------------------------------------
# Charts Row 1
# ------------------------------------------------
col1,col2 = st.columns(2)

with col1:
    fig = px.pie(filtered_df, names="Class",
                 title="🧾 Fraud Distribution",
                 color="Class",
                 color_discrete_map={0:"#00FFA6",1:"#FF4D6D"})
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    trend = filtered_df.groupby("Hour")["Class"].sum().reset_index()
    fig = px.line(trend, x="Hour", y="Class",
                  markers=True,
                  title="⏱ Fraud Trend by Hour",
                  color_discrete_sequence=["#00CFFF"])
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
    st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------
# Charts Row 2
# ------------------------------------------------
col1,col2 = st.columns(2)

with col1:
    merchant_chart = filtered_df.groupby("Merchant_Category")["Class"].sum().sort_values(ascending=False).head(10)
    fig = px.bar(merchant_chart,
                 title="🏬 Fraud by Merchant Category",
                 color=merchant_chart.values,
                 color_continuous_scale=["#ff9a00", "#ff3d00"])
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    device_chart = filtered_df.groupby("Device_Type")["Class"].sum()
    fig = px.bar(device_chart,
                 title="📱 Fraud by Device Type",
                 color=device_chart.values,
                 color_continuous_scale=["#7F00FF", "#E100FF"])
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
    st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------
# City Chart
# ------------------------------------------------
city_fraud = filtered_df.groupby("City")["Class"].sum().reset_index()

fig = px.bar(
    city_fraud.sort_values("Class", ascending=False).head(10),
    x="City",
    y="Class",
    title="🌍 Top Fraud Cities",
    color="Class",
    color_continuous_scale="Reds"
)
fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------
# Histogram
# ------------------------------------------------
fig = px.histogram(
    filtered_df,
    x="combined_score",
    nbins=50,
    color="Class",
    title="📉 Fraud Score Distribution",
    color_discrete_map={0:"#00CFFF",1:"#FF4D6D"}
)
fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------
# Table
# ------------------------------------------------
st.markdown("### 🚨 Top Suspicious Transactions")
top = filtered_df.sort_values("combined_score", ascending=False).head(50)
st.dataframe(top, use_container_width=True)

# ------------------------------------------------
# Customer
# ------------------------------------------------
st.markdown("### 👤 Customer Risk Profile")

customer = st.selectbox("Select Customer", filtered_df["Customer_ID"].unique())
cust_data = filtered_df[filtered_df["Customer_ID"] == customer]

st.dataframe(cust_data)

# ------------------------------------------------
# Download
# ------------------------------------------------
st.download_button(
    "📥 Download Fraud Report",
    top.to_csv(index=False),
    file_name="fraud_report.csv"
)

# ------------------------------------------------
# Simulator
# ------------------------------------------------
st.markdown('<div class="section-title">⚡ Fraud Simulator</div>', unsafe_allow_html=True)

c1,c2 = st.columns(2)

with c1:
    amount = st.number_input("Transaction Amount",0.0,100000.0,100.0)

with c2:
    hour = st.slider("Transaction Hour",0,23,12)

risk = (amount / df["Amount"].max())*0.7 + (abs(hour-df["Hour"].mean())/24)*0.3

st.write("Fraud Risk Score:", round(risk,3))

if risk > 0.7:
    st.error("⚠ HIGH RISK")
elif risk > 0.4:
    st.warning("⚠ MEDIUM RISK")
else:
    st.success("✅ LOW RISK")
