import os
import json
import subprocess
import pandas as pd
import streamlit as st

st.set_page_config(page_title="VisionGuard AI", page_icon="��", layout="wide")

VIDEO_MAIN_PATH = "main.py"
VIDEO_INPUT_PATH = "input.mp4"
VIDEO_RESULTS_JSON = "attendance_results.json"

if "video_processed" not in st.session_state:
    st.session_state.video_processed = False

st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #1e3c72, #2a5298);
    padding: 1.5rem;
    border-radius: 12px;
    color: white;
    text-align: center;
    margin-bottom: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
<h1>🎓 VisionGuard AI</h1>
<p>Smart Attendance System</p>
</div>
""", unsafe_allow_html=True)

st.success("✅ NEW VISIONGUARD APP IS RUNNING")
st.write("Running file:", __file__)
st.write("Current folder:", os.getcwd())

def save_uploaded_video(file):
    with open(VIDEO_INPUT_PATH, "wb") as f:
        f.write(file.getbuffer())

def run_video():
    st.session_state.video_processed = False

    if os.path.exists(VIDEO_RESULTS_JSON):
        os.remove(VIDEO_RESULTS_JSON)

    if not os.path.exists(VIDEO_MAIN_PATH):
        return False, f"main.py not found in {os.getcwd()}"

    result = subprocess.run(
        ["python", VIDEO_MAIN_PATH],
        cwd=".",
        capture_output=True,
        text=True
    )

    output = (result.stdout or "") + "\n" + (result.stderr or "")

    if result.returncode != 0:
        return False, output

    if not os.path.exists(VIDEO_RESULTS_JSON):
        return False, "attendance_results.json was not created.\n\n" + output

    return True, output

def load_results():
    if not os.path.exists(VIDEO_RESULTS_JSON):
        return None

    with open(VIDEO_RESULTS_JSON, "r") as f:
        data = json.load(f)

    rows = []

    for name, rec in data.get("attendance", {}).items():
        rows.append({
            "Name": name,
            "ID": data.get("name_to_id", {}).get(name, "N/A"),
            "Status": "Present" if rec.get("present") else "Absent",
            "Detections": rec.get("count", 0),
            "First Seen": rec.get("first_seen", "N/A")
        })

    return pd.DataFrame(rows)

def show_summary(df):
    total = len(df)
    present = len(df[df["Status"] == "Present"])
    absent = len(df[df["Status"] == "Absent"])
    percent = (present / total * 100) if total else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("👥 Total Students", total)
    c2.metric("✅ Present", present)
    c3.metric("❌ Absent", absent)
    c4.metric("📊 Attendance %", f"{percent:.2f}%")

mode = st.radio(
    "Choose Mode",
    ["📤 Video Upload Mode", "🎥 Live Camera Mode"],
    horizontal=True
)

if mode == "📤 Video Upload Mode":
    st.subheader("📤 Video Upload Attendance")

    uploaded_file = st.file_uploader(
        "Upload classroom video",
        type=["mp4", "avi", "mov", "mkv"],
        key="video_upload_file"
    )

    if uploaded_file is not None:
        st.video(uploaded_file)

        if st.button("▶️ Run Attendance", key="run_attendance_btn"):
            save_uploaded_video(uploaded_file)

            with st.spinner("Processing video..."):
                ok, output = run_video()

            if ok:
                st.session_state.video_processed = True
                st.success("Attendance processed successfully.")
            else:
                st.error("Video processing failed.")
                st.code(output)

    if st.session_state.video_processed:
        df = load_results()

        if df is not None and not df.empty:
            show_summary(df)

            st.markdown("### 📋 Attendance Table")
            st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "⬇️ Download Attendance CSV",
                csv,
                "attendance.csv",
                "text/csv"
            )
        else:
            st.warning("No attendance data found.")

else:
    st.subheader("🎥 Live Camera Mode")
    st.info("Live camera mode will be added after video mode is stable.")
