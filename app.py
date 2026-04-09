import streamlit as st
import pandas as pd
import random
from time import sleep

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Smart Factory Dashboard", layout="wide")

# ---------- SESSION STATE ----------
if "prev_data" not in st.session_state:
    st.session_state.prev_data = {
        "prod": 120,
        "eff": 90,
        "down": 10,
        "energy": 450
    }

# ---------- AI THINK LAYER ----------
def predict_demand(stock):
    if stock < 100:
        return "Stock will run out in 2 days 🚨"
    else:
        return "Stock level is safe ✅"

def best_route():
    return "Best Route: A → C → D (Optimized)"

def predict_delay(speed):
    if speed < 10:
        return "High Delay Risk ⚠️"
    else:
        return "Low Delay Risk ✅"

# ---------- CUSTOM UI ----------
st.markdown("""
<style>
.stApp { background-color: #0e1117; }

.header {
    padding: 20px;
    border-radius: 12px;
    background: linear-gradient(90deg, #00d4ff, #007cf0);
    color: white;
    text-align: center;
    margin-bottom: 20px;
}

.card {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 20px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.4);
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

# Load CSV
user_data = None
if uploaded_file is not None:
    user_data = pd.read_csv(uploaded_file)

# ---------- DELTA FUNCTION ----------
def get_delta(current, previous):
    change = current - previous
    percent = (change / previous) * 100
    return f"{percent:+.1f}%"

# ---------- LIVE LOOP ----------
placeholder = st.empty()

while True:
    with placeholder.container():

        # HEADER
        st.markdown("""
        <div class="header">
            <h1>🏭 Smart AI Factory Dashboard</h1>
            <p>Sense → THINK → Act</p>
        </div>
        """, unsafe_allow_html=True)

        # ---------- KPI ----------
        st.markdown('<div class="card">', unsafe_allow_html=True)

        prod = random.randint(100,150)
        eff = random.randint(85,95)
        down = random.randint(5,15)
        energy = random.randint(400,500)

        prev = st.session_state.prev_data

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Production", f"{prod}", get_delta(prod, prev["prod"]))
        c2.metric("Efficiency", f"{eff}%", get_delta(eff, prev["eff"]))
        c3.metric("Downtime", f"{down}", get_delta(down, prev["down"]))
        c4.metric("Energy", f"{energy}", get_delta(energy, prev["energy"]))

        st.markdown('</div>', unsafe_allow_html=True)

        st.session_state.prev_data = {
            "prod": prod,
            "eff": eff,
            "down": down,
            "energy": energy
        }

        # ---------- MACHINE ----------
        st.markdown('<div class="card">', unsafe_allow_html=True)

        m1, m2, m3 = st.columns(3)

        h1 = random.randint(70, 100)
        h2 = random.randint(60, 95)
        h3 = random.randint(75, 98)

        m1.metric("Machine 1", f"{h1}%")
        m2.metric("Machine 2", f"{h2}%")
        m3.metric("Machine 3", f"{h3}%")

        popup = False
        message = ""

        if h2 < 70:
            popup = True
            message = "🚨 Machine 2 Critical!"
        elif h1 < 75:
            popup = True
            message = "⚠️ Maintenance Required"

        if popup:
            st.error(message)
        else:
            st.success("✅ All machines healthy")

        # POPUP
        if popup:
            st.markdown(f"""
            <div style="
                position: fixed;
                top: 25%;
                left: 30%;
                width: 40%;
                background-color: red;
                color: white;
                padding: 25px;
                border-radius: 15px;
                text-align: center;
                font-size: 22px;
                z-index: 9999;">
                {message}
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # ---------- CHART ----------
        st.markdown('<div class="card">', unsafe_allow_html=True)

        chart_data = pd.DataFrame({
            "Production": [random.randint(90,150) for _ in range(6)],
            "Energy": [random.randint(400,500) for _ in range(6)]
        })

        st.line_chart(chart_data)

        st.markdown('</div>', unsafe_allow_html=True)

        # ---------- AI THINK LAYER ----------
        if view == "AI Insights":
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("🧠 THINK Layer - AI Engine")

            if user_data is not None:
                st.dataframe(user_data)

                # Demand Prediction
                if "stock_level" in user_data.columns:
                    avg_stock = user_data["stock_level"].mean()
                    st.info(f"📊 {predict_demand(avg_stock)}")

                # Route
                st.success(f"🗺️ {best_route()}")

                # Delay
                if "speed_kmph" in user_data.columns:
                    avg_speed = user_data["speed_kmph"].mean()
                    delay = predict_delay(avg_speed)

                    if "High" in delay:
                        st.error(f"🚨 {delay}")
                    else:
                        st.success(f"✅ {delay}")

                # Chart
                if "stock_level" in user_data.columns:
                    st.line_chart(user_data["stock_level"])

            else:
                st.warning("Upload CSV to activate AI engine")

            st.markdown('</div>', unsafe_allow_html=True)

        # ---------- FOOTER ----------
        st.markdown("---")
        st.success("🟢 System Fully Operational")

    sleep(5)
