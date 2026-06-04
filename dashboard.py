import streamlit as st
import pandas as pd
import sqlite3
import time

DB_FILE = 'data/machine_data.db'

st.set_page_config(page_title="Smart Factory Dashboard", layout="wide")

def load_data():
    try:
        conn = sqlite3.connect(DB_FILE)
        query = "SELECT * FROM logs ORDER BY timestamp DESC LIMIT 100"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception:
        return pd.DataFrame()

def show_status(df):
    st.subheader("📊 Machine Status")
    latest = df.groupby('machine_id').first().reset_index()
    for _, row in latest.iterrows():
        # FIX LOGIKA: 1 = At Risk (Merah), 0 = Healthy (Hijau)
        color = "red" if int(row['prediction']) == 1 else "green"
        status = "⚠️ At Risk" if int(row['prediction']) == 1 else "✅ Healthy"
        
        st.markdown(f"""
            <div style='padding:15px; border-radius:10px; background-color:{color}; color:white; margin-bottom:10px;'>
                <span style='font-size:18px;'><strong>{row['machine_id']}</strong>: {status}</span><br>
                Temp: {row['temperature']}°C | Vib: {row['vibration']} m/s²<br>
                <small>Last Updated: {row['timestamp']}</small>
            </div>
        """, unsafe_allow_html=True)

def show_charts(df):
    st.subheader("📈 Sensor Trends")
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    machines = sorted(df['machine_id'].unique())

    for machine in machines:
        st.markdown(f"### {machine}")
        mdf = df[df['machine_id'] == machine].sort_values('timestamp')

        col1, col2 = st.columns(2)
        with col1:
            st.caption("Temperature Over Time")
            st.line_chart(mdf.set_index('timestamp')['temperature'], use_container_width=True)
        with col2:
            st.caption("Vibration Over Time")
            st.line_chart(mdf.set_index('timestamp')['vibration'], use_container_width=True)

def show_logs(df):
    st.subheader("🧾 Recent Logs (SQLite DB)")
    st.dataframe(df, use_container_width=True)

def main():
    st.title("🛠️ 5G + IoT + ML Smart Factory Dashboard")

    refresh_interval = st.sidebar.slider("⏱️ Refresh every (seconds)", 2, 20, 5)
    st.sidebar.markdown("Built with ❤️ using Streamlit + SQLite + ML")

    df = load_data()
    
    if df.empty:
        st.warning("🔄 Waiting for database logs... Please make sure Terminal 1 and 2 are running.")
    else:
        show_status(df)
        show_charts(df)
        show_logs(df)

    # Auto-refresh aman khas Streamlit modern
    time.sleep(refresh_interval)
    st.rerun()

if __name__ == "__main__":
    main()