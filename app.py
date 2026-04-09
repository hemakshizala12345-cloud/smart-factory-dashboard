import streamlit as st
import pandas as pd
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
        return "🚨 Stock will run out soon"
    else:
        return "✅ Stock level is safe"

def best_route():
    return "🗺️ Route Optimized: A → C → D"

def predict_delay(speed):
    if speed < 10:
        return "🚨 High Delay Risk"
    else:
        return "✅ Low Delay Risk"

# ---------- DELTA FUNCTION ----------
def get_delta(current, previous):
    if previous == 0:
        return "0%"
    change = current - previous
    percent = (change / previous) * 100
    return f"{percent:+.1f}%"

# ---------- UI ----------
st.markdown("""
<style>
.stApp { background-color: #0e1117; }
.header {
    padding: 20px;
    border-radius: 12px;
    background: linear-gradient(90deg, #00d4ff, #007cf0);
    color: white;
    text-align: center;
}
.card {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 12px;
    margin-top: 15px;
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

# ---------- MAIN ----------
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

        if user_data is not None:

            prod = int(user_data["outflow"].mean())
            eff = int((user_data["inflow"].sum() / user_data["outflow"].sum()) * 100)
            down = int((user_data["truck_status"] == "Stopped").sum())
            energy = int(user_data["speed_kmph"].mean() * 5)

        else:
            prod, eff, down, energy = 120, 90, 10, 450

        prev = st.session_state.prev_data

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Production", prod, get_delta(prod, prev["prod"]))
        c2.metric("Efficiency", f"{eff}%", get_delta(eff, prev["eff"]))
        c3.metric("Downtime", down, get_delta(down, prev["down"]))
        c4.metric("Energy", energy, get_delta(energy, prev["energy"]))

        st.session_state.prev_data = {
            "prod": prod,
            "eff": eff,
            "down": down,
            "energy": energy
        }

        st.markdown('</div>', unsafe_allow_html=True)

        # ---------- MACHINE HEALTH ----------
        st.markdown('<div class="card">', unsafe_allow_html=True)

        if user_data is not None and len(user_data) >= 3:
            h1 = int(user_data["speed_kmph"].iloc[0] * 2)
            h2 = int(user_data["speed_kmph"].iloc[1] * 2)
            h3 = int(user_data["speed_kmph"].iloc[2] * 2)
        else:
            h1, h2, h3 = 90, 85, 88

        m1, m2, m3 = st.columns(3)
        m1.metric("Machine 1", f"{h1}%")
        m2.metric("Machine 2", f"{h2}%")
        m3.metric("Machine 3", f"{h3}%")

        # ALERT
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

        if user_data is not None:
            st.line_chart(user_data[["stock_level", "speed_kmph"]])

        st.markdown('</div>', unsafe_allow_html=True)

        # ---------- AI THINK ----------
        if view == "AI Insights":
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("🧠 THINK Layer")

            if user_data is not None:

                st.dataframe(user_data)

                avg_stock = user_data["stock_level"].mean()
                st.info(predict_demand(avg_stock))

                st.success(best_route())

                avg_speed = user_data["speed_kmph"].mean()
                delay = predict_delay(avg_speed)

                if "High" in delay:
                    st.error(delay)
                else:
                    st.success(delay)

            else:
                st.warning("Upload CSV")

            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")
        st.success("🟢 System Operational")

    sleep(5)
