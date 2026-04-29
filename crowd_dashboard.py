import streamlit as st
import cv2
import numpy as np
import pandas as pd
from crowd_counter import CrowdCounter
import plotly.express as px
import time
import os

st.set_page_config(page_title="CrowdSight AI", page_icon="👥", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    * { font-family: 'Inter', sans-serif; }
    .stApp { background: #0f172a; }
    .hero-header { background: linear-gradient(135deg, #dc2626, #ea580c, #f97316); padding: 2rem 3rem; border-radius: 24px; color: white; margin-bottom: 2rem; }
    .stat-card { padding: 1.5rem; border-radius: 20px; color: white; text-align: center; }
    .stat-card-total { background: linear-gradient(135deg, #1e293b, #334155); border: 1px solid #475569; }
    .stat-card-high { background: linear-gradient(135deg, #dc2626, #ef4444); }
    .stat-card-medium { background: linear-gradient(135deg, #d97706, #f59e0b); }
    .stat-card-low { background: linear-gradient(135deg, #059669, #10b981); }
    .stat-number { font-size: 2.5rem; font-weight: 800; }
    .stat-label { font-size: 0.9rem; opacity: 0.9; text-transform: uppercase; letter-spacing: 1px; }
    .stButton > button { border-radius: 12px; font-weight: 600; padding: 0.7rem 1.5rem; border: none; background: linear-gradient(135deg, #dc2626, #ea580c); color: white; }
    .glass-card { background: #1e293b; border-radius: 16px; padding: 1.5rem; border: 1px solid #334155; margin-bottom: 1rem; }
</style>
""", unsafe_allow_html=True)

if 'counter' not in st.session_state:
    st.session_state.counter = CrowdCounter()
if 'stats' not in st.session_state:
    st.session_state.stats = None

st.markdown('<div class="hero-header"><h1>👥 CrowdSight AI</h1><p style="font-size:1.2rem;">Real-Time Crowd Intelligence & People Counting</p></div>', unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])

with col1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📹 Video Feed")
    video_placeholder = st.empty()
    
    uploaded_file = st.file_uploader("Upload crowd video", type=['mp4', 'avi', 'mov'])
    
    if uploaded_file:
        video_path = "temp_crowd.mp4"
        with open(video_path, 'wb') as f:
            f.write(uploaded_file.read())
        st.success("✅ Video ready!")
        
        capacity = st.slider("Max Capacity", 10, 50000, 100)
        
        if st.button("🚀 Start Counting", type="primary", use_container_width=True):
            cc = st.session_state.counter
            cap = cv2.VideoCapture(video_path)
            counts = []
            
            progress_bar = st.progress(0)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            frame_count = 0
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_count % 10 == 0:
                    count, boxes = cc.count_people(frame)
                    counts.append(count)
                    
                    if boxes is not None and len(boxes) > 0:
                        for box in boxes:
                            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (16, 185, 129), 2)
                    
                    risk, color = cc.get_risk_level(count, capacity)
                    cv2.putText(frame, f"Count: {count}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (16, 185, 129), 3)
                    cv2.putText(frame, f"Risk: {risk}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    
                    video_placeholder.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), use_container_width=True)
                
                frame_count += 1
                if frame_count % 50 == 0:
                    progress_bar.progress(min(frame_count / total_frames, 1.0))
            
            cap.release()
            
            if counts:
                st.session_state.stats = {
                    'max': max(counts),
                    'min': min(counts),
                    'avg': sum(counts) / len(counts),
                    'counts': counts
                }
                st.success(f"✅ Done! Max: {max(counts)} | Avg: {sum(counts)/len(counts):.0f}")
                st.balloons()
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📊 Live Statistics")
    
    if st.session_state.stats:
        s = st.session_state.stats
        max_count = s['max']
        
        if max_count > capacity * 0.9:
            card = 'stat-card-high'
        elif max_count > capacity * 0.5:
            card = 'stat-card-medium'
        else:
            card = 'stat-card-low'
        
        st.markdown(f'<div class="stat-card {card}"><div class="stat-number">{max_count}</div><div class="stat-label">Max Count</div></div>', unsafe_allow_html=True)
        
        st.metric("Average Count", f"{s['avg']:.0f}")
        st.metric("Minimum Count", s['min'])
        
        pct = (max_count / capacity * 100) if capacity > 0 else 0
        st.progress(min(pct / 100, 1.0), text=f"Capacity: {pct:.0f}%")
        
        if pct > 90:
            st.error("🚨 CRITICAL: Near capacity!")
        
        st.markdown("---")
        fig = px.line(y=s['counts'], title="Count Over Time")
        fig.update_layout(height=250, paper_bgcolor='rgba(0,0,0,0)', font={'color': 'white'})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Upload a video to start counting")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("CrowdSight AI | Real-Time Crowd Intelligence | © 2026")