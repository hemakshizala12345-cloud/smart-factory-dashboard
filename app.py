import streamlit as st
import pandas as pd
import random
from time import sleep

# Page config
st.set_page_config(page_title="Smart Factory Dashboard", layout="wide")

# Sidebar
st.sidebar.title("⚙️ Control Panel")
view = st.sidebar.selectbox("Select View", ["Overview", "AI Insights"])

st.sidebar.markdown("---")
uploaded_file = st.sidebar.file_uploader("📂 Upload CSV File", type=["csv"])

st.sidebar.markdown("---")
st.sidebar.write("👤 Dashboard Lead")
st.sidebar.write("📡 System: Active")

# Load uploaded data
user_data = None
if uploaded_file is not None:
    user_data = pd.read_csv(uploaded_file)

# Placeholder for live updates
placeholder = st.empty()

while True:
    with placeholder.container():

        # Title
        st.title("🏭 Smart AI Factory Dashboard")
        st.markdown("Real-time Monitoring | Logistics | AI Insights")

        # KPI Section
        st.subheader("📊 Key Performance Indicators")
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Production", f"{random.randint(100,150)} units/hr", "+5%")
        col2.metric("Efficiency", f"{random.randint(85,95)}%", "+2%")
        col3.metric("Downtime", f"{random.randint(5,15)} min", "-1 min")
        col4.metric("Energy Usage", f"{random.randint(400,500)} kWh", "-3%")

        st.markdown("---")

        # Machine Health
        st.subheader("🏭 Machine Health Monitoring")
        col1, col2, col3 = st.columns(3)

        health1 = random.randint(70, 100)
        health2 = random.randint(60, 95)
        health3 = random.randint(75, 98)

        col1.metric("Machine 1", f"{health1}%")
        col2.metric("Machine 2", f"{health2}%")
        col3.metric("Machine 3", f"{health3}%")

        # Alerts
        if health2 < 70:
            st.error("🚨 Alert: Machine 2 needs attention!")
        elif health1 < 75:
            st.warning("⚠️ Warning: Maintenance required soon")
        else:
            st.success("✅ All machines running optimally")

        st.markdown("---")

        # Charts
        st.subheader("📈 Production & Energy Trends")

        data = pd.DataFrame({
            "Production": [random.randint(90,150) for _ in range(6)],
            "Energy": [random.randint(400,500) for _ in range(6)]
        })

        st.line_chart(data)

        st.markdown("---")

        # Inventory
        st.subheader("📦 Inventory Status")
        col1, col2 = st.columns(2)

        col1.metric("Raw Material", f"{random.randint(200,500)} units")
        col2.metric("Finished Goods", f"{random.randint(100,300)} units")

        st.markdown("---")

        # AI INSIGHTS SECTION
        if view == "AI Insights":
            st.subheader("🤖 Smart AI Logistics Insights")

            if user_data is not None:

                # Show data
                st.write("📂 Uploaded Data Preview")
                st.dataframe(user_data)

                # Low Stock Alert
                if "stock_level" in user_data.columns:
                    low_stock = user_data[user_data["stock_level"] < 100]
                    if not low_stock.empty:
                        st.error(f"🚨 Low Stock Alert in {len(low_stock)} records")

                # Truck Status Alert
                if "truck_status" in user_data.columns:
                    stopped = user_data[user_data["truck_status"] == "Stopped"]
                    if not stopped.empty:
                        st.warning(f"⚠️ {len(stopped)} truck(s) stopped!")

                # Speed Analysis
                if "speed_kmph" in user_data.columns:
                    avg_speed = user_data["speed_kmph"].mean()
                    st.info(f"🚚 Average Speed: {avg_speed:.2f} km/h")

                # Stock Trend Chart
                if "stock_level" in user_data.columns:
                    st.subheader("📊 Stock Level Trend")
                    st.line_chart(user_data["stock_level"])

            else:
                st.info("Upload logistics CSV to see AI insights")

        # Footer
        st.markdown("---")
        st.success("✅ System Status: Fully Operational")
        st.caption("Smart Factory + Logistics AI | Hackathon Demo")

    sleep(5)
