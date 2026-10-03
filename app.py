import streamlit as st
import pandas as pd
import os
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# Page Configuration (Title aur Icon)
st.set_page_config(page_title="Smart Attendance Dashboard", layout="wide")

# Time aur Date setup
date_today = datetime.now().strftime("%d-%m-%Y")

# Sidebar - Navigation ke liye
st.sidebar.title("📌 Navigation")
menu = st.sidebar.radio("Pages", ["Home/Dashboard", "View All Records", "System Info"])

# 1. HOME / DASHBOARD PAGE
if menu == "Home/Dashboard":
    st.title(f"📊 Attendance Dashboard - {date_today}")
    
    # Auto-refresh har 5 second mein (taaki live update dikhe)
    st_autorefresh(interval=5000, key="datarefresh")

    file_path = f"Attendance/Attendance_04-03-2026.csv{date_today}.csv"

    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        
        # Top Metrics (Summary boxes)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Students Present", len(df))
        with col2:
            last_entry = df['TIME'].iloc[-1] if not df.empty else "N/A"
            st.metric("Last Entry Time", last_entry)
        with col3:
            st.metric("Status", "🟢 Live")

        st.markdown("---")
        
        # Attendance Table display
        st.subheader("📍 Recent Attendance Logs")
        st.dataframe(df.style.highlight_max(axis=0), use_container_width=True)
        
        # Download Button
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Report (CSV)", data=csv_data, file_name=f"Attendance_{date_today}.csv")

    else:
        st.warning("⚠️ Aaj ki attendance file abhi tak bani nahi hai. Camera chalu karein!")

# 2. VIEW ALL RECORDS PAGE
elif menu == "View All Records":
    st.title("📂 Historical Records")
    folder_path = "Attendance/"
    
    if os.path.exists(folder_path):
        files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
        selected_file = st.selectbox("Select Date", files)
        
        if selected_file:
            df_old = pd.read_csv(os.path.join(folder_path, selected_file))
            st.write(f"Showing records for: {selected_file}")
            st.dataframe(df_old, use_container_width=True)
    else:
        st.error("Attendance folder nahi mila!")

# 3. SYSTEM INFO PAGE
elif menu == "System Info":
    st.title("⚙️ System Status")
    st.info("Ye system Face Recognition aur KNN Algorithm par base hai.")
    st.write("*Frontend:* Streamlit")
    st.write("*Backend:* Python (OpenCV, Scikit-learn)")