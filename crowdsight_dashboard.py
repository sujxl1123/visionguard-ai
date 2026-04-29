import streamlit as st
import cv2
import numpy as np
import pandas as pd
import os
import time
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from crowd_engine import CrowdCounter

st.set_page_config(page_title="VisionGuard Crowd AI", page_icon="👥", layout="wide")

st.markdown("""
<style>
.main-header { background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%); padding: 1.5rem; border-radius: 15px; margin-bottom: 1.5rem; text-align: center; color: white; }
.metric-card { background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); text-align: center; }
.stButton > button { font-weight: 600; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

if "crowd_counter" not in st.session_state:
    st.session_state.crowd_counter = CrowdCounter()
if "stats" not in st.session_state:
    st.session_state.stats = None

st.markdown('<div class="main-header"><h1>👥 VisionGuard Crowd AI</h1><p>Real-Time Crowd Intelligence</p></div>', unsafe_allow_html=True)

capacity = st.sidebar.number_input("Max Capacity", value=100, min_value=10)
uploaded_file = st.file_uploader("Upload video", type=["mp4", "avi", "mov"])

col1, col2 = st.columns([3, 1])
video_placeholder = col1.empty()

with col2:
    st.subheader("📊 Stats")
    if st.session_state.stats:
        s = st.session_state.stats
        st.metric("Max Count", s["max"])
        st.metric("Average", f"{s['avg']:.0f}")
        pct = (s["max"] / capacity * 100) if capacity > 0 else 0
        st.progress(min(pct/100, 1.0), text=f"Capacity: {pct:.0f}%")
    else:
        st.info("Upload video to begin")

if uploaded_file:
    video_path = "temp_video.mp4"
    with open(video_path, "wb") as f:
        f.write(uploaded_file.read())
    
    if st.button("🚀 Start Analysis", use_container_width=True, type="primary"):
        cc = st.session_state.crowd_counter
        cap = cv2.VideoCapture(video_path)
        counts = []
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            count, boxes = cc.count_people(frame)
            counts.append(count)
            
            if boxes is not None and len(boxes) > 0:
                for box in boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            cv2.putText(frame, f"Count: {count}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
            risk, color = cc.get_risk_level(count, capacity)
            cv2.putText(frame, f"Risk: {risk}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
            video_placeholder.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), use_container_width=True)
        
        cap.release()
        
        if counts:
            st.session_state.stats = {"max": max(counts), "avg": sum(counts)/len(counts), "counts": counts}
            st.success("✅ Analysis complete!")
            st.balloons()

if st.session_state.stats:
    st.markdown("---")
    st.subheader("📈 Trends")
    fig = px.line(y=st.session_state.stats["counts"], title="Crowd Count Over Time")
    st.plotly_chart(fig, use_container_width=True)