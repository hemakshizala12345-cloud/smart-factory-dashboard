import streamlit as st
import pandas as pd
import random
from time import sleep

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Smart Factory Dashboard", layout="wide")

# ---------- CUSTOM UI ----------
st.markdown("""
<style>

/* Background */
.stApp {
    background-color: #0e1117;
}

/* Header */
.header {
    padding: 20px;
    border-radius: 12px;
    background: linear-gradient(90deg, #00d4ff, #007cf0);
    color: white;
    text-align: center;
    margin-bottom: 20px;
}

/* Cards */
.card {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 20px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.4);
}

/* Titles */
h2 {
    color: #00d4ff;
}

</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.title("⚙️ Control Panel")
view = st.sidebar.radio("Select Section", ["Overview", "AI Insights"])
uploaded_file = st.sidebar.file_uploader("📂 Upload CSV", type=["csv"])

st.sidebar.markdown("---")
st.sidebar.write("👤 Dashboard Lead")
st.sidebar.write("🟢 System Active")

# Load data
user_data = None
if uploaded_file is not None:
    user_data = pd.read_csv(uploaded_file)

# ---------- LIVE LOOP ----------
placeholder = st.empty()

while True:
    with placeholder.container():

        # ---------- HEADER ----------
        st.markdown("""
        <div class="header">
            <h1>🏭 Smart AI Factory Dashboard</h1>
            <p>Real-time Monitoring • Logistics • AI Insights</p>
        </div>
        """, unsafe_allow_html=True)

        # ---------- KPI SECTION ----------
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📊 Key Performance Indicators")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Production", f"{random.randint(100,150)} units/hr", "+5%")
        col2.metric("Efficiency", f"{random.randint(85,95)}%", "+2%")
        col3.metric("Downtime", f"{random.randint(5,15)} min", "-1 min")
        col4.metric("Energy", f"{random.randint(400,500)} kWh", "-3%")

        st.markdown('</div>', unsafe_allow_html=True)

        # ---------- MACHINE HEALTH ----------
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🏭 Machine Health")

        c1, c2, c3 = st.columns(3)

        h1 = random.randint(70, 100)
        h2 = random.randint(60, 95)
        h3 = random.randint(75, 98)

        c1.metric("Machine 1", f"{h1}%")
        c2.metric("Machine 2", f"{h2}%")
        c3.metric("Machine 3", f"{h3}%")

        # Alerts
        if h2 < 70:
            st.error("🚨 Machine 2 needs immediate attention!")
        elif h1 < 75:
            st.warning("⚠️ Maintenance required soon")
        else:
            st.success("✅ All machines operating normally")

        st.markdown('</div>', unsafe_allow_html=True)

        # ---------- CHART SECTION ----------
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📈 Production & Energy Trends")

        data = pd.DataFrame({
            "Production": [random.randint(90,150) for _ in range(6)],
            "Energy": [random.randint(400,500) for _ in range(6)]
        })

        st.line_chart(data)
        st.markdown('</div>', unsafe_allow_html=True)

        # ---------- INVENTORY ----------
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📦 Inventory")

        c1, c2 = st.columns(2)
        c1.metric("Raw Material", f"{random.randint(200,500)} units")
        c2.metric("Finished Goods", f"{random.randint(100,300)} units")

        st.markdown('</div>', unsafe_allow_html=True)

        # ---------- AI INSIGHTS ----------
        if view == "AI Insights":
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("🤖 AI Logistics Insights")

            if user_data is not None:
                st.dataframe(user_data)

                # Low Stock Alert
                if "stock_level" in user_data.columns:
                    low_stock = user_data[user_data["stock_level"] < 100]
                    if not low_stock.empty:
                        st.error(f"🚨 Low stock detected in {len(low_stock)} records")

                # Truck Alerts
                if "truck_status" in user_data.columns:
                    stopped = user_data[user_data["truck_status"] == "Stopped"]
                    if not stopped.empty:
                        st.warning(f"⚠️ {len(stopped)} truck(s) stopped")

                # Speed Analysis
                if "speed_kmph" in user_data.columns:
                    avg_speed = user_data["speed_kmph"].mean()
                    st.info(f"🚚 Average Speed: {avg_speed:.2f} km/h")

                # Stock Chart
                if "stock_level" in user_data.columns:
                    st.subheader("📊 Stock Trend")
                    st.line_chart(user_data["stock_level"])

            else:
                st.info("Upload CSV to activate AI insights")

            st.markdown('</div>', unsafe_allow_html=True)

        # ---------- FOOTER ----------
        st.markdown("---")
        st.success("🟢 System Status: Fully Operational")
        st.caption("Smart Factory + AI + Logistics Dashboard")

    sleep(5)
