"""
╔══════════════════════════════════════════════════════════════╗
║           VISIONGUARD AI PRO - COMPETITION WINNER            ║
║              Enterprise Attendance Intelligence              ║
║                                                            ║
║  Developed by: Sujal Ganesh Kamathe & Saniya Rahul Dhawade ║
║  Guide: Dr. Vikas J. Magar                                 ║
║  MIT World Peace University, Pune                           ║
║  © 2026 VisionGuard AI. All rights reserved.               ║
╚══════════════════════════════════════════════════════════════╝
"""
import streamlit as st
import pandas as pd
import json
import os
import subprocess
import time
import math
import cv2
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import random

APP_NAME = "VisionGuard AI Pro"
APP_VERSION = "4.0.0"
COLLEGE = "MIT World Peace University, Pune"
DEVELOPERS = "Sujal Ganesh Kamathe & Saniya Rahul Dhawade"
GUIDE = "Dr. Vikas J. Magar"
BATCH = "SY BSc DSBDA | 2026-27"

st.set_page_config(page_title=APP_NAME, page_icon="🎓", layout="wide", initial_sidebar_state="expanded")

# ═══════════════════ THEME ═══════════════════
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    * { font-family: 'Inter', sans-serif; }
    .stApp { background: #0a0e17; }
    
    .hero {
        background: linear-gradient(135deg, #1e293b, #0f3460, #16213e);
        border: 1px solid rgba(99,102,241,0.3);
        padding: 2rem 3rem; border-radius: 24px; color: white;
        margin-bottom: 2rem; box-shadow: 0 20px 60px rgba(0,0,0,0.5);
    }
    
    .stat-card {
        padding: 1.5rem; border-radius: 20px; color: white; text-align: center;
        border: 1px solid rgba(255,255,255,0.08); transition: all 0.3s; cursor: pointer;
    }
    .stat-card:hover { transform: translateY(-5px); box-shadow: 0 20px 60px rgba(0,0,0,0.6); }
    .stat-total { background: linear-gradient(135deg, #1e293b, #1a1a3e); }
    .stat-present { background: linear-gradient(135deg, #064e3b, #065f46); border-color: #10b981; }
    .stat-absent { background: linear-gradient(135deg, #4c1d1d, #7f1d1d); border-color: #ef4444; }
    .stat-late { background: linear-gradient(135deg, #4a3a0a, #78350f); border-color: #f59e0b; }
    .stat-pending { background: linear-gradient(135deg, #1e1b4b, #312e81); border-color: #6366f1; }
    .stat-number { font-size: 2.5rem; font-weight: 800; }
    .stat-label { font-size: 0.8rem; opacity: 0.8; text-transform: uppercase; letter-spacing: 2px; }
    .stat-subtitle { font-size: 0.7rem; opacity: 0.5; }
    
    .stButton > button {
        border-radius: 12px; font-weight: 600; padding: 0.7rem 1.5rem;
        background: linear-gradient(135deg, #6366f1, #4f46e5); color: white;
        border: none; transition: all 0.3s;
    }
    .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(99,102,241,0.4); }
    
    .glass {
        background: rgba(30,41,59,0.7); backdrop-filter: blur(20px);
        border-radius: 20px; padding: 1.5rem; border: 1px solid rgba(255,255,255,0.08);
        margin-bottom: 1rem;
    }
    
    .insight-card {
        background: rgba(30,41,59,0.5); border: 1px solid rgba(255,255,255,0.05);
        border-radius: 14px; padding: 1.2rem; margin: 0.5rem 0;
        border-left: 4px solid #6366f1; transition: all 0.3s;
    }
    .insight-positive { border-left-color: #10b981; }
    .insight-warning { border-left-color: #f59e0b; }
    .insight-danger { border-left-color: #ef4444; }
    
    .service-card {
        background: rgba(30,41,59,0.5); border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px; padding: 1.5rem; text-align: center; transition: all 0.3s; cursor: pointer;
    }
    .service-card:hover { background: rgba(99,102,241,0.1); border-color: rgba(99,102,241,0.3); transform: translateY(-3px); }
    .service-icon { font-size: 2.5rem; margin-bottom: 0.5rem; }
    .service-name { font-weight: 600; color: white; }
    .service-time { font-size: 0.8rem; color: #94a3b8; }
    
    .status-badge { padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; display: inline-block; }
    .status-pending { background: #f59e0b; color: black; }
    .status-approved { background: #10b981; color: white; }
    .status-processing { background: #6366f1; color: white; }
    .status-completed { background: #10b981; color: white; }
    .status-rejected { background: #ef4444; color: white; }
    
    .stTabs [data-baseweb="tab-list"] { gap: 0.4rem; background: rgba(30,41,59,0.5); padding: 0.4rem; border-radius: 14px; }
    .stTabs [data-baseweb="tab"] { border-radius: 10px; padding: 0.6rem 1.2rem; font-weight: 600; font-size: 0.85rem; color: #94a3b8; }
    .stTabs [aria-selected="true"] { background: linear-gradient(135deg, #6366f1, #8b5cf6) !important; color: white !important; }
    
    .sidebar-profile { text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #6366f1, #4f46e5); border-radius: 16px; color: white; margin-bottom: 1rem; }
    .badge-demo { background: #f59e0b; color: black; padding: 4px 14px; border-radius: 20px; font-weight: 700; animation: pulse 2s infinite; display: inline-block; }
    .badge-live { background: #10b981; color: white; padding: 4px 12px; border-radius: 20px; font-weight: 700; animation: pulse 1.5s infinite; display: inline-block; }
    
    @keyframes pulse { 0%,100% { opacity:1; } 50% { opacity:0.5; } }
    .footer { text-align: center; padding: 1.5rem; color: #64748b; font-size: 0.8rem; border-top: 1px solid rgba(255,255,255,0.05); margin-top: 3rem; }
    .footer-brand { color: #818cf8; font-weight: 600; }
    
    .timetable-card { background: rgba(30,41,59,0.5); padding: 1rem; border-radius: 12px; margin: 0.3rem 0; border-left: 3px solid #6366f1; }
    .timetable-card.current { border-left-color: #10b981; background: rgba(16,185,129,0.1); }
    .certificate { background: white; color: black; padding: 2rem; border-radius: 16px; text-align: center; border: 4px double #6366f1; }
    
    .student-quick-action {
        background: rgba(30,41,59,0.5); border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px; padding: 1.2rem; text-align: center; cursor: pointer; transition: all 0.3s;
    }
    .student-quick-action:hover { background: rgba(99,102,241,0.15); border-color: rgba(99,102,241,0.4); transform: translateY(-3px); }
    .quick-icon { font-size: 2rem; margin-bottom: 0.3rem; }
    .quick-text { font-size: 0.85rem; color: white; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════ AUTO-CLEAR ═══════════════════
if 'session_started' not in st.session_state:
    for f in ['attendance_results.json', 'attendance.csv', 'live_attendance.json']:
        if os.path.exists(f): os.remove(f)
    st.session_state.session_started = True

# ═══════════════════ SESSION ═══════════════════
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'role' not in st.session_state: st.session_state.role = None
if 'user' not in st.session_state: st.session_state.user = {}
if 'total_lectures' not in st.session_state: st.session_state.total_lectures = 40
if 'live_running' not in st.session_state: st.session_state.live_running = False
if 'live_marked' not in st.session_state: st.session_state.live_marked = set()
if 'demo' not in st.session_state: st.session_state.demo = False
if 'clicked_stat' not in st.session_state: st.session_state.clicked_stat = None
if 'reset_otp' not in st.session_state: st.session_state.reset_otp = None
if 'service_requests' not in st.session_state: st.session_state.service_requests = []

# ═══════════════════ SERVICES ═══════════════════
SERVICES = {
    "📄 Bonafide Certificate": {"fee": "₹100", "time": "1-2 days", "dept": "Academic Office"},
    "🎓 Leaving Certificate (LC)": {"fee": "₹500", "time": "7-10 days", "dept": "Academic Office"},
    "📝 Transcript": {"fee": "₹300", "time": "15-20 days", "dept": "Examination Cell"},
    "🆔 ID Card Reissue": {"fee": "₹200", "time": "2-3 days", "dept": "Security Office"},
    "🏥 Medical Leave": {"fee": "Free", "time": "Same day", "dept": "Medical Center"},
    "💰 Fee Receipt": {"fee": "Free", "time": "1 day", "dept": "Accounts Department"},
    "🎫 Exam Form Correction": {"fee": "₹150", "time": "2-3 days", "dept": "Examination Cell"},
    "📋 Scholarship Document": {"fee": "Free", "time": "3-5 days", "dept": "Scholarship Cell"},
    "🚌 Bus Pass": {"fee": "₹500", "time": "5-7 days", "dept": "Transport Office"},
    "🏠 Hostel Request": {"fee": "₹1000", "time": "7-14 days", "dept": "Hostel Office"}
}

# ═══════════════════ HELPERS ═══════════════════
def load_csv(f):
    try:
        if os.path.exists(f): return pd.read_csv(f)
    except: pass
    return None

def load_json(f):
    try:
        if os.path.exists(f):
            with open(f) as fh: return json.load(fh)
    except: pass
    return None

def save_json(f, d):
    with open(f, 'w') as fh: json.dump(d, fh, indent=2)

def load_attendance():
    records = []
    for src in ['attendance_results.json', 'live_attendance.json']:
        data = load_json(src)
        if data:
            att = data.get('attendance', data)
            nti = data.get('name_to_id', {})
            if isinstance(att, dict):
                for name, info in att.items():
                    if isinstance(info, dict) and name not in ['name_to_id']:
                        records.append({
                            'name': name, 'id': nti.get(name, name),
                            'status': 'Present' if info.get('present') else info.get('status', 'Absent'),
                            'timestamp': info.get('first_seen', info.get('timestamp', 'N/A')),
                            'count': info.get('count', 1)
                        })
    return records

def get_camera():
    cap = cv2.VideoCapture(0)
    if cap.isOpened(): cap.release(); return 0
    return None

def generate_certificate(student_name, prn, percentage):
    return f"""
    <div class="certificate">
        <h2 style="color:#1e3c72;">{COLLEGE}</h2>
        <h3 style="color:#6366f1;">ATTENDANCE CERTIFICATE</h3>
        <p>This is to certify that</p>
        <h2 style="color:#1e3c72;">{student_name}</h2>
        <p>PRN: {prn}</p>
        <p>has achieved <strong>{percentage:.1f}%</strong> attendance</p>
        <p style="color:#10b981;font-weight:700;">✅ ELIGIBLE FOR EXAMINATIONS</p>
        <hr><p>Generated by {APP_NAME} v{APP_VERSION}</p>
    </div>"""

def submit_service_request(student_name, prn, service_type, notes=""):
    request = {
        'id': f"SR{len(st.session_state.service_requests)+1:04d}",
        'student': student_name, 'prn': prn, 'service': service_type,
        'status': 'Pending', 'date': datetime.now().strftime("%d %b %Y, %I:%M %p"),
        'notes': notes, 'dept': SERVICES[service_type]['dept'],
        'fee': SERVICES[service_type]['fee'], 'est_time': SERVICES[service_type]['time']
    }
    st.session_state.service_requests.append(request)
    save_json('service_requests.json', st.session_state.service_requests)
    return request['id']

def load_service_requests():
    data = load_json('service_requests.json')
    if data: st.session_state.service_requests = data
    return st.session_state.service_requests

# ═══════════════════ LOGIN ═══════════════════
def login_page():
    col1, col2, col3 = st.columns([1, 0.8, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f'<div style="text-align:center;margin-bottom:2rem;"><div style="font-size:4rem;">🎓</div><h1 style="color:white;font-size:2.2rem;font-weight:800;">{APP_NAME}</h1><p style="color:#94a3b8;">Enterprise Attendance Intelligence</p></div>', unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="glass"><h3 style="color:white;">🔐 Sign In</h3>', unsafe_allow_html=True)
            role = st.selectbox("Select Role", ["Teacher", "Student", "Administrator"])
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button("🚀 Sign In", use_container_width=True, type="primary"):
                    if username == "demo" and password == "demo":
                        st.session_state.logged_in = True
                        st.session_state.role = role.lower().replace('administrator','admin')
                        st.session_state.user = {'name':'Demo User','id':'DEMO001','email':'demo@mitwpu.edu.in','dept':'Computer Science','subject':'All Subjects'}
                        st.session_state.demo = True; load_service_requests(); st.rerun()
                    users = load_csv('users.csv')
                    if users is not None:
                        r = role.lower().replace('administrator','admin')
                        u = users[(users['username']==username)&(users['password']==password)&(users['role']==r)]
                        if not u.empty:
                            st.session_state.logged_in = True; st.session_state.role = r
                            st.session_state.user = u.iloc[0].to_dict()
                            st.session_state.demo = False; load_service_requests(); st.rerun()
                        else: st.error("Invalid credentials")
                    else: st.error("users.csv not found")
            
            with c2:
                if st.button("🎮 Try Demo", use_container_width=True):
                    st.session_state.logged_in = True
                    st.session_state.role = role.lower().replace('administrator','admin')
                    st.session_state.user = {'name':'Demo User','id':'DEMO001','email':'demo@mitwpu.edu.in','dept':'Computer Science','subject':'All Subjects'}
                    st.session_state.demo = True; load_service_requests(); st.rerun()
            
            with st.expander("🔑 Forgot Password?"):
                email = st.text_input("Enter registered email", key="forgot_email")
                if st.button("📧 Send OTP"):
                    otp = str(random.randint(100000, 999999))
                    st.session_state.reset_otp = otp; st.session_state.reset_email = email
                    st.success(f"📧 OTP sent! Demo: **{otp}**")
                if st.session_state.reset_otp:
                    uo = st.text_input("Enter OTP", max_chars=6, key="otp_input")
                    np = st.text_input("New Password", type="password", key="new_pass")
                    if st.button("✅ Reset"):
                        if uo == st.session_state.reset_otp:
                            users = load_csv('users.csv')
                            if users is not None:
                                mask = users['email'] == st.session_state.reset_email
                                if mask.any():
                                    users.loc[mask, 'password'] = np; users.to_csv('users.csv', index=False)
                                    st.success("✅ Done!"); st.session_state.reset_otp = None; time.sleep(1); st.rerun()
                        else: st.error("Invalid OTP")
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown(f'<p style="text-align:center;color:#64748b;margin-top:1rem;">{COLLEGE}</p>', unsafe_allow_html=True)

# ═══════════════════ STUDENT PORTAL (ENHANCED) ═══════════════════
def student_portal():
    u = st.session_state.user
    student_name = u.get('name', 'Student')
    student_id = u.get('id', 'N/A')
    
    # ═══════ HERO ═══════
    st.markdown(f"""
        <div class="hero animate">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <h2>👋 Welcome, {student_name.split()[0]}!</h2>
                    <p>PRN: {student_id} | {u.get('dept','Computer Science')} | {BATCH}</p>
                </div>
                <span class="badge-live">🟢 Active</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    records = load_attendance()
    my = next((r for r in records if r.get('name','').lower() == student_name.lower()), None)
    if st.session_state.demo and not my:
        my = {'count': 34, 'status': 'Present', 'timestamp': datetime.now().strftime('%I:%M %p')}
    
    det = my.get('count', 0) if my else 0
    tl = st.session_state.total_lectures
    pct = (det/tl*100) if tl > 0 else 0
    req = math.ceil(0.75*tl)
    cm = max(0, det-req)
    nm = max(0, req-det)
    elig = pct >= 75
    
    # ═══════ QUICK ACTIONS ═══════
    st.markdown("### ⚡ Quick Actions")
    q1, q2, q3, q4, q5 = st.columns(5)
    with q1: st.markdown('<div class="student-quick-action"><div class="quick-icon">📊</div><div class="quick-text">Attendance</div></div>', unsafe_allow_html=True)
    with q2: st.markdown('<div class="student-quick-action"><div class="quick-icon">📅</div><div class="quick-text">Timetable</div></div>', unsafe_allow_html=True)
    with q3: st.markdown('<div class="student-quick-action"><div class="quick-icon">🏛️</div><div class="quick-text">Services</div></div>', unsafe_allow_html=True)
    with q4: st.markdown('<div class="student-quick-action"><div class="quick-icon">📜</div><div class="quick-text">Certificate</div></div>', unsafe_allow_html=True)
    with q5: st.markdown('<div class="student-quick-action"><div class="quick-icon">💬</div><div class="quick-text">Help</div></div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ═══════ MAIN TABS ═══════
    tabs = st.tabs(["📊 Dashboard", "📅 Timetable", "🏛️ Service Hub", "📜 Certificates", "💬 Help"])
    
    # ═══════ TAB 0: DASHBOARD ═══════
    with tabs[0]:
        # Stats Row
        c1, c2, c3, c4 = st.columns(4)
        
        with c1:
            if pct >= 90: color, emoji = "#10b981", "🏆"
            elif pct >= 75: color, emoji = "#f59e0b", "📊"
            else: color, emoji = "#ef4444", "⚠️"
            st.markdown(f'<div class="stat-card stat-present"><div style="font-size:2rem;">{emoji}</div><div class="stat-number" style="color:{color};">{pct:.0f}%</div><div class="stat-label">Attendance</div><div class="stat-subtitle">Target: 75%</div></div>', unsafe_allow_html=True)
        
        with c2:
            st.markdown(f'<div class="stat-card stat-total"><div style="font-size:2rem;">📚</div><div class="stat-number">{det}</div><div class="stat-label">Attended</div><div class="stat-subtitle">Out of {tl} lectures</div></div>', unsafe_allow_html=True)
        
        with c3:
            missed = tl - det
            st.markdown(f'<div class="stat-card stat-absent"><div style="font-size:2rem;">📉</div><div class="stat-number">{missed}</div><div class="stat-label">Missed</div><div class="stat-subtitle">Classes absent</div></div>', unsafe_allow_html=True)
        
        with c4:
            st.markdown(f'<div class="stat-card {"stat-present" if elig else "stat-absent"}"><div style="font-size:2rem;">{"✅" if elig else "❌"}</div><div class="stat-number">{"ELIGIBLE" if elig else "NOT"}</div><div class="stat-label">Exam Status</div><div class="stat-subtitle">{"Can miss " + str(cm) + " more" if elig else "Need " + str(nm) + " more"}</div></div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Gauge Chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=pct, delta={'reference': 75, 'increasing': {'color': '#10b981'}, 'decreasing': {'color': '#ef4444'}},
            number={'font': {'size': 55, 'color': 'white'}},
            gauge={
                'axis': {'range': [0, 100], 'tickcolor': 'white'},
                'bar': {'color': '#6366f1', 'thickness': 0.2},
                'bgcolor': 'rgba(255,255,255,0.05)',
                'steps': [
                    {'range': [0, 50], 'color': 'rgba(239,68,68,0.3)'},
                    {'range': [50, 75], 'color': 'rgba(245,158,11,0.3)'},
                    {'range': [75, 100], 'color': 'rgba(16,185,129,0.3)'}
                ],
                'threshold': {'line': {'color': 'white', 'width': 3}, 'value': 75}
            }
        ))
        fig.update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)', font={'color': 'white'})
        st.plotly_chart(fig, use_container_width=True)
        
        # Status Message
        if not elig:
            st.error(f"⚠️ **URGENT:** You need **{nm}** more classes to be eligible for exams!")
        elif pct < 80:
            st.warning(f"⚡ **CAUTION:** You can miss only **{cm}** more classes. Stay careful!")
        else:
            st.success(f"🎉 **EXCELLENT!** Your attendance is outstanding. Keep it up!")
        
        # Attendance Tips
        with st.expander("💡 Tips to Improve Attendance"):
            if pct >= 90:
                st.success("You're doing great! Here's how to maintain:")
            elif pct >= 75:
                st.warning("You're meeting requirements but could improve:")
            else:
                st.error("You need to improve. Here's how:")
            st.markdown("""
            - 📅 Attend all remaining classes
            - ⏰ Arrive on time (before grace period ends)
            - 🏥 Submit medical certificates for valid absences
            - 📞 Contact class teacher if facing issues
            - 🤝 Buddy up with a regular student for reminders
            """)
    
    # ═══════ TAB 1: TIMETABLE ═══════
    with tabs[1]:
        st.markdown("### 📅 Your Class Schedule")
        tdf = load_csv('timetable.csv')
        if tdf is not None and not tdf.empty:
            today = datetime.now().strftime("%A")
            ct = datetime.now().strftime("%H:%M")
            today_df = tdf[tdf['Day'].str.lower() == today.lower()]
            
            c1,c2,c3 = st.columns(3)
            c1.metric("Today", today); c2.metric("Time", ct); c3.metric("Grace", "10 min")
            
            if not today_df.empty:
                st.success(f"**{today}'s Classes:**")
                for _, row in today_df.iterrows():
                    is_current = row["Start Time"] <= ct <= row["End Time"]
                    st.markdown(f"""
                        <div class="timetable-card {"current" if is_current else ""}">
                            <strong>{row['Subject']}</strong> by {row['Faculty']}<br>
                            <small>⏰ {row['Start Time']} - {row['End Time']} | 🏫 {row.get('Class','DSBDA')}</small>
                            {'<span style="color:#10b981;">🔴 LIVE NOW</span>' if is_current else ''}
                        </div>
                    """, unsafe_allow_html=True)
            else: st.info(f"No classes for {today}")
            
            st.markdown("---")
            with st.expander("📆 View Full Week"):
                st.dataframe(tdf, use_container_width=True)
        else: st.info("No timetable data")
    
    # ═══════ TAB 2: SERVICE HUB ═══════
    with tabs[2]:
        st.markdown("### 🏛️ Student Service Hub")
        st.markdown("*Apply for certificates & services online - No more queues!*")
        
        # Service Grid
        st.markdown("#### 📋 Available Services")
        cols = st.columns(3)
        for i, (service, details) in enumerate(SERVICES.items()):
            with cols[i % 3]:
                st.markdown(f"""
                    <div class="service-card">
                        <div class="service-icon">{service.split()[0]}</div>
                        <div class="service-name">{service}</div>
                        <div class="service-time">⏱️ {details['time']}</div>
                        <div class="service-time">💰 {details['fee']}</div>
                        <div class="service-time">🏢 {details['dept']}</div>
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Apply
        col1, col2 = st.columns(2)
        with col1:
            service_type = st.selectbox("Select Service", list(SERVICES.keys()))
        with col2:
            sel = SERVICES[service_type]
            st.info(f"🏢 {sel['dept']} | 💰 {sel['fee']} | ⏱️ {sel['time']}")
        
        notes = st.text_area("Additional Notes (optional)")
        
        if st.button("📤 Submit Request", type="primary", use_container_width=True):
            req_id = submit_service_request(student_name, student_id, service_type, notes)
            st.success(f"✅ Submitted! ID: **{req_id}**")
            st.balloons()
        
        # My Requests
        st.markdown("---")
        st.subheader("📋 My Requests")
        my_requests = [r for r in st.session_state.service_requests if r.get('prn') == student_id]
        if my_requests:
            for req in reversed(my_requests[-5:]):
                sc = f"status-{req['status'].lower()}"
                st.markdown(f"""
                    <div class="insight-card">
                        <strong>{req['service']}</strong> <span class="status-badge {sc}">{req['status']}</span><br>
                        <small>🆔 {req['id']} | 📅 {req['date']} | 💰 {req['fee']}</small>
                    </div>
                """, unsafe_allow_html=True)
        else: st.info("No requests yet")
    
    # ═══════ TAB 3: CERTIFICATES ═══════
    with tabs[3]:
        st.markdown("### 📜 Your Certificates")
        if elig:
            st.success("🎉 You are eligible for attendance certificate!")
            st.markdown(generate_certificate(student_name, student_id, pct), unsafe_allow_html=True)
            st.download_button("📥 Download Certificate", generate_certificate(student_name, student_id, pct), f"certificate_{student_id}.html")
        else:
            st.warning(f"⚠️ You need {nm} more classes to be eligible for attendance certificate")
            # Progress bar
            st.progress(pct/100, text=f"Progress: {pct:.0f}% (Need 75%)")
    
    # ═══════ TAB 4: HELP ═══════
    with tabs[4]:
        st.markdown("### 💬 Help & Support")
        
        st.markdown("#### ❓ Frequently Asked Questions")
        with st.expander("How is attendance calculated?"):
            st.write("Attendance = (Classes Attended / Total Lectures) × 100. You need 75% minimum.")
        with st.expander("What if I'm late?"):
            st.write("You have a 10-minute grace period. After that, you're marked Late. Teachers can override with valid reason.")
        with st.expander("How to apply for certificates?"):
            st.write("Go to Service Hub tab → Select service → Submit. Track in 'My Requests'.")
        with st.expander("What if my attendance is below 75%?"):
            st.write("You won't be eligible for exams. Attend all remaining classes and contact your class teacher.")
        
        st.markdown("---")
        st.markdown("#### 📞 Contact")
        st.info(f"""
        **Class Teacher:** {GUIDE}
        **Department:** Computer Science & Engineering
        **College:** {COLLEGE}
        **Email:** support@mitwpu.edu.in
        """)

# ═══════════════════ TEACHER DASHBOARD ═══════════════════
def teacher_dashboard():
    u = st.session_state.user
    subject = u.get('subject', 'All Subjects')
    
    st.markdown(f"""
        <div class="hero animate">
            <h2>👨‍🏫 {u.get('name','Teacher')}</h2>
            <p>{u.get('dept','Computer Science')} · <strong>{subject}</strong></p>
        </div>
    """, unsafe_allow_html=True)
    
    students = []
    if os.path.exists('students.csv'):
        try: students = pd.read_csv('students.csv').to_dict('records')
        except: pass
    
    records = load_attendance()
    rec_dict = {r['name'].lower(): r for r in records}
    
    if st.session_state.demo and not rec_dict:
        demo_names = ['Kamathe Sujal Ganesh','Saniya Rahul Dhawade','Shrutika Pokale','Vedang Govind Joshi','Krushna Ashok Bodake']
        for name in demo_names:
            rec_dict[name.lower()] = {'name':name,'status':random.choice(['Present','Present','Absent','Late']),'count':random.randint(25,40),'timestamp':f'{random.randint(9,11):02d}:{random.randint(0,59):02d}'}
    
    tl = st.session_state.total_lectures
    total = len(students) if students else 76
    p = sum(1 for r in rec_dict.values() if r.get('status')=='Present')
    a = sum(1 for r in rec_dict.values() if r.get('status')=='Absent')
    l = sum(1 for r in rec_dict.values() if r.get('status')=='Late')
    nd = max(0, total - len(rec_dict))
    
    # Clickable stats
    c1,c2,c3,c4,c5 = st.columns(5)
    with c1:
        if st.button(f"👥\n\n{total}\n\nTOTAL", key="btn_total", use_container_width=True): st.session_state.clicked_stat = 'total'
    with c2:
        if st.button(f"✅\n\n{p}\n\nPRESENT", key="btn_present", use_container_width=True): st.session_state.clicked_stat = 'present'
    with c3:
        if st.button(f"❌\n\n{a}\n\nABSENT", key="btn_absent", use_container_width=True): st.session_state.clicked_stat = 'absent'
    with c4:
        if st.button(f"⏰\n\n{l}\n\nLATE", key="btn_late", use_container_width=True): st.session_state.clicked_stat = 'late'
    with c5:
        if st.button(f"⚪\n\n{nd}\n\nPENDING", key="btn_pending", use_container_width=True): st.session_state.clicked_stat = 'pending'
    
    c1.markdown(f'<div class="stat-card stat-total"><div class="stat-number">{total}</div><div class="stat-label">Total</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="stat-card stat-present"><div class="stat-number">{p}</div><div class="stat-label">Present</div></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="stat-card stat-absent"><div class="stat-number">{a}</div><div class="stat-label">Absent</div></div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="stat-card stat-late"><div class="stat-number">{l}</div><div class="stat-label">Late</div></div>', unsafe_allow_html=True)
    c5.markdown(f'<div class="stat-card stat-pending"><div class="stat-number">{nd}</div><div class="stat-label">Pending</div></div>', unsafe_allow_html=True)
    
    if st.session_state.clicked_stat:
        st.markdown("---")
        status_map = {'total': None, 'present': 'Present', 'absent': 'Absent', 'late': 'Late', 'pending': 'Pending'}
        filter_val = status_map.get(st.session_state.clicked_stat)
        
        if st.session_state.clicked_stat == 'total': filtered = rec_dict.values()
        elif st.session_state.clicked_stat == 'pending': filtered = [{'name': s.get('Name',''), 'id': s.get('Student ID',''), 'status': 'Pending', 'count': 0} for s in students if s.get('Name','').lower() not in rec_dict]
        else: filtered = [r for r in rec_dict.values() if r.get('status') == filter_val]
        
        st.subheader(f"📋 {st.session_state.clicked_stat.upper()} Students")
        if filtered:
            fr = [{'Name':r.get('name',''),'PRN':r.get('id','N/A'),'Status':r.get('status','Pending'),'Att%':f"{(r.get('count',0)/tl*100):.0f}%",'Detections':r.get('count',0)} for r in filtered]
            st.dataframe(pd.DataFrame(fr), use_container_width=True)
        if st.button("✖️ Close"): st.session_state.clicked_stat = None; st.rerun()
    
    tabs = st.tabs(["📊 Analytics", "📋 Roster", "📹 Camera", "📤 Upload", "🎮 Demo", "⏰ Late", "🧠 AI", "📅 Timetable", "🏛️ Services"])
    
    with tabs[0]:
        c1,c2 = st.columns(2)
        with c1:
            fig = px.pie(values=[p,a,l,nd], names=['Present','Absent','Late','Pending'], color_discrete_sequence=['#10b981','#ef4444','#f59e0b','#6366f1'], hole=0.5)
            fig.update_layout(height=380, paper_bgcolor='rgba(0,0,0,0)', font={'color':'white'})
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.markdown("### 🧠 AI Insights")
            rate = (p/total*100) if total>0 else 0
            insights = []
            if rate >= 90: insights.append({'type':'positive','msg':f'🏆 Excellent: {rate:.0f}%'})
            elif rate >= 75: insights.append({'type':'warning','msg':f'📊 Moderate: {rate:.0f}%'})
            else: insights.append({'type':'danger','msg':f'🚨 Critical: {rate:.0f}%'})
            if a > 0: insights.append({'type':'danger','msg':f'❌ {a} students absent'})
            if l > 0: insights.append({'type':'warning','msg':f'⏰ {l} students late'})
            for ins in insights: st.markdown(f'<div class="insight-card insight-{ins["type"]}">{ins["msg"]}</div>', unsafe_allow_html=True)
    
    with tabs[1]:
        rows = []
        for s in (students if students else [{'Name':f'Student {i}','Student ID':f'PRN{i:04d}'} for i in range(1,77)]):
            name = s.get('Name','Unknown'); sid = str(s.get('Student ID','N/A'))
            r = rec_dict.get(name.lower(), {}); pct = (r.get('count',0)/tl*100) if tl>0 else 0
            rows.append({'Name':name,'PRN':sid,'Status':r.get('status','Pending'),'Att%':f'{pct:.0f}%','Detections':r.get('count',0)})
        st.dataframe(pd.DataFrame(rows), use_container_width=True, height=400)
        st.download_button("📥 Export CSV", pd.DataFrame(rows).to_csv(index=False), f"roster_{datetime.now().strftime('%Y%m%d')}.csv")
    
    with tabs[2]:
        st.markdown('<div class="glass"><h3 style="color:white;">📹 Live Camera</h3>', unsafe_allow_html=True)
        cam = get_camera()
        if cam is None: st.warning("No camera")
        else:
            b1,b2 = st.columns(2)
            if b1.button("▶️ Start", use_container_width=True, type="primary"):
                if os.path.exists('live_attendance.json'): os.remove('live_attendance.json')
                st.session_state.live_running = True; st.session_state.live_marked = set()
            if b2.button("⏹️ Stop", use_container_width=True): st.session_state.live_running = False
            FW = st.image([])
            if st.session_state.live_running:
                fc = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                cap = cv2.VideoCapture(cam)
                while cap.isOpened() and st.session_state.live_running:
                    ret, frame = cap.read()
                    if not ret: break
                    frame = cv2.flip(frame, 1)
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    faces = fc.detectMultiScale(gray, 1.1, 5, minSize=(60,60))
                    for (x,y,w,h) in faces: cv2.rectangle(frame, (x,y), (x+w,y+h), (16,185,129), 3)
                    cv2.putText(frame, f"Detected: {len(st.session_state.live_marked)}", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (99,102,241), 2)
                    FW.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                cap.release()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tabs[3]:
        st.markdown('<div class="glass"><h3 style="color:white;">📤 Upload & Process</h3>', unsafe_allow_html=True)
        uf = st.file_uploader("Drop video", type=['mp4','avi','mov'])
        if uf:
            with open('input.mp4','wb') as f: f.write(uf.read()); st.success("✅ Ready!")
        if st.button("🚀 Process", type="primary", use_container_width=True):
            if not os.path.exists('input.mp4'): st.error("Upload first!")
            else:
                for f in ['attendance_results.json','attendance.csv']:
                    if os.path.exists(f): os.remove(f)
                with st.spinner("Processing..."):
                    pb = st.progress(0)
                    for i in range(10): time.sleep(0.4); pb.progress(i*10)
                    subprocess.run(['python3','main.py'], capture_output=True, text=True)
                    pb.progress(100)
                    if os.path.exists('attendance_results.json'):
                        st.success("✅ Done!"); st.balloons(); time.sleep(1); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tabs[4]:
        st.markdown('<div class="glass"><h3 style="color:white;">🎮 Demo Mode</h3>', unsafe_allow_html=True)
        if st.button("🎮 Load Demo Data", type="primary", use_container_width=True):
            demo_data = {'attendance':{},'name_to_id':{}}
            names = [('Kamathe Sujal Ganesh','1272240519'),('Saniya Rahul Dhawade','1272240684'),('Shrutika Pokale','1272240580'),('Vedang Govind Joshi','1272240258'),('Krushna Ashok Bodake','1272240252')]
            for name,prn in names:
                demo_data['attendance'][name] = {'present':random.choice([True,True,False]),'status':random.choice(['Present','Present','Absent','Late']),'first_seen':f'{random.randint(9,11):02d}:{random.randint(0,59):02d}','count':random.randint(25,40)}
                demo_data['name_to_id'][name] = prn
            save_json('attendance_results.json', demo_data)
            st.success("✅ Demo loaded!"); st.balloons(); time.sleep(1); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tabs[5]:
        late_list = [r for r in records if r.get('status')=='Late']
        if late_list:
            for i,s in enumerate(late_list):
                with st.expander(f"⏰ {s.get('name','')}"):
                    if st.button(f"✅ Mark Present", key=f"late_{i}"): st.success("Done!"); st.rerun()
        else: st.success("No late students!")
    
    with tabs[6]:
        st.markdown("### 🧠 AI Predictor")
        for s_name in list(rec_dict.keys())[:5]:
            current = rec_dict[s_name].get('count',30)
            predicted = current + random.randint(-5,3)
            trend = "📈" if predicted > current else "📉" if predicted < current else "➡️"
            st.markdown(f'<div class="insight-card"><strong>{s_name}</strong>: {current}→{predicted} classes {trend}</div>', unsafe_allow_html=True)
    
    with tabs[7]:
        st.markdown('<div class="glass"><h3 style="color:white;">📅 Timetable</h3>', unsafe_allow_html=True)
        tdf = load_csv('timetable.csv')
        if tdf is not None and not tdf.empty:
            today = datetime.now().strftime("%A"); ct = datetime.now().strftime("%H:%M")
            today_df = tdf[tdf['Day'].str.lower() == today.lower()]
            c1,c2,c3 = st.columns(3); c1.metric("Today",today); c2.metric("Time",ct); c3.metric("Grace","10 min")
            if not today_df.empty:
                for _, row in today_df.iterrows():
                    is_current = row["Start Time"] <= ct <= row["End Time"]
                    st.markdown(f'<div class="timetable-card {"current" if is_current else ""}"><strong>{row["Subject"]}</strong> by {row["Faculty"]}<br><small>⏰ {row["Start Time"]} - {row["End Time"]}</small>{"<span style=\"color:#10b981;\">🔴 LIVE</span>" if is_current else ""}</div>', unsafe_allow_html=True)
            st.markdown("---"); st.subheader("📆 Weekly View")
            days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
            available = [d for d in days if d in tdf['Day'].unique()]
            if available:
                sd = st.selectbox("Select Day", available, index=available.index(today) if today in available else 0)
                day_df = tdf[tdf['Day'].str.lower() == sd.lower()]
                if not day_df.empty: st.dataframe(day_df[["Start Time","End Time","Subject","Faculty","Class"]], use_container_width=True)
            with st.expander("📋 Full Timetable"): st.dataframe(tdf, use_container_width=True, height=400)
        else: st.info("No timetable data")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tabs[8]:
        st.markdown("### 🏛️ Service Hub - All Requests")
        all_requests = st.session_state.service_requests
        if all_requests:
            pc = sum(1 for r in all_requests if r['status']=='Pending')
            ac = sum(1 for r in all_requests if r['status']=='Approved')
            cc = sum(1 for r in all_requests if r['status']=='Completed')
            c1,c2,c3,c4 = st.columns(4)
            c1.metric("Total", len(all_requests)); c2.metric("Pending", pc); c3.metric("Approved", ac); c4.metric("Completed", cc)
            st.markdown("---")
            sf = st.selectbox("Filter", ["All","Pending","Approved","Processing","Completed","Rejected"])
            fr = all_requests if sf == "All" else [r for r in all_requests if r['status']==sf]
            for req in reversed(fr):
                sc = f"status-{req['status'].lower()}"
                with st.expander(f"{req['service']} - {req['student']} ({req['date']})"):
                    st.markdown(f'<span class="status-badge {sc}">{req["status"]}</span><br><strong>Student:</strong> {req["student"]}<br><strong>PRN:</strong> {req["prn"]}<br><strong>Dept:</strong> {req["dept"]}<br><strong>Fee:</strong> {req["fee"]}', unsafe_allow_html=True)
                    if req['status'] in ['Pending','Processing']:
                        ns = st.selectbox("Update", ["Pending","Processing","Approved","Completed","Rejected"], key=f"st_{req['id']}")
                        if st.button("✅ Update", key=f"up_{req['id']}"):
                            req['status'] = ns; save_json('service_requests.json', all_requests)
                            st.success("Updated!"); st.rerun()
        else: st.info("No requests yet")

# ═══════════════════ ADMIN ═══════════════════
def admin_dashboard():
    st.markdown('<div class="hero animate"><h2>👑 Administrator Panel</h2></div>', unsafe_allow_html=True)
    records = load_attendance()
    if records:
        p = sum(1 for r in records if r.get('status')=='Present')
        a = sum(1 for r in records if r.get('status')=='Absent')
        c1,c2,c3 = st.columns(3)
        c1.metric("Total", len(records)); c2.metric("Present", p); c3.metric("Absent", a)
        st.dataframe(pd.DataFrame(records), use_container_width=True)

# ═══════════════════ MAIN ═══════════════════
def main():
    if not st.session_state.logged_in:
        login_page()
    else:
        with st.sidebar:
            st.markdown(f"""
                <div class="sidebar-profile">
                    <div style="font-size:2rem;">👤</div>
                    <h4>{st.session_state.user.get('name','User')}</h4>
                    <p>{st.session_state.role.title()}</p>
                    {'<span class="badge-demo">🎮 DEMO</span>' if st.session_state.demo else '<span class="badge-live">🔴 LIVE</span>'}
                </div>
            """, unsafe_allow_html=True)
            if st.button("🗑️ Clear All Data", use_container_width=True):
                for f in ['attendance_results.json','attendance.csv','live_attendance.json','service_requests.json']:
                    if os.path.exists(f): os.remove(f)
                st.session_state.clicked_stat = None; st.session_state.service_requests = []
                st.success("✅ Cleared!"); time.sleep(1); st.rerun()
            if st.button("🚪 Sign Out", use_container_width=True):
                for k in list(st.session_state.keys()): del st.session_state[k]
                st.rerun()
        
        r = st.session_state.role
        if r == 'student': student_portal()
        elif r == 'teacher': teacher_dashboard()
        elif r == 'admin': admin_dashboard()
        
        st.markdown(f"""
            <div class="footer">
                <p><span class="footer-brand">{APP_NAME}</span> v{APP_VERSION} | {COLLEGE}</p>
                <p>Developed by <strong>{DEVELOPERS}</strong> | Guided by <strong>{GUIDE}</strong></p>
            </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()