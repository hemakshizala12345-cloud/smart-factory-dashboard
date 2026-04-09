import streamlit as st
import pandas as pd
import random
import time
from time import sleep

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Smart Factory Dashboard", layout="wide")

# ---------- SESSION ----------
if "prev_data" not in st.session_state:
    st.session_state.prev_data = {"prod":120,"eff":90,"down":10,"energy":450}

if "upload_time" not in st.session_state:
    st.session_state.upload_time = None

# ---------- DELTA ----------
def get_delta(current, previous):
    if previous == 0:
        return "0%"
    return f"{((current-previous)/previous)*100:+.1f}%"

# ---------- DIGITAL TWIN ----------
def simulate_future(data):
    future_stock = []
    future_speed = []

    stock = data["stock_level"].iloc[-1]
    speed = data["speed_kmph"].iloc[-1]

    for _ in range(5):
        stock = stock - random.randint(5,20) + random.randint(0,10)
        speed = max(0, speed + random.randint(-10,10))

        future_stock.append(stock)
        future_speed.append(speed)

    return pd.DataFrame({
        "Future Stock": future_stock,
        "Future Speed": future_speed
    })

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

# ---------- LOAD CSV ----------
user_data = None
if uploaded_file is not None:
    user_data = pd.read_csv(uploaded_file)

    if st.session_state.upload_time is None:
        st.session_state.upload_time = time.time()

# ---------- MODE ----------
use_csv = False
if st.session_state.upload_time is not None:
    elapsed = time.time() - st.session_state.upload_time
    if elapsed <= 10:
        use_csv = True
    else:
        use_csv = False
        st.session_state.upload_time = None

# ---------- MAIN LOOP ----------
placeholder = st.empty()

while True:
    with placeholder.container():

        # HEADER
        st.markdown("""
        <div class="header">
            <h1>🏭 Smart AI Factory Dashboard</h1>
            <p>Sense → THINK → Act → Predict</p>
        </div>
        """, unsafe_allow_html=True)

        # MODE
        if use_csv:
            st.info("📂 Real Data Mode (10 sec)")
        else:
            st.success("🔄 Simulation Mode")

        # ---------- KPI ----------
        st.markdown('<div class="card">', unsafe_allow_html=True)

        if use_csv and user_data is not None:
            prod = int(user_data["outflow"].mean())
            eff = int((user_data["inflow"].sum()/user_data["outflow"].sum())*100)
            down = int((user_data["truck_status"]=="Stopped").sum())
            energy = int(user_data["speed_kmph"].mean()*5)
        else:
            prod = random.randint(100,150)
            eff = random.randint(85,95)
            down = random.randint(5,15)
            energy = random.randint(400,500)

        prev = st.session_state.prev_data

        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Production", prod, get_delta(prod, prev["prod"]))
        c2.metric("Efficiency", f"{eff}%", get_delta(eff, prev["eff"]))
        c3.metric("Downtime", down, get_delta(down, prev["down"]))
        c4.metric("Energy", energy, get_delta(energy, prev["energy"]))

        st.session_state.prev_data = {"prod":prod,"eff":eff,"down":down,"energy":energy}

        st.markdown('</div>', unsafe_allow_html=True)

        # ---------- MACHINE ----------
        st.markdown('<div class="card">', unsafe_allow_html=True)

        if use_csv and user_data is not None:
            h1 = int(user_data["speed_kmph"].iloc[0]*2)
            h2 = int(user_data["speed_kmph"].iloc[1]*2)
            h3 = int(user_data["speed_kmph"].iloc[2]*2)
        else:
            h1 = random.randint(70,100)
            h2 = random.randint(60,95)
            h3 = random.randint(75,98)

        m1,m2,m3 = st.columns(3)
        m1.metric("Machine 1", f"{h1}%")
        m2.metric("Machine 2", f"{h2}%")
        m3.metric("Machine 3", f"{h3}%")

        popup = False
        msg = ""

        if h2 < 70:
            popup = True
            msg = "🚨 Machine 2 Critical!"
        elif h1 < 75:
            popup = True
            msg = "⚠️ Maintenance Required"

        if popup:
            st.error(msg)
        else:
            st.success("✅ All machines healthy")

        if popup:
            st.markdown(f"""
            <div style="
                position: fixed;
                top: 25%;
                left: 30%;
                width: 40%;
                background: red;
                color: white;
                padding: 20px;
                border-radius: 10px;
                text-align:center;
                font-size:20px;
                z-index:9999;">
                {msg}
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # ---------- CHART ----------
        st.markdown('<div class="card">', unsafe_allow_html=True)

        if use_csv and user_data is not None:
            st.line_chart(user_data[["stock_level","speed_kmph"]])
        else:
            chart = pd.DataFrame({
                "Production":[random.randint(90,150) for _ in range(6)],
                "Energy":[random.randint(400,500) for _ in range(6)]
            })
            st.line_chart(chart)

        st.markdown('</div>', unsafe_allow_html=True)

        # ---------- AI ----------
        if view == "AI Insights":
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("🧠 Row-wise AI Analysis")

            if use_csv and user_data is not None:

                for i, row in user_data.iterrows():

                    st.markdown(f"### 📍 Truck {row['truck_id']} | Warehouse {row['warehouse_id']}")

                    col1, col2, col3 = st.columns(3)

                    if row["stock_level"] < 100:
                        col1.error(f"Stock: {row['stock_level']} → 🚨 Low")
                    else:
                        col1.success(f"Stock: {row['stock_level']} → ✅ OK")

                    if row["speed_kmph"] < 10:
                        col2.error(f"Speed: {row['speed_kmph']} → 🚨 Delay")
                    elif row["speed_kmph"] < 25:
                        col2.warning(f"Speed: {row['speed_kmph']} → ⚠️ Slow")
                    else:
                        col2.success(f"Speed: {row['speed_kmph']} → ✅ Normal")

                    if row["stock_level"] < 100 and row["speed_kmph"] < 10:
                        col3.error("🚨 Critical")
                    elif row["stock_level"] < 100:
                        col3.warning("⚠️ Low Stock")
                    elif row["speed_kmph"] < 10:
                        col3.warning("⚠️ Delay Risk")
                    else:
                        col3.success("✅ All Good")

                    st.markdown("---")

            else:
                st.warning("Upload CSV to activate AI")

            st.markdown('</div>', unsafe_allow_html=True)

            # ---------- DIGITAL TWIN ----------
            if use_csv and user_data is not None:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader("🔮 Digital Twin – Future Simulation")

                future_df = simulate_future(user_data)

                st.line_chart(future_df)

                if future_df["Future Stock"].min() < 100:
                    st.error("🚨 Future Risk: Low Stock")

                if future_df["Future Speed"].min() < 10:
                    st.warning("⚠️ Future Delay Risk")

                st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")
        st.success("🟢 System Running")

    sleep(5)
