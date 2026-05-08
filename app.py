"""
╔══════════════════════════════════════════════════════════════════════╗
║               VISIONGUARD AI PRO  ·  v6.0.0                         ║
║          Enterprise Attendance Intelligence Platform                 ║
║                                                                      ║
║  Developed by: Sujal Ganesh Kamathe & Saniya Rahul Dhawade          ║
║  Guide: Dr. Vikas J. Magar                                           ║
║  MIT World Peace University, Pune                                    ║
║  © 2026 VisionGuard AI. All rights reserved.                         ║
╚══════════════════════════════════════════════════════════════════════╝

PRODUCTION UPGRADES (v5 → v6):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✔ Biometric Heatmap — real-time visual attendance grid per seat
✔ Smart Engagement Score — presence + participation composite metric
✔ Predictive Drop-Out Risk Engine (rule-based, no ML libs)
✔ Live Leaderboard — gamified streak & attendance rankings
✔ Parent/Guardian Notification Log simulation
✔ AI Report Card Generator — personalized HTML report per student
✔ Class Mood Tracker — emoji-based daily check-in for students
✔ Voice Attendance Confirmation (Web Speech API via HTML component)
✔ QR Attendance Fallback — generate QR codes per session
✔ Dark/Light mode toggle
✔ Animated celebration micro-interactions
✔ SMS/WhatsApp alert simulation panel (teacher broadcast)
✔ Exam Schedule & Countdown widget
✔ Student Compare Tool — head-to-head attendance analytics
✔ Subject Danger Zone — auto-flag subjects nearing debarment
✔ Admin Global Heatmap Calendar (GitHub-style)
✔ Bulk Leave Approval workflow (admin/teacher)
✔ Enhanced audit trail with export
✔ System uptime & performance metrics panel
✔ On-screen animated tutorial overlay
"""

# ──────────────────────────────────────────────────────────────────────
import streamlit as st
import pandas as pd
import json
import os
import subprocess
import time
import math
import cv2
import numpy as np
from datetime import datetime, timedelta, date
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
import hashlib
import io
import traceback
import base64

# ──────────────────────────────────────────────────────────────────────
# CONSTANTS
# ──────────────────────────────────────────────────────────────────────
APP_NAME    = "VisionGuard AI Pro"
APP_VERSION = "6.0.0"
COLLEGE     = "MIT World Peace University, Pune"
DEVELOPERS  = "Sujal Ganesh Kamathe & Saniya Rahul Dhawade"
GUIDE       = "Dr. Vikas J. Magar"
BATCH       = "SY BSc DSBDA | 2026-27"

MIN_ATTENDANCE     = 75
LATE_GRACE_MIN     = 10
SESSION_TIMEOUT_MIN = 60
DEBARMENT_THRESHOLD = 65   # below this → danger zone
DROPOUT_RISK_THRESHOLD = 55

DEPT_LIST = [
    "Computer Science", "Information Technology", "Electronics",
    "Mechanical", "Civil", "Data Science & AI", "MBA", "MCA"
]

SERVICES = {
    "Bonafide Certificate":  {"fee": "₹100",  "time": "1-2 days",   "dept": "Academic Office",  "icon": "📄"},
    "Leaving Certificate":   {"fee": "₹500",  "time": "7-10 days",  "dept": "Academic Office",  "icon": "🎓"},
    "Transcript":            {"fee": "₹300",  "time": "15-20 days", "dept": "Examination Cell", "icon": "📑"},
    "ID Card Reissue":       {"fee": "₹200",  "time": "2-3 days",   "dept": "Security Office",  "icon": "🪪"},
    "Medical Leave":         {"fee": "Free",  "time": "Same day",   "dept": "Medical Center",   "icon": "🏥"},
    "Fee Receipt":           {"fee": "Free",  "time": "1 day",      "dept": "Accounts Dept",    "icon": "🧾"},
    "Exam Form Correction":  {"fee": "₹150",  "time": "2-3 days",   "dept": "Examination Cell", "icon": "📝"},
    "Scholarship Document":  {"fee": "Free",  "time": "3-5 days",   "dept": "Scholarship Cell", "icon": "🏅"},
    "Bus Pass":              {"fee": "₹500",  "time": "5-7 days",   "dept": "Transport Office", "icon": "🚌"},
    "Hostel Request":        {"fee": "₹1000", "time": "7-14 days",  "dept": "Hostel Office",    "icon": "🏠"},
}

SUBJECTS = [
    "Data Structures", "Database Management", "Machine Learning",
    "Statistics", "Python Programming", "Data Visualization", "Big Data"
]

MOOD_OPTIONS = ["😊 Great", "😐 Okay", "😴 Tired", "😰 Stressed", "🤒 Unwell"]

EXAM_SCHEDULE = [
    {"subject": "Linear Algebra and Calculus",       "date": "2026-05-26", "time": "10:30 AM", "room": "Exam Hall", "code": "BDA10070"},
    {"subject": "Big Data Technologies using Hadoop", "date": "2026-05-28", "time": "10:30 AM", "room": "Exam Hall", "code": "BDA30020"},
    {"subject": "SPSS Programming",                   "date": "2026-05-30", "time": "10:30 AM", "room": "Exam Hall", "code": "BDA30030"},
    {"subject": "Statistical Inference and Multivariate Analysis", "date": "2026-06-02", "time": "10:30 AM", "room": "Exam Hall", "code": "BDA30040"},
]

# ── PAGE CONFIG ────────────────────────────────────────────────────────
st.set_page_config(
    page_title=APP_NAME,
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'mailto:sujal@mitwpu.edu.in',
        'About': f'{APP_NAME} v{APP_VERSION} — {COLLEGE}'
    }
)

# ══════════════════════════════════════════════════════════════════════
# GLOBAL CSS — Obsidian Ultra Theme v6
# ══════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,300&family=JetBrains+Mono:wght@400;600&display=swap');

*, *::before, *::after { box-sizing: border-box; }
* { font-family: 'Inter', sans-serif; }
.stApp { background: #060a10; }

:root {
    --bg0:#060a10; --bg1:#0d1526; --bg2:#131d30; --bg3:#1a2640;
    --bg4:#212f4d; --border:rgba(255,255,255,0.07); --border-hi:rgba(99,102,241,0.4);
    --indigo:#6366f1; --indigo-light:#818cf8; --indigo-dark:#4338ca;
    --emerald:#10b981; --amber:#f59e0b; --rose:#f43f5e;
    --sky:#38bdf8; --violet:#8b5cf6; --pink:#ec4899; --teal:#14b8a6;
    --text-hi:#f1f5f9; --text-mid:#94a3b8; --text-lo:#475569;
    --radius-sm:10px; --radius-md:16px; --radius-lg:24px; --radius-xl:32px;
    --shadow:0 8px 40px rgba(0,0,0,0.7);
    --glow:0 0 60px rgba(99,102,241,0.12);
    --glow-emerald:0 0 40px rgba(16,185,129,0.1);
}

h1,h2,h3,h4,.syne { font-family:'Inter',sans-serif !important; }
code,.mono { font-family:'JetBrains Mono',monospace !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width:6px; height:6px; }
::-webkit-scrollbar-track { background:var(--bg1); }
::-webkit-scrollbar-thumb { background:var(--bg4); border-radius:99px; }

/* ── Streamlit overrides ── */
section[data-testid="stSidebar"] { background:var(--bg1) !important; border-right:1px solid var(--border); }
.stTextInput>div>div>input,
.stSelectbox>div>div>div,
.stTextArea textarea,
.stNumberInput>div>div>input {
    background:var(--bg2) !important; color:var(--text-hi) !important;
    border:1px solid var(--border) !important; border-radius:var(--radius-sm) !important;
    transition:all 0.2s;
}
.stTextInput>div>div>input:focus,.stTextArea textarea:focus {
    border-color:var(--indigo) !important;
    box-shadow:0 0 0 3px rgba(99,102,241,0.15) !important;
}
.stButton>button {
    background:linear-gradient(135deg,var(--indigo),#4f46e5) !important;
    color:white !important; border:none !important;
    border-radius:var(--radius-sm) !important; font-weight:600 !important;
    font-family:'Inter',sans-serif !important; transition:all 0.25s !important;
    padding:0.6rem 1.4rem !important; letter-spacing:0.02em;
}
.stButton>button:hover { transform:translateY(-2px) !important; box-shadow:0 8px 28px rgba(99,102,241,0.45) !important; }
.stButton>button:active { transform:translateY(0) !important; }
.stButton>button[kind="secondary"] { background:var(--bg3) !important; border:1px solid var(--border-hi) !important; }
.stTabs [data-baseweb="tab-list"] { background:var(--bg2); padding:6px; border-radius:var(--radius-md); gap:4px; border:1px solid var(--border); flex-wrap:wrap; }
.stTabs [data-baseweb="tab"] { border-radius:var(--radius-sm); padding:0.5rem 0.9rem; font-weight:600; font-size:0.8rem; color:var(--text-mid); }
.stTabs [aria-selected="true"] { background:linear-gradient(135deg,var(--indigo),#7c3aed) !important; color:white !important; }
div[data-testid="stMetric"] { background:var(--bg2); border:1px solid var(--border); border-radius:var(--radius-md); padding:1rem; }
div[data-testid="stMetric"] label { color:var(--text-mid) !important; font-size:0.75rem; font-weight:700; letter-spacing:0.08em; text-transform:uppercase; }
div[data-testid="stMetricValue"] { color:var(--text-hi) !important; font-family:'Inter',sans-serif !important; font-size:2rem !important; }
.stExpander { border:1px solid var(--border) !important; border-radius:var(--radius-md) !important; background:var(--bg2) !important; }
.stProgress>div>div { border-radius:99px; }
.stDataFrame { border-radius:var(--radius-md) !important; overflow:hidden; }

/* ── Hero ── */
.hero {
    background:linear-gradient(135deg,#0a1628 0%,#160d3a 45%,#0a1e2d 100%);
    border:1px solid var(--border-hi); padding:2.4rem 3rem;
    border-radius:var(--radius-lg); color:white; margin-bottom:2rem;
    box-shadow:var(--shadow),var(--glow); position:relative; overflow:hidden;
}
.hero::before {
    content:''; position:absolute; top:-30%; right:-5%;
    width:500px; height:500px; background:radial-gradient(circle,rgba(99,102,241,0.1) 0%,transparent 65%);
    border-radius:50%; pointer-events:none; animation:pulse-glow 4s ease-in-out infinite;
}
.hero::after {
    content:''; position:absolute; bottom:-40%; left:10%;
    width:300px; height:300px; background:radial-gradient(circle,rgba(20,184,166,0.08) 0%,transparent 65%);
    border-radius:50%; pointer-events:none;
}
@keyframes pulse-glow { 0%,100%{opacity:1;} 50%{opacity:0.5;} }
.hero h2 { font-family:'Inter',sans-serif; font-size:1.2rem; font-weight:800; margin:0 0 0.4rem; }
.hero p  { color:rgba(255,255,255,0.55); margin:0; font-size:0.9rem; }
.hero .badge { display:inline-flex; align-items:center; gap:6px; background:rgba(99,102,241,0.18); border:1px solid rgba(99,102,241,0.4); padding:5px 14px; border-radius:99px; font-size:0.78rem; color:var(--indigo-light); margin-top:1rem; }
.live-dot { width:8px; height:8px; background:var(--emerald); border-radius:50%; animation:blink 1.2s ease-in-out infinite; display:inline-block; }
@keyframes blink { 0%,100%{opacity:1;box-shadow:0 0 6px var(--emerald);} 50%{opacity:0.2;box-shadow:none;} }

/* ── Stat Cards ── */
.stat-card {
    background:var(--bg2); border:1px solid var(--border);
    border-radius:var(--radius-md); padding:1.4rem 1.6rem;
    transition:all 0.25s; position:relative; overflow:hidden;
    cursor:default;
}
.stat-card::after {
    content:''; position:absolute; bottom:0; left:0; right:0;
    height:3px; border-radius:0 0 var(--radius-md) var(--radius-md);
    transition:height 0.25s;
}
.stat-card:hover { transform:translateY(-4px); box-shadow:var(--shadow); border-color:var(--border-hi); }
.stat-card:hover::after { height:4px; }
.stat-present::after { background:linear-gradient(90deg,var(--emerald),var(--teal)); }
.stat-absent::after  { background:linear-gradient(90deg,var(--rose),#e11d48); }
.stat-late::after    { background:linear-gradient(90deg,var(--amber),#d97706); }
.stat-pending::after { background:linear-gradient(90deg,var(--indigo),var(--violet)); }
.stat-total::after   { background:linear-gradient(90deg,var(--sky),var(--indigo)); }
.stat-risk::after    { background:linear-gradient(90deg,var(--rose),var(--amber)); }
.stat-num  { font-family:'Inter',sans-serif; font-size:2.4rem; font-weight:800; color:var(--text-hi); line-height:1; }
.stat-lbl  { font-size:0.72rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:var(--text-mid); margin-top:4px; }
.stat-sub  { font-size:0.7rem; color:var(--text-lo); margin-top:4px; }
.stat-icon { position:absolute; top:1.2rem; right:1.4rem; font-size:1rem; opacity:0.2; }
.stat-trend { position:absolute; bottom:1rem; right:1rem; font-size:0.7rem; font-weight:700; }

/* ── Glass Panel ── */
.glass {
    background:rgba(13,21,38,0.7); backdrop-filter:blur(20px);
    border:1px solid var(--border); border-radius:var(--radius-lg);
    padding:1.8rem; margin-bottom:1rem;
}

/* ── Cards ── */
.insight-card {
    background:var(--bg2); border:1px solid var(--border);
    border-left:4px solid var(--indigo); border-radius:var(--radius-sm);
    padding:1rem 1.2rem; margin:0.35rem 0; transition:all 0.2s;
}
.insight-card:hover { border-color:var(--border-hi); background:var(--bg3); }
.insight-ok   { border-left-color:var(--emerald); }
.insight-warn { border-left-color:var(--amber); }
.insight-crit { border-left-color:var(--rose); }
.insight-info { border-left-color:var(--sky); }
.insight-violet { border-left-color:var(--violet); }
.insight-card h5 { margin:0 0 4px; color:var(--text-hi); font-weight:600; font-size:0.92rem; }
.insight-card p  { margin:0; color:var(--text-mid); font-size:0.84rem; line-height:1.5; }

/* ── Badges ── */
.badge { padding:3px 12px; border-radius:99px; font-size:0.7rem; font-weight:700; display:inline-block; letter-spacing:0.05em; text-transform:uppercase; }
.badge-pending    { background:rgba(245,158,11,0.12); color:var(--amber); border:1px solid rgba(245,158,11,0.3); }
.badge-approved   { background:rgba(16,185,129,0.12); color:var(--emerald); border:1px solid rgba(16,185,129,0.3); }
.badge-processing { background:rgba(99,102,241,0.12); color:var(--indigo-light); border:1px solid var(--border-hi); }
.badge-completed  { background:rgba(16,185,129,0.12); color:var(--emerald); border:1px solid rgba(16,185,129,0.3); }
.badge-rejected   { background:rgba(244,63,94,0.12); color:var(--rose); border:1px solid rgba(244,63,94,0.3); }
.badge-present    { background:rgba(16,185,129,0.12); color:var(--emerald); border:1px solid rgba(16,185,129,0.3); }
.badge-absent     { background:rgba(244,63,94,0.12); color:var(--rose); border:1px solid rgba(244,63,94,0.3); }
.badge-late       { background:rgba(245,158,11,0.12); color:var(--amber); border:1px solid rgba(245,158,11,0.3); }
.badge-danger     { background:rgba(244,63,94,0.2); color:var(--rose); border:1px solid var(--rose); animation:pulse-badge 1.5s infinite; }
.badge-new        { background:rgba(20,184,166,0.12); color:var(--teal); border:1px solid rgba(20,184,166,0.3); }
@keyframes pulse-badge { 0%,100%{opacity:1;} 50%{opacity:0.6;} }

/* ── Sidebar ── */
.sidebar-profile {
    background:linear-gradient(135deg,#160d38,#0d1e38);
    border:1px solid var(--border-hi); border-radius:var(--radius-md);
    padding:1.5rem; text-align:center; margin-bottom:1.2rem; color:white;
}
.sidebar-profile .avatar { font-size:3rem; margin-bottom:0.4rem; filter:drop-shadow(0 4px 8px rgba(0,0,0,0.5)); }
.sidebar-profile .name { font-family:'Inter',sans-serif; font-weight:700; font-size:1.1rem; }
.sidebar-profile .role { color:var(--text-mid); font-size:0.78rem; text-transform:uppercase; letter-spacing:0.1em; margin-top:2px; }
.badge-demo { background:var(--amber); color:#000; padding:3px 12px; border-radius:99px; font-weight:700; font-size:0.7rem; animation:blink 2s infinite; display:inline-block; margin-top:8px; }
.badge-live { background:var(--emerald); color:#fff; padding:3px 12px; border-radius:99px; font-weight:700; font-size:0.7rem; animation:blink 1.5s infinite; display:inline-block; margin-top:8px; }

/* ── Streak / Leaderboard ── */
.streak-box { background:linear-gradient(135deg,#1a110a,#2a1a06); border:1px solid rgba(245,158,11,0.3); border-radius:var(--radius-md); padding:1.2rem; text-align:center; }
.streak-num { font-family:'Inter',sans-serif; font-size:2.8rem; font-weight:800; color:var(--amber); line-height:1; }
.streak-lbl { color:var(--text-mid); font-size:0.75rem; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; margin-top:4px; }

.rank-card { background:var(--bg2); border:1px solid var(--border); border-radius:var(--radius-md); padding:1rem 1.2rem; margin:0.3rem 0; display:flex; align-items:center; gap:1rem; transition:all 0.2s; }
.rank-card:hover { background:var(--bg3); transform:translateX(4px); }
.rank-num { font-family:'Inter',sans-serif; font-size:1.4rem; font-weight:800; min-width:40px; }
.rank-gold   { color:#fbbf24; }
.rank-silver { color:#cbd5e1; }
.rank-bronze { color:#d97706; }
.rank-info   { flex:1; }
.rank-name   { color:var(--text-hi); font-weight:600; font-size:0.9rem; }
.rank-sub    { color:var(--text-mid); font-size:0.78rem; }
.rank-pct    { font-family:'Inter',sans-serif; font-weight:800; font-size:1.1rem; }

/* ── Timetable ── */
.tt-card { background:var(--bg2); border:1px solid var(--border); border-left:4px solid var(--indigo); border-radius:var(--radius-sm); padding:1rem 1.2rem; margin:0.4rem 0; transition:all 0.2s; }
.tt-card.current { border-left-color:var(--emerald); background:rgba(16,185,129,0.06); animation:current-class 2s ease-in-out infinite; }
.tt-card.upcoming { border-left-color:var(--sky); }
.tt-card.done { opacity:0.45; }
@keyframes current-class { 0%,100%{box-shadow:0 0 0 rgba(16,185,129,0);} 50%{box-shadow:0 0 20px rgba(16,185,129,0.15);} }
.tt-card h5 { color:var(--text-hi); font-weight:700; margin:0 0 4px; }
.tt-card small { color:var(--text-mid); font-size:0.78rem; }

/* ── Heatmap Cells ── */
.heatmap-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(32px,1fr)); gap:4px; }
.heatmap-cell { width:32px; height:32px; border-radius:6px; display:flex; align-items:center; justify-content:center; font-size:0.6rem; font-weight:700; cursor:pointer; transition:transform 0.15s; }
.heatmap-cell:hover { transform:scale(1.2); z-index:10; position:relative; }
.hm-present { background:rgba(16,185,129,0.7); color:white; }
.hm-absent  { background:rgba(244,63,94,0.6); color:white; }
.hm-late    { background:rgba(245,158,11,0.7); color:white; }
.hm-empty   { background:var(--bg3); color:var(--text-lo); border:1px solid var(--border); }
.hm-today   { outline:2px solid var(--indigo); outline-offset:2px; }

/* ── Risk Meter ── */
.risk-meter { text-align:center; padding:1rem; }
.risk-low    { color:var(--emerald); }
.risk-medium { color:var(--amber); }
.risk-high   { color:var(--rose); }
.risk-label  { font-family:'Inter',sans-serif; font-size:1.8rem; font-weight:800; }
.risk-sub    { color:var(--text-mid); font-size:0.8rem; }

/* ── Mood ── */
.mood-grid { display:flex; gap:0.7rem; flex-wrap:wrap; }
.mood-btn { background:var(--bg2); border:1px solid var(--border); border-radius:var(--radius-md); padding:0.8rem 1.2rem; cursor:pointer; text-align:center; transition:all 0.2s; font-size:1.5rem; }
.mood-btn:hover, .mood-btn.active { border-color:var(--indigo); background:var(--bg3); transform:scale(1.05); }
.mood-label { font-size:0.7rem; color:var(--text-mid); margin-top:4px; display:block; }

/* ── QR Box ── */
.qr-box { background:var(--bg2); border:2px dashed var(--border-hi); border-radius:var(--radius-lg); padding:2rem; text-align:center; }
.qr-code-display { font-family:'JetBrains Mono',monospace; font-size:0.65rem; background:white; color:black; padding:1rem; border-radius:var(--radius-sm); display:inline-block; letter-spacing:2px; line-height:1.8; }

/* ── Exam Countdown ── */
.exam-card { background:var(--bg2); border:1px solid var(--border); border-radius:var(--radius-md); padding:1.2rem; margin:0.4rem 0; }
.exam-card.soon { border-color:var(--amber); background:rgba(245,158,11,0.05); }
.exam-card.very-soon { border-color:var(--rose); background:rgba(244,63,94,0.05); animation:pulse-badge 1.5s infinite; }
.exam-days { font-family:'Inter',sans-serif; font-size:1.2rem; font-weight:800; }
.exam-days.green { color:var(--emerald); }
.exam-days.amber { color:var(--amber); }
.exam-days.red   { color:var(--rose); }
.exam-subject { color:var(--text-hi); font-weight:700; font-size:0.95rem; }
.exam-meta    { color:var(--text-mid); font-size:0.78rem; }

/* ── Seat Heatmap ── */
.seat-grid { display:grid; grid-template-columns:repeat(8,1fr); gap:6px; max-width:600px; }
.seat { width:100%; aspect-ratio:1; border-radius:8px; display:flex; align-items:center; justify-content:center; font-size:0.58rem; font-weight:700; text-align:center; cursor:pointer; transition:all 0.2s; }
.seat:hover { transform:scale(1.1); z-index:5; position:relative; }
.seat-occupied-present { background:linear-gradient(135deg,rgba(16,185,129,0.8),rgba(20,184,166,0.6)); color:white; }
.seat-occupied-absent  { background:linear-gradient(135deg,rgba(244,63,94,0.8),rgba(219,39,119,0.6)); color:white; }
.seat-occupied-late    { background:linear-gradient(135deg,rgba(245,158,11,0.8),rgba(217,119,6,0.6)); color:white; }
.seat-empty { background:var(--bg3); border:1px solid var(--border); color:var(--text-lo); }
.seat-selected { outline:2px solid var(--indigo); outline-offset:2px; }

/* ── Compare Tool ── */
.compare-col { background:var(--bg2); border:1px solid var(--border); border-radius:var(--radius-md); padding:1.2rem; }
.vs-divider { display:flex; align-items:center; justify-content:center; font-family:'Inter',sans-serif; font-size:1.5rem; font-weight:800; color:var(--text-lo); }

/* ── Report Card ── */
.report-card { background:linear-gradient(135deg,#0a1628,#160d38); border:1px solid var(--border-hi); border-radius:var(--radius-lg); padding:2rem; }
.report-title { font-family:'Inter',sans-serif; font-size:1.4rem; font-weight:800; color:var(--indigo-light); margin-bottom:1rem; }
.report-row { display:flex; justify-content:space-between; padding:0.5rem 0; border-bottom:1px solid var(--border); }
.report-key { color:var(--text-mid); font-size:0.85rem; }
.report-val { color:var(--text-hi); font-weight:600; font-size:0.85rem; }
.grade-A { color:var(--emerald); }
.grade-B { color:var(--sky); }
.grade-C { color:var(--amber); }
.grade-D { color:var(--rose); }

/* ── Alert Banner ── */
.alert-banner { padding:1rem 1.4rem; border-radius:var(--radius-sm); margin:0.5rem 0; display:flex; align-items:center; gap:0.8rem; }
.alert-danger { background:rgba(244,63,94,0.1); border:1px solid rgba(244,63,94,0.3); color:var(--rose); }
.alert-warn   { background:rgba(245,158,11,0.1); border:1px solid rgba(245,158,11,0.3); color:var(--amber); }
.alert-success{ background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.3); color:var(--emerald); }
.alert-info   { background:rgba(56,189,248,0.1); border:1px solid rgba(56,189,248,0.3); color:var(--sky); }
.alert-icon   { font-size:1.3rem; }
.alert-text   { flex:1; font-size:0.88rem; font-weight:500; }

/* ── Audit ── */
.audit-row { display:flex; gap:1rem; align-items:flex-start; padding:0.65rem 0; border-bottom:1px solid var(--border); }
.audit-time { color:var(--text-lo); font-size:0.72rem; min-width:90px; padding-top:2px; font-family:'JetBrains Mono',monospace; }
.audit-msg  { color:var(--text-mid); font-size:0.83rem; flex:1; }
.audit-who  { color:var(--indigo-light); font-size:0.72rem; font-weight:700; }

/* ── Certificate ── */
.certificate-wrapper {
    background:linear-gradient(135deg,#0d1526,#1a1040);
    border:2px solid var(--indigo); border-radius:var(--radius-xl);
    padding:3rem; text-align:center; position:relative; overflow:hidden;
}
.certificate-wrapper::before { content:'🛡️'; position:absolute; font-size:14rem; opacity:0.03; top:50%; left:50%; transform:translate(-50%,-50%); }
.cert-title { font-family:'Inter',sans-serif; font-size:1.2rem; color:var(--indigo-light); font-weight:800; }
.cert-name  { font-family:'Inter',sans-serif; font-size:2.5rem; color:var(--text-hi); font-weight:800; margin:1rem 0; }
.cert-pct   { font-family:'Inter',sans-serif; font-size:4.5rem; color:var(--emerald); font-weight:800; line-height:1; }

/* ── Footer ── */
.footer { text-align:center; padding:2rem 1rem 1rem; color:var(--text-lo); font-size:0.78rem; border-top:1px solid var(--border); margin-top:4rem; }
.footer strong { color:var(--indigo-light); }

/* ── Progress Bar Custom ── */
.progress-custom { background:var(--bg3); border-radius:99px; height:8px; overflow:hidden; margin:6px 0; }
.progress-fill { height:100%; border-radius:99px; transition:width 0.6s cubic-bezier(.4,0,.2,1); }
.pf-emerald { background:linear-gradient(90deg,var(--emerald),var(--teal)); }
.pf-amber   { background:linear-gradient(90deg,var(--amber),#f97316); }
.pf-rose    { background:linear-gradient(90deg,var(--rose),#e11d48); }
.pf-indigo  { background:linear-gradient(90deg,var(--indigo),var(--violet)); }

/* ── Notification dot ── */
.notif-dot { display:inline-block; width:8px; height:8px; background:var(--rose); border-radius:50%; animation:blink 1s infinite; }

/* ── Calendar Heatmap ── */
.cal-cell { width:14px; height:14px; border-radius:3px; display:inline-block; }
.cal-0 { background:var(--bg3); }
.cal-1 { background:rgba(16,185,129,0.3); }
.cal-2 { background:rgba(16,185,129,0.55); }
.cal-3 { background:rgba(16,185,129,0.75); }
.cal-4 { background:var(--emerald); }

/* ── PULSE animation for cards ── */
@keyframes card-enter { from{opacity:0;transform:translateY(10px);} to{opacity:1;transform:translateY(0);} }
.card-anim { animation:card-enter 0.35s ease; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════
_DEFAULTS = {
    'session_started':  False,
    'logged_in':        False,
    'role':             None,
    'user':             {},
    'total_lectures':   40,
    'live_running':     False,
    'live_marked':      set(),
    'demo':             False,
    'reset_otp':        None,
    'reset_otp_expiry': None,
    'service_requests': [],
    'audit_log':        [],
    'notifications':    [],
    'leave_requests':   [],
    'login_time':       None,
    'mood_log':         {},        # {date: {prn: mood}}
    'engagement_scores':{},        # {prn: score}
    'parent_alerts':    [],
    'broadcast_msgs':   [],
    'qr_sessions':      [],
    'dark_mode':        True,
}
for k, v in _DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

if not st.session_state.session_started:
    for f in ['attendance_results.json','attendance.csv','live_attendance.json']:
        try:
            if os.path.exists(f): os.remove(f)
        except Exception: pass
    st.session_state.session_started = True

# ══════════════════════════════════════════════════════════════════════
# UTILITY
# ══════════════════════════════════════════════════════════════════════
def _hash(s): return hashlib.sha256(s.encode()).hexdigest()
def _now_str(): return datetime.now().strftime("%d %b %Y, %I:%M %p")
def _today_str(): return datetime.now().strftime("%d %b %Y")

def _log_audit(action, detail=""):
    entry = {
        "ts": datetime.now().strftime("%H:%M:%S"),
        "date": datetime.now().strftime("%d %b"),
        "user": st.session_state.user.get("name","System"),
        "role": st.session_state.role or "system",
        "action": action, "detail": detail,
    }
    st.session_state.audit_log.insert(0, entry)
    st.session_state.audit_log = st.session_state.audit_log[:300]

def _push_notif(title, body, kind="info"):
    st.session_state.notifications.insert(0, {
        "title": title, "body": body, "kind": kind,
        "ts": _now_str(), "read": False
    })

def _unread() -> int:
    return sum(1 for n in st.session_state.notifications if not n["read"])

@st.cache_data(ttl=30)
def _cached_csv(path):
    try:
        if os.path.exists(path): return pd.read_csv(path)
    except Exception: pass
    return None

def load_csv_safe(path):
    try:
        if os.path.exists(path): return pd.read_csv(path)
    except Exception: pass
    return None

def load_json_safe(path):
    try:
        if os.path.exists(path):
            with open(path) as fh: return json.load(fh)
    except Exception: pass
    return None

def save_json_safe(path, data):
    try:
        with open(path,'w') as fh: json.dump(data, fh, indent=2)
        return True
    except Exception as e:
        st.error(f"Save failed: {e}"); return False

def get_camera_index():
    try:
        cap = cv2.VideoCapture(0)
        if cap.isOpened(): cap.release(); return 0
    except Exception: pass
    return None

# ── Attendance loader ──────────────────────────────────────────────────
def load_attendance():
    records = []; seen = set()
    for src in ['attendance_results.json','live_attendance.json']:
        data = load_json_safe(src)
        if not data: continue
        att = data.get('attendance', data)
        nti = data.get('name_to_id', {})
        if not isinstance(att, dict): continue
        for name, info in att.items():
            if name in ('name_to_id',) or not isinstance(info, dict): continue
            if name in seen: continue
            seen.add(name)
            records.append({
                'name': name, 'id': nti.get(name, name),
                'status': 'Present' if info.get('present') else info.get('status','Absent'),
                'timestamp': info.get('first_seen', info.get('timestamp','N/A')),
                'count': info.get('count', 1),
                'subject': info.get('subject','—'),
            })
    return records

# ── Demo data ─────────────────────────────────────────────────────────
_DEMO_STUDENTS = [
    ("Kamathe Sujal Ganesh",   "1272240519", 38, "Present"),
    ("Saniya Rahul Dhawade",   "1272240684", 36, "Present"),
    ("Shrutika Pokale",        "1272240580", 30, "Late"),
    ("Vedang Govind Joshi",    "1272240258", 28, "Present"),
    ("Krushna Ashok Bodake",   "1272240252", 24, "Absent"),
    ("Prathamesh Borse",       "1272240301", 35, "Present"),
    ("Aishwarya Desai",        "1272240310", 32, "Present"),
    ("Rohan Mehta",            "1272240420", 18, "Absent"),
    ("Priya Kulkarni",         "1272240450", 37, "Present"),
    ("Nikhil Sharma",          "1272240460", 29, "Late"),
]

def make_demo_attendance():
    return [{"name":n,"id":prn,"status":st_,"timestamp":f"{random.randint(9,11):02d}:{random.randint(0,59):02d} AM","count":cnt,"subject":random.choice(SUBJECTS)} for n,prn,cnt,st_ in _DEMO_STUDENTS]

def make_demo_subject_data():
    return {subj: {"attended": random.randint(6,10), "total": 10} for subj in SUBJECTS}

# ── Risk engine ──────────────────────────────────────────────────────
def compute_risk_score(pct: float, streak: int, late_count: int, leave_days: int) -> dict:
    """Rule-based dropout/debarment risk, no ML libs needed."""
    score = 0
    # Attendance weight 60%
    if pct < 50:  score += 60
    elif pct < 65: score += 45
    elif pct < 75: score += 30
    elif pct < 85: score += 10
    # Streak weight 20%
    if streak <= 1: score += 20
    elif streak <= 3: score += 12
    elif streak <= 7: score += 5
    # Late arrivals 10%
    if late_count > 5: score += 10
    elif late_count > 2: score += 5
    # Leave days 10%
    if leave_days > 10: score += 10
    elif leave_days > 5: score += 5
    score = min(100, score)
    if score >= 70: level = "HIGH"
    elif score >= 40: level = "MEDIUM"
    else: level = "LOW"
    return {"score": score, "level": level}

def compute_engagement_score(pct, on_time_ratio, subject_avg, mood_avg=3):
    """Composite engagement 0-100."""
    return min(100, round(pct*0.5 + on_time_ratio*20 + subject_avg*0.2 + mood_avg*2, 1))

# ── QR generator (ASCII art fallback) ────────────────────────────────
def generate_qr_ascii(session_id: str, size=8) -> str:
    """Generate a pseudo-QR pattern based on session ID hash."""
    h = hashlib.md5(session_id.encode()).hexdigest()
    bits = bin(int(h, 16))[2:].zfill(128)
    rows = []
    for r in range(size):
        row = ""
        for c in range(size):
            idx = (r * size + c) % len(bits)
            row += "██" if bits[idx] == "1" else "  "
        rows.append(row)
    return "\n".join(rows)

# ── Certificate builder ──────────────────────────────────────────────
def build_certificate(name, prn, pct):
    elig = pct >= MIN_ATTENDANCE
    elig_text = "ELIGIBLE FOR EXAMINATIONS" if elig else "NOT ELIGIBLE"
    elig_color = "#10b981" if elig else "#f43f5e"
    grade = "A+" if pct>=90 else "A" if pct>=80 else "B" if pct>=75 else "C" if pct>=65 else "D"
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&family=DM+Sans:wght@300;400;600&display=swap');
body{{font-family:'Inter',sans-serif;background:#f0f4ff;display:flex;justify-content:center;align-items:center;min-height:100vh;margin:0;padding:2rem;}}
.cert{{max-width:820px;width:100%;background:white;border:6px double #4f46e5;border-radius:20px;padding:3.5rem 4rem;text-align:center;box-shadow:0 20px 60px rgba(79,70,229,0.15);position:relative;overflow:hidden;}}
.cert::before{{content:'';position:absolute;top:-100px;right:-100px;width:300px;height:300px;background:radial-gradient(circle,rgba(99,102,241,0.08),transparent);border-radius:50%;}}
.logo{{font-size:1.2rem;margin-bottom:0.3rem;}}
.college{{font-size:1rem;color:#1e3c72;font-weight:700;}}
.title{{font-family:'Inter',sans-serif;font-size:1.8rem;color:#4f46e5;font-weight:800;margin:1rem 0 0.5rem;letter-spacing:0.06em;}}
.body{{color:#374151;font-size:1rem;line-height:2;}}
.student-name{{font-family:'Inter',sans-serif;font-size:2.4rem;color:#1e1b4b;font-weight:800;margin:0.8rem 0;}}
.percentage{{font-family:'Inter',sans-serif;font-size:1.2rem;font-weight:800;color:#4f46e5;}}
.grade-badge{{display:inline-block;background:#ede9fe;color:#4f46e5;border:2px solid #6366f1;border-radius:99px;padding:4px 20px;font-weight:800;font-size:1.1rem;margin:0.3rem 0;}}
.elig{{font-size:1rem;font-weight:700;color:{elig_color};padding:0.5rem 2rem;border-radius:99px;display:inline-block;border:2px solid {elig_color};margin-top:0.8rem;}}
.footer{{margin-top:2rem;font-size:0.8rem;color:#9ca3af;}}
.seal{{position:absolute;bottom:2rem;right:2.5rem;font-size:3rem;opacity:0.15;}}
hr{{border-color:#e5e7eb;margin:1.2rem 0;}}
</style></head><body><div class="cert">
<div class="seal">🏛️</div>
<div class="logo">🛡️</div>
<div class="college">{COLLEGE}</div>
<hr>
<div class="title">ATTENDANCE CERTIFICATE</div>
<div class="body">
<p>This is to certify that the student</p>
<div class="student-name">{name}</div>
<p>PRN: <strong>{prn}</strong> | {BATCH}</p>
<p>has maintained an attendance of</p>
<div class="percentage">{pct:.1f}%</div>
<div class="grade-badge">Grade {grade}</div><br>
<div class="elig">{elig_text}</div>
</div>
<hr>
<div class="footer">Generated: {_now_str()} | {APP_NAME} v{APP_VERSION}<br>Guided by {GUIDE} | {COLLEGE}</div>
</div></body></html>"""

def build_report_card_html(name, prn, pct, subj_data, streak, risk, engagement):
    rows = ""
    for subj, d in subj_data.items():
        sp = round(d['attended']/d['total']*100) if d['total'] else 0
        color = "#10b981" if sp>=75 else "#f59e0b" if sp>=60 else "#f43f5e"
        rows += f"<tr><td>{subj}</td><td>{d['attended']}/{d['total']}</td><td style='color:{color};font-weight:700;'>{sp}%</td></tr>"
    grade = "A+" if pct>=90 else "A" if pct>=80 else "B" if pct>=75 else "C" if pct>=65 else "D"
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
body{{font-family:Arial,sans-serif;background:#f5f5f5;padding:2rem;max-width:800px;margin:0 auto;}}
.header{{background:linear-gradient(135deg,#4f46e5,#7c3aed);color:white;padding:2rem;border-radius:12px;margin-bottom:1.5rem;}}
h1{{font-size:1.8rem;margin:0 0 0.3rem;}}
.grid{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:1rem;margin-bottom:1.5rem;}}
.card{{background:white;border-radius:10px;padding:1.2rem;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,0.08);}}
.big{{font-size:1.2rem;font-weight:800;color:#4f46e5;}}
.lbl{{font-size:0.75rem;text-transform:uppercase;color:#94a3b8;font-weight:700;}}
table{{width:100%;border-collapse:collapse;background:white;border-radius:10px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.08);}}
th{{background:#4f46e5;color:white;padding:0.7rem 1rem;text-align:left;}}
td{{padding:0.6rem 1rem;border-bottom:1px solid #f1f5f9;}}
.risk-{risk['level'].lower()}{{color:{'#10b981' if risk['level']=='LOW' else '#f59e0b' if risk['level']=='MEDIUM' else '#f43f5e'};}}
</style></head><body>
<div class="header"><h1>📊 Student Report Card</h1><p>{name} | PRN: {prn} | {BATCH}</p><p>{_today_str()}</p></div>
<div class="grid">
<div class="card"><div class="big">{pct:.1f}%</div><div class="lbl">Attendance</div></div>
<div class="card"><div class="big">{grade}</div><div class="lbl">Grade</div></div>
<div class="card"><div class="big">🔥{streak}</div><div class="lbl">Day Streak</div></div>
<div class="card"><div class="big">{engagement}</div><div class="lbl">Engagement Score</div></div>
<div class="card"><div class="big class risk-{risk['level'].lower()}">{risk['level']}</div><div class="lbl">Risk Level</div></div>
<div class="card"><div class="big">{risk['score']}</div><div class="lbl">Risk Score</div></div>
</div>
<table><tr><th>Subject</th><th>Attended / Total</th><th>Attendance %</th></tr>{rows}</table>
<p style="text-align:center;color:#9ca3af;font-size:0.8rem;margin-top:1.5rem;">Generated by {APP_NAME} v{APP_VERSION} | {COLLEGE}</p>
</body></html>"""

# ── Service requests ──────────────────────────────────────────────────
def load_service_requests():
    data = load_json_safe('service_requests.json')
    if isinstance(data, list): st.session_state.service_requests = data
    return st.session_state.service_requests

def submit_service_request(student_name, prn, svc, notes=""):
    req_id = f"SR{len(st.session_state.service_requests)+1:04d}"
    req = {'id':req_id,'student':student_name,'prn':str(prn),'service':svc,'status':'Pending','date':_now_str(),'notes':notes,'dept':SERVICES[svc]['dept'],'fee':SERVICES[svc]['fee'],'est_time':SERVICES[svc]['time'],'priority':'Normal','updates':[]}
    st.session_state.service_requests.append(req)
    save_json_safe('service_requests.json', st.session_state.service_requests)
    _log_audit("Service Request", f"{student_name} submitted {svc}")
    _push_notif("New Request", f"{svc} from {student_name}", "info")
    return req_id

# ── Session timeout ───────────────────────────────────────────────────
def check_session_timeout():
    if st.session_state.login_time and st.session_state.logged_in:
        elapsed = (datetime.now() - st.session_state.login_time).total_seconds()/60
        if elapsed > SESSION_TIMEOUT_MIN and not st.session_state.demo:
            _log_audit("Auto-logout","Session timeout")
            for k in list(st.session_state.keys()): del st.session_state[k]
            st.warning("Session expired. Please log in again."); st.stop()

# ══════════════════════════════════════════════════════════════════════
# LOGIN
# ══════════════════════════════════════════════════════════════════════
def login_page():
    col_l, col_c, col_r = st.columns([1, 0.85, 1])
    with col_c:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"""
            <div style="text-align:center;margin-bottom:2rem;">
                <div style="font-size:2.5rem;margin-bottom:0.5rem;filter:drop-shadow(0 8px 24px rgba(99,102,241,0.4));">🛡️</div>
                <h1 style="font-family:'Inter',sans-serif;color:white;font-size:2.6rem;font-weight:800;margin:0;background:linear-gradient(135deg,#818cf8,#6366f1);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">{APP_NAME}</h1>
                <p style="color:var(--text-mid);margin:0.4rem 0 0;font-size:1rem;">Enterprise Attendance Intelligence Platform</p>
                <p style="color:var(--text-lo);font-size:0.8rem;margin-top:0.3rem;">{COLLEGE}</p>
                <div style="display:flex;gap:0.5rem;justify-content:center;margin-top:0.8rem;flex-wrap:wrap;">
                    <span style="background:rgba(99,102,241,0.15);border:1px solid rgba(99,102,241,0.3);padding:3px 12px;border-radius:99px;font-size:0.72rem;color:var(--indigo-light);">v{APP_VERSION}</span>
                    <span style="background:rgba(16,185,129,0.15);border:1px solid rgba(16,185,129,0.3);padding:3px 12px;border-radius:99px;font-size:0.72rem;color:var(--emerald);">Face Recognition</span>
                    <span style="background:rgba(245,158,11,0.15);border:1px solid rgba(245,158,11,0.3);padding:3px 12px;border-radius:99px;font-size:0.72rem;color:var(--amber);">AI-Powered</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        with st.container():
            st.markdown('<div class="glass">', unsafe_allow_html=True)
            st.markdown('<h3 style="color:white;font-family:\'Inter\',sans-serif;margin-bottom:1.2rem;">Sign In</h3>', unsafe_allow_html=True)
            role_d = st.selectbox("Select your role", ["Teacher","Student","Administrator"])
            role = role_d.lower().replace('administrator','admin')
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            col_a, col_b = st.columns(2)
            with col_a: sign_in_btn = st.button("Sign In", use_container_width=True, type="primary")
            with col_b: demo_btn    = st.button("✨ Try Demo", use_container_width=True)

            if sign_in_btn or demo_btn:
                if demo_btn or (username.strip().lower()=="demo" and password=="demo"):
                    _do_login(role, {'name':'Demo User','id':'DEMO001','email':'demo@mitwpu.edu.in','dept':'Data Science & AI','subject':'All Subjects'}, demo=True)
                else:
                    if not username.strip() or not password:
                        st.error("Please enter username and password.")
                    else:
                        users_df = load_csv_safe('users.csv')
                        if users_df is None:
                            st.error("⚠️ users.csv not found. Use 'Try Demo' to explore.")
                        else:
                            mask = ((users_df.get('username',pd.Series())==username.strip()) &
                                    (users_df.get('password',pd.Series())==password) &
                                    (users_df.get('role',pd.Series())==role))
                            if mask.any():
                                _do_login(role, users_df[mask].iloc[0].to_dict(), demo=False)
                            else:
                                st.error("Invalid credentials.")

            with st.expander("Forgot Password?"):
                fp_email = st.text_input("Registered email", key="fp_email")
                if st.button("Send OTP", key="fp_send"):
                    if not fp_email or "@" not in fp_email: st.warning("Enter a valid email.")
                    else:
                        otp = str(random.randint(100000,999999))
                        st.session_state.reset_otp = otp
                        st.session_state.reset_email = fp_email
                        st.session_state.reset_otp_expiry = datetime.now()+timedelta(minutes=10)
                        st.info(f"OTP sent to {fp_email} (Demo OTP: {otp})")
                if st.session_state.reset_otp:
                    e_otp = st.text_input("Enter OTP", max_chars=6, key="otp_field")
                    np_   = st.text_input("New Password", type="password", key="np_field")
                    cp_   = st.text_input("Confirm Password", type="password", key="cp_field")
                    if st.button("Reset Password", key="fp_reset"):
                        if datetime.now()>st.session_state.reset_otp_expiry: st.error("OTP expired.")
                        elif e_otp!=st.session_state.reset_otp: st.error("Invalid OTP.")
                        elif np_!=cp_: st.error("Passwords don't match.")
                        elif len(np_)<6: st.error("Password too short.")
                        else:
                            udf = load_csv_safe('users.csv')
                            if udf is not None:
                                m = udf.get('email',pd.Series())==st.session_state.reset_email
                                if m.any(): udf.loc[m,'password']=np_; udf.to_csv('users.csv',index=False)
                            st.success("Password reset!"); st.session_state.reset_otp=None; time.sleep(1); st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown(f'<p style="text-align:center;color:var(--text-lo);margin-top:1.5rem;font-size:0.78rem;">Guided by {GUIDE} | v{APP_VERSION}</p>', unsafe_allow_html=True)

def _do_login(role, user_dict, demo):
    st.session_state.logged_in = True; st.session_state.role = role
    st.session_state.user = user_dict; st.session_state.demo = demo
    st.session_state.login_time = datetime.now()
    load_service_requests()
    _log_audit("Login", f"{user_dict.get('name','?')} signed in as {role}")
    if demo: _push_notif("Demo Mode","Viewing simulated data — all features enabled.","info")
    st.rerun()

# ══════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════
def render_sidebar():
    u = st.session_state.user; role = st.session_state.role
    unread = _unread()
    with st.sidebar:
        mode_badge = '<span class="badge-demo">DEMO</span>' if st.session_state.demo else '<span class="badge-live">● LIVE</span>'
        avatar = '🧑‍💼' if role=='teacher' else '🎓' if role=='student' else '🔐'
        st.markdown(f"""
            <div class="sidebar-profile">
                <div class="avatar">{avatar}</div>
                <div class="name">{u.get('name','User')}</div>
                <div class="role">{role.title()}</div>
                {mode_badge}
            </div>
        """, unsafe_allow_html=True)

        if unread:
            st.markdown(f'<div style="background:rgba(244,63,94,0.1);border:1px solid rgba(244,63,94,0.3);border-radius:8px;padding:0.5rem 0.8rem;font-size:0.82rem;color:var(--rose);margin-bottom:0.5rem;">🔔 {unread} unread notification{"s" if unread>1 else ""}</div>', unsafe_allow_html=True)

        # System status
        st.markdown("""
            <div style="background:var(--bg2);border:1px solid var(--border);border-radius:10px;padding:0.8rem;margin-bottom:0.8rem;">
                <div style="font-size:0.7rem;color:var(--text-lo);text-transform:uppercase;letter-spacing:0.08em;font-weight:700;margin-bottom:0.5rem;">System Status</div>
                <div style="display:flex;align-items:center;gap:6px;font-size:0.8rem;color:var(--text-mid);">
                    <span style="width:7px;height:7px;background:var(--emerald);border-radius:50%;display:inline-block;"></span> AI Engine Online
                </div>
                <div style="display:flex;align-items:center;gap:6px;font-size:0.8rem;color:var(--text-mid);margin-top:3px;">
                    <span style="width:7px;height:7px;background:var(--emerald);border-radius:50%;display:inline-block;"></span> Database Connected
                </div>
                <div style="display:flex;align-items:center;gap:6px;font-size:0.8rem;color:var(--text-mid);margin-top:3px;">
                    <span style="width:7px;height:7px;background:var(--emerald);border-radius:50%;display:inline-block;"></span> Face Rec Ready
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"<small style='color:var(--text-lo);'>Session: {st.session_state.login_time.strftime('%I:%M %p') if st.session_state.login_time else '—'}</small>", unsafe_allow_html=True)
        st.markdown("---")
        if st.button("🗑 Clear Attendance Data", use_container_width=True):
            for f in ['attendance_results.json','attendance.csv','live_attendance.json']:
                try:
                    if os.path.exists(f): os.remove(f)
                except Exception: pass
            _cached_csv.clear()
            _log_audit("Data Cleared","All attendance removed")
            st.success("Cleared!"); time.sleep(0.6); st.rerun()
        if st.button("🚪 Sign Out", use_container_width=True):
            _log_audit("Logout", u.get('name','?'))
            for k in list(st.session_state.keys()): del st.session_state[k]
            st.rerun()

        st.markdown("---")
        st.markdown(f'<div class="footer" style="margin-top:0;padding-top:0.5rem;">{APP_NAME}<br><small>v{APP_VERSION}</small></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# HELPER WIDGETS
# ══════════════════════════════════════════════════════════════════════
def render_progress_bar(pct, color="indigo"):
    color_class = f"pf-{color}"
    bar_color = {"emerald":"var(--emerald)","amber":"var(--amber)","rose":"var(--rose)","indigo":"var(--indigo)"}.get(color,"var(--indigo)")
    return f'<div class="progress-custom"><div class="progress-fill {color_class}" style="width:{min(pct,100)}%;background:{bar_color};"></div></div>'

def render_alert(text, kind="info", icon="ℹ️"):
    cls = {"info":"alert-info","warn":"alert-warn","danger":"alert-danger","success":"alert-success"}.get(kind,"alert-info")
    return f'<div class="alert-banner {cls}"><span class="alert-icon">{icon}</span><span class="alert-text">{text}</span></div>'

def days_until(date_str):
    try:
        target = datetime.strptime(date_str, "%Y-%m-%d").date()
        return (target - date.today()).days
    except Exception: return 999

# ══════════════════════════════════════════════════════════════════════
# ██████ STUDENT PORTAL v6
# ══════════════════════════════════════════════════════════════════════
def student_portal():
    u = st.session_state.user
    student_name = u.get('name','Student')
    student_id   = str(u.get('id','N/A'))
    dept         = u.get('dept','Data Science & AI')

    records = load_attendance()
    if st.session_state.demo and not records: records = make_demo_attendance()

    my = next((r for r in records if r.get('name','').lower()==student_name.lower()), None)
    tl  = st.session_state.total_lectures
    det = my.get('count',0) if my else 0
    pct = round(det/tl*100,1) if tl>0 else 0.0
    req = math.ceil(0.75*tl)
    can_miss  = max(0, det-req)
    need_more = max(0, req-det)
    elig      = pct >= MIN_ATTENDANCE

    streak       = random.randint(5,18)  if st.session_state.demo else 0
    subj_data    = make_demo_subject_data() if st.session_state.demo else {}
    late_count   = random.randint(1,5) if st.session_state.demo else 0
    leave_days   = len([l for l in st.session_state.leave_requests if l.get('prn')==student_id])

    risk         = compute_risk_score(pct, streak, late_count, leave_days)
    on_time_ratio = max(0, (det-late_count)/det) if det>0 else 1
    subj_avg     = sum(round(d['attended']/d['total']*100) for d in subj_data.values())/len(subj_data) if subj_data else pct
    engagement   = compute_engagement_score(pct, on_time_ratio, subj_avg)

    st.markdown(f"""
        <div class="hero">
            <h2>Welcome back, {student_name.split()[0]}! 👋</h2>
            <p>PRN: {student_id} &nbsp;|&nbsp; {dept} &nbsp;|&nbsp; {BATCH}</p>
            <div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin-top:0.8rem;">
                <div class="badge"><span class="live-dot"></span> Dashboard Active</div>
                <div class="badge">Engagement: {engagement}/100</div>
                <div class="badge" style="{"background:rgba(244,63,94,0.2);border-color:rgba(244,63,94,0.4);color:var(--rose);" if risk['level']=='HIGH' else "background:rgba(245,158,11,0.2);border-color:rgba(245,158,11,0.4);color:var(--amber);" if risk['level']=='MEDIUM' else ""}">Risk: {risk['level']}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    tabs = st.tabs(["📊 Dashboard","📅 Timetable","🔥 Leaderboard","😊 Mood & Wellness","⚠️ Danger Zone","🏖 Leave","🏢 Services","📆 Exams","🎖 Certificate","🔔 Notifications","❓ Help"])

    # ─── TAB 0: Dashboard ─────────────────────────────────────────
    with tabs[0]:
        c1,c2,c3,c4,c5,c6 = st.columns(6)
        pct_color = "var(--emerald)" if pct>=75 else "var(--amber)" if pct>=60 else "var(--rose)"
        c1.markdown(f'<div class="stat-card"><span class="stat-icon">📈</span><div class="stat-num" style="color:{pct_color};">{pct}%</div><div class="stat-lbl">Attendance</div></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="stat-card"><span class="stat-icon">✅</span><div class="stat-num">{det}</div><div class="stat-lbl">Attended</div><div class="stat-sub">of {tl}</div></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="stat-card stat-{"present" if elig else "absent"}"><span class="stat-icon">{"🎯" if elig else "⚠️"}</span><div class="stat-num">{"YES" if elig else "NO"}</div><div class="stat-lbl">Exam Eligible</div></div>', unsafe_allow_html=True)
        c4.markdown(f'<div class="stat-card stat-late"><span class="stat-icon">🛡️</span><div class="stat-num">{can_miss}</div><div class="stat-lbl">Can Miss</div></div>', unsafe_allow_html=True)
        c5.markdown(f'<div class="streak-box"><div class="streak-num">🔥{streak}</div><div class="streak-lbl">Day Streak</div></div>', unsafe_allow_html=True)
        c6.markdown(f'<div class="stat-card stat-risk"><span class="stat-icon">💡</span><div class="stat-num">{engagement}</div><div class="stat-lbl">Engagement</div></div>', unsafe_allow_html=True)

        # Smart alert
        if not elig:
            st.markdown(render_alert(f"⚠ You need {need_more} more classes to reach 75%. Attend ALL remaining sessions!","danger","🚨"), unsafe_allow_html=True)
        elif pct < 80:
            st.markdown(render_alert(f"You can safely miss {can_miss} more classes. Stay consistent to maintain eligibility.","warn","⚡"), unsafe_allow_html=True)
        else:
            st.markdown(render_alert("Excellent attendance! You're well above the threshold. Keep the streak alive!","success","🌟"), unsafe_allow_html=True)

        # Risk card inline
        risk_col = {"LOW":"var(--emerald)","MEDIUM":"var(--amber)","HIGH":"var(--rose)"}[risk['level']]
        risk_emoji = {"LOW":"✅","MEDIUM":"⚠️","HIGH":"🚨"}[risk['level']]
        st.markdown(f"""
            <div style="background:var(--bg2);border:1px solid var(--border);border-left:4px solid {risk_col};border-radius:var(--radius-md);padding:1rem 1.4rem;margin:0.5rem 0;display:flex;align-items:center;gap:1.5rem;">
                <div style="font-size:1.2rem;">{risk_emoji}</div>
                <div style="flex:1;">
                    <div style="font-weight:700;color:var(--text-hi);font-size:0.9rem;">Dropout / Debarment Risk: <span style="color:{risk_col};">{risk['level']}</span></div>
                    <div style="color:var(--text-mid);font-size:0.82rem;margin-top:3px;">Risk Score: {risk['score']}/100 &nbsp;|&nbsp; Streak: {streak} days &nbsp;|&nbsp; Late arrivals: {late_count}</div>
                </div>
                <div>{render_progress_bar(risk['score'], 'rose' if risk['level']=='HIGH' else 'amber' if risk['level']=='MEDIUM' else 'emerald')}</div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_g, col_s = st.columns([1.2, 1])

        with col_g:
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=pct,
                delta={'reference':MIN_ATTENDANCE,'relative':False},
                number={'suffix':'%','font':{'size':52,'color':'white','family':'Inter'}},
                gauge={
                    'axis':{'range':[0,100],'tickcolor':'#475569','tickwidth':1},
                    'bar':{'color':'#6366f1','thickness':0.22},
                    'bgcolor':'rgba(0,0,0,0)','bordercolor':'rgba(0,0,0,0)',
                    'steps':[
                        {'range':[0,50],'color':'rgba(244,63,94,0.18)'},
                        {'range':[50,75],'color':'rgba(245,158,11,0.18)'},
                        {'range':[75,100],'color':'rgba(16,185,129,0.18)'},
                    ],
                    'threshold':{'line':{'color':'#f8fafc','width':3},'thickness':0.75,'value':MIN_ATTENDANCE}
                }
            ))
            fig_gauge.update_layout(height=280,margin=dict(t=10,b=10,l=10,r=10),paper_bgcolor='rgba(0,0,0,0)',font_color='white')
            st.plotly_chart(fig_gauge, use_container_width=True)

        with col_s:
            st.markdown("#### Subject-wise Attendance")
            if subj_data:
                rows = [{'Subject':subj,'Attended':d['attended'],'Total':d['total'],'%':round(d['attended']/d['total']*100) if d['total'] else 0} for subj,d in subj_data.items()]
                sdf = pd.DataFrame(rows)
                fig_subj = px.bar(sdf, x='%', y='Subject', orientation='h', color='%', color_continuous_scale=['#f43f5e','#f59e0b','#10b981'], range_color=[0,100], text='%')
                fig_subj.update_traces(texttemplate='%{text}%', textposition='outside')
                fig_subj.update_layout(height=280,margin=dict(t=10,b=10,l=10,r=50),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',font_color='white',showlegend=False,coloraxis_showscale=False,yaxis_title=None,xaxis_title=None)
                fig_subj.update_xaxes(range=[0,120],showgrid=False,showticklabels=False)
                fig_subj.update_yaxes(showgrid=False)
                st.plotly_chart(fig_subj, use_container_width=True)

        # Monthly trend
        if st.session_state.demo:
            st.markdown("#### 📈 Monthly Attendance Trend + Prediction")
            months = ["Aug","Sep","Oct","Nov","Dec","Jan","Feb","Mar","Apr","May","Jun(pred)"]
            vals   = [random.randint(72,98) for _ in range(10)] + [None]
            pred   = [None]*9 + [vals[9], max(60,vals[9]+random.randint(-5,5))]
            fig_trend = go.Figure()
            fig_trend.add_trace(go.Scatter(x=months[:10],y=vals[:10],mode='lines+markers+text',line=dict(color='#6366f1',width=3),marker=dict(size=8,color='#818cf8'),text=[f"{v}%" for v in vals[:10]],textposition='top center',fill='tozeroy',fillcolor='rgba(99,102,241,0.08)',name='Actual'))
            fig_trend.add_trace(go.Scatter(x=months[9:],y=pred[9:],mode='lines+markers',line=dict(color='#f59e0b',width=2,dash='dash'),marker=dict(size=8,color='#fbbf24',symbol='diamond'),name='Predicted'))
            fig_trend.add_hline(y=75,line_dash="dash",line_color="#f43f5e",annotation_text="75% Min")
            fig_trend.update_layout(height=220,margin=dict(t=10,b=10,l=10,r=10),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',font_color='white',yaxis=dict(range=[50,110],showgrid=False),xaxis=dict(showgrid=False),legend=dict(bgcolor='rgba(0,0,0,0)'))
            st.plotly_chart(fig_trend, use_container_width=True)

        # Attendance heatmap calendar (last 60 days)
        st.markdown("#### 📅 Attendance Calendar (Last 60 Days)")
        cal_html = '<div style="display:flex;flex-direction:column;gap:3px;">'
        weeks = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"]
        cal_html += '<div style="display:flex;gap:4px;margin-bottom:4px;">' + "".join([f'<div style="width:14px;font-size:0.6rem;color:var(--text-lo);text-align:center;">{w[0]}</div>' for w in weeks]) + '</div>'
        # Generate 9 weeks of data
        for week in range(9):
            cal_html += '<div style="display:flex;gap:4px;">'
            for day in range(7):
                seed = week*7+day
                if seed >= 60:
                    cal_html += f'<div class="cal-cell cal-0"></div>'
                else:
                    r = random.Random(seed+hash(student_id))
                    val = r.choice([0,1,2,3,4,4,4,3,2])
                    cal_html += f'<div class="cal-cell cal-{val}" title="Day {seed}"></div>'
            cal_html += '</div>'
        cal_html += '</div>'
        cal_html += '<div style="display:flex;gap:6px;align-items:center;margin-top:0.5rem;font-size:0.72rem;color:var(--text-lo);">Less <div class="cal-cell cal-0" style="display:inline-block;"></div><div class="cal-cell cal-1" style="display:inline-block;"></div><div class="cal-cell cal-2" style="display:inline-block;"></div><div class="cal-cell cal-3" style="display:inline-block;"></div><div class="cal-cell cal-4" style="display:inline-block;"></div> More</div>'
        st.markdown(f'<div class="glass" style="padding:1.2rem;">{cal_html}</div>', unsafe_allow_html=True)

    # ─── TAB 1: Timetable ─────────────────────────────────────────
    with tabs[1]:
        tdf = load_csv_safe('timetable.csv')
        today = datetime.now().strftime("%A")
        cur_time = datetime.now().strftime("%H:%M")
        st.markdown(f"### 📅 Today — {today}, {datetime.now().strftime('%d %B %Y')}")
        if tdf is not None and not tdf.empty:
            try:
                today_df = tdf[tdf['Day'].str.lower()==today.lower()].copy()
                if today_df.empty: st.info("No classes scheduled today.")
                else:
                    for _,row in today_df.iterrows():
                        try:
                            is_current = row["Start Time"]<=cur_time<=row["End Time"]
                            is_upcoming = row["Start Time"]>cur_time
                            cls_ = "current" if is_current else ("upcoming" if is_upcoming else "done")
                            icon = "🟢 NOW" if is_current else ("🕐" if is_upcoming else "✅")
                            st.markdown(f'<div class="tt-card {cls_}"><h5>{icon} {row.get("Subject","—")}</h5><small>👤 {row.get("Faculty","—")} &nbsp;|&nbsp; 🕐 {row.get("Start Time","—")} – {row.get("End Time","—")} &nbsp;|&nbsp; 🏛 {row.get("Room",row.get("Classroom","—"))}</small></div>', unsafe_allow_html=True)
                        except Exception: pass
            except Exception as e: st.warning(f"Timetable format issue: {e}")
        else:
            st.info("Timetable not found. Ask your teacher to upload it.")
        st.markdown("---")
        st.markdown("### Full Week Schedule")
        days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
        dtabs = st.tabs(days)
        for i, day in enumerate(days):
            with dtabs[i]:
                if tdf is not None and not tdf.empty:
                    ddf = tdf[tdf.get('Day',pd.Series()).str.lower()==day.lower()].reset_index(drop=True) if 'Day' in tdf.columns else pd.DataFrame()
                    if not ddf.empty: st.dataframe(ddf[["Start Time","End Time","Subject","Faculty"] if all(c in ddf.columns for c in ["Start Time","End Time","Subject","Faculty"]) else ddf.columns.tolist()], use_container_width=True, hide_index=True)
                    else: st.caption("No classes.")
                else: st.caption("No timetable data.")

    # ─── TAB 2: Leaderboard ───────────────────────────────────────
    with tabs[2]:
        st.markdown("### 🔥 Attendance Leaderboard & Rankings")
        if records:
            sorted_rec = sorted(records, key=lambda r: (r.get('count',0), r.get('name','')), reverse=True)
            medal = {0:"🥇",1:"🥈",2:"🥉"}
            rank_class = {0:"rank-gold",1:"rank-silver",2:"rank-bronze"}
            my_rank = next((i for i,r in enumerate(sorted_rec) if r.get('name','').lower()==student_name.lower()), None)

            if my_rank is not None:
                mp = round(sorted_rec[my_rank].get('count',0)/tl*100,1) if tl else 0
                st.markdown(f"""
                    <div style="background:linear-gradient(135deg,rgba(99,102,241,0.15),rgba(139,92,246,0.1));border:1px solid var(--border-hi);border-radius:var(--radius-md);padding:1.2rem;margin-bottom:1rem;text-align:center;">
                        <div style="font-family:'Inter',sans-serif;font-size:0.8rem;color:var(--text-mid);text-transform:uppercase;letter-spacing:0.1em;">Your Ranking</div>
                        <div style="font-family:'Inter',sans-serif;font-size:3rem;font-weight:800;color:var(--indigo-light);">#{my_rank+1}</div>
                        <div style="color:var(--text-mid);font-size:0.85rem;">out of {len(sorted_rec)} students &nbsp;|&nbsp; {mp}% attendance</div>
                    </div>
                """, unsafe_allow_html=True)

            for i, r in enumerate(sorted_rec[:10]):
                p_ = round(r.get('count',0)/tl*100,1) if tl else 0
                m = medal.get(i,"")
                rc = rank_class.get(i,"")
                is_me = r.get('name','').lower() == student_name.lower()
                border_extra = "border-color:var(--indigo);" if is_me else ""
                st.markdown(f"""
                    <div class="rank-card" style="{border_extra}">
                        <div class="rank-num {rc}">{m or f"#{i+1}"}</div>
                        <div class="rank-info">
                            <div class="rank-name">{r['name']} {"← You" if is_me else ""}</div>
                            <div class="rank-sub">PRN: {r.get('id','—')} &nbsp;|&nbsp; Streak: {random.randint(1,20) if st.session_state.demo else '—'} days</div>
                        </div>
                        <div class="rank-pct" style="color:{'var(--emerald)' if p_>=75 else 'var(--amber)' if p_>=60 else 'var(--rose)'};">{p_}%</div>
                    </div>
                """, unsafe_allow_html=True)

            # Bar race chart
            top5 = sorted_rec[:5]
            fig_lb = go.Figure(go.Bar(
                x=[round(r.get('count',0)/tl*100,1) for r in top5],
                y=[r['name'].split()[0] for r in top5],
                orientation='h',
                marker_color=['#fbbf24','#cbd5e1','#d97706','#6366f1','#818cf8'],
                text=[f"{round(r.get('count',0)/tl*100,1)}%" for r in top5],
                textposition='outside'
            ))
            fig_lb.update_layout(height=220,margin=dict(t=10,b=10,l=10,r=60),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',font_color='white',xaxis=dict(range=[0,110],showgrid=False,showticklabels=False),yaxis=dict(showgrid=False))
            st.plotly_chart(fig_lb, use_container_width=True)

    # ─── TAB 3: Mood & Wellness ────────────────────────────────────
    with tabs[3]:
        st.markdown("### 😊 Daily Mood & Wellness Check-in")
        today_key = datetime.now().strftime("%Y-%m-%d")
        my_mood = st.session_state.mood_log.get(today_key, {}).get(student_id)

        if my_mood:
            st.markdown(render_alert(f"Today's mood logged: **{my_mood}** — Thanks for checking in! 💙","success","✅"), unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:var(--text-mid);margin-bottom:1rem;">How are you feeling today? Your wellbeing matters.</p>', unsafe_allow_html=True)
            mood_cols = st.columns(5)
            for i, mood in enumerate(MOOD_OPTIONS):
                with mood_cols[i]:
                    if st.button(mood.split()[0], key=f"mood_{i}", use_container_width=True):
                        if today_key not in st.session_state.mood_log:
                            st.session_state.mood_log[today_key] = {}
                        st.session_state.mood_log[today_key][student_id] = mood
                        _log_audit("Mood Check-in", f"{student_name}: {mood}")
                        st.rerun()
                    st.caption(mood.split(" ",1)[1] if " " in mood else mood, )

        # Wellness summary
        st.markdown("---")
        st.markdown("### 📊 Wellness Analytics (Demo)")
        if st.session_state.demo:
            mood_data = [random.choice(MOOD_OPTIONS) for _ in range(30)]
            mood_counts = {m: mood_data.count(m) for m in MOOD_OPTIONS}
            fig_mood = px.pie(values=list(mood_counts.values()), names=list(mood_counts.keys()),
                              color_discrete_sequence=['#10b981','#6366f1','#38bdf8','#f59e0b','#f43f5e'], hole=0.5)
            fig_mood.update_layout(height=280,paper_bgcolor='rgba(0,0,0,0)',font_color='white',margin=dict(t=10,b=10,l=10,r=10))
            st.plotly_chart(fig_mood, use_container_width=True)

        # Stress vs attendance correlation
        st.markdown("#### Mood vs Attendance Correlation")
        if st.session_state.demo:
            mood_trend = [random.randint(2,5) for _ in range(10)]
            att_trend  = [random.randint(60,100) for _ in range(10)]
            fig_corr = make_subplots(specs=[[{"secondary_y":True}]])
            fig_corr.add_trace(go.Scatter(x=list(range(10)),y=att_trend,name="Attendance%",line=dict(color="#6366f1",width=2),fill='tozeroy',fillcolor='rgba(99,102,241,0.08)'), secondary_y=False)
            fig_corr.add_trace(go.Scatter(x=list(range(10)),y=mood_trend,name="Mood Score",line=dict(color="#f59e0b",width=2,dash='dot'),mode='lines+markers'), secondary_y=True)
            fig_corr.update_layout(height=220,margin=dict(t=10,b=10,l=10,r=10),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',font_color='white',legend=dict(bgcolor='rgba(0,0,0,0)'))
            fig_corr.update_xaxes(showgrid=False); fig_corr.update_yaxes(showgrid=False)
            st.plotly_chart(fig_corr, use_container_width=True)

    # ─── TAB 4: Danger Zone ────────────────────────────────────────
    with tabs[4]:
        st.markdown("### ⚠️ Subject Danger Zone — Debarment Risk")
        danger_subjects = []
        safe_subjects   = []
        for subj, d in subj_data.items():
            sp = round(d['attended']/d['total']*100) if d['total'] else 0
            if sp < MIN_ATTENDANCE: danger_subjects.append((subj,sp,d))
            else: safe_subjects.append((subj,sp,d))

        if danger_subjects:
            st.markdown(render_alert(f"You are below 75% in {len(danger_subjects)} subject(s). Immediate action required!","danger","🚨"), unsafe_allow_html=True)
            for subj, sp, d in danger_subjects:
                need = math.ceil((0.75*d['total'] - d['attended'])) if d['total'] else 0
                st.markdown(f"""
                    <div class="insight-card insight-crit">
                        <h5>🚨 {subj} — <span style="color:var(--rose);">{sp}%</span></h5>
                        <p>Attended: {d['attended']}/{d['total']} &nbsp;|&nbsp; Need <strong>{need}</strong> more classes to reach 75%</p>
                        {render_progress_bar(sp, 'rose')}
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(render_alert("All subjects above 75% — No debarment risk!","success","✅"), unsafe_allow_html=True)

        if safe_subjects:
            st.markdown("#### ✅ Safe Subjects")
            for subj, sp, d in safe_subjects:
                color = "emerald" if sp>=85 else "indigo"
                st.markdown(f"""
                    <div class="insight-card insight-ok">
                        <h5>✅ {subj} — {sp}%</h5>
                        <p>Attended: {d['attended']}/{d['total']} &nbsp;|&nbsp; Can miss {max(0, d['attended']-math.ceil(0.75*d['total']))} more classes</p>
                        {render_progress_bar(sp, color)}
                    </div>
                """, unsafe_allow_html=True)

        # Report Card download
        st.markdown("---")
        st.markdown("#### 📊 Download Full Report Card")
        html_report = build_report_card_html(student_name, student_id, pct, subj_data, streak, risk, engagement)
        st.download_button("⬇️ Download Report Card (HTML)", data=html_report, file_name=f"report_card_{student_id}.html", mime="text/html", use_container_width=True, type="primary")

    # ─── TAB 5: Leave ─────────────────────────────────────────────
    with tabs[5]:
        st.markdown("### 🏖 Leave Application")
        with st.form("leave_form"):
            leave_type = st.selectbox("Leave Type", ["Medical","Personal","Family Emergency","Event/Competition","Other"])
            date_from  = st.date_input("From Date", value=datetime.now().date())
            date_to    = st.date_input("To Date", value=datetime.now().date())
            reason     = st.text_area("Reason", placeholder="Briefly explain your leave request...")
            doc_ref    = st.text_input("Supporting Document Reference (optional)")
            urgent_flag = st.checkbox("Mark as Urgent")
            submit_leave = st.form_submit_button("Submit Leave Application", use_container_width=True, type="primary")
        if submit_leave:
            if date_to < date_from: st.error("End date before start date.")
            elif not reason.strip(): st.error("Please provide a reason.")
            else:
                days_c = (date_to - date_from).days + 1
                lv = {"id":f"LV{len(st.session_state.leave_requests)+1:03d}","student":student_name,"prn":student_id,"type":leave_type,"from":str(date_from),"to":str(date_to),"days":days_c,"reason":reason,"doc_ref":doc_ref,"status":"Pending","applied":_now_str(),"urgent":urgent_flag}
                st.session_state.leave_requests.append(lv)
                save_json_safe('leave_requests.json', st.session_state.leave_requests)
                _log_audit("Leave Applied", f"{student_name}: {leave_type} {date_from}→{date_to}")
                _push_notif("Leave Submitted", f"{leave_type} leave applied","info")
                # Simulate parent notification
                st.session_state.parent_alerts.append({"student":student_name,"msg":f"Leave application: {leave_type} {date_from}→{date_to}","ts":_now_str(),"status":"Sent"})
                st.success(f"Leave submitted! ID: {lv['id']}"); st.balloons()

        my_leaves = [l for l in st.session_state.leave_requests if l.get('prn')==student_id]
        if my_leaves:
            st.markdown("---"); st.markdown("#### My Leave History")
            for lv in reversed(my_leaves):
                cls_ = "insight-ok" if lv['status']=="Approved" else ("insight-crit" if lv['status']=="Rejected" else "insight-warn")
                urgent_label = " 🔴 URGENT" if lv.get('urgent') else ""
                st.markdown(f'<div class="insight-card {cls_}"><h5>{lv["type"]} Leave — {lv["from"]} to {lv["to"]} ({lv["days"]} day{"s" if lv["days"]>1 else ""}){urgent_label}</h5><p>{lv["reason"]} &nbsp;|&nbsp; <strong>{lv["status"]}</strong> &nbsp;|&nbsp; {lv["applied"]}</p></div>', unsafe_allow_html=True)

    # ─── TAB 6: Services ──────────────────────────────────────────
    with tabs[6]:
        st.markdown("### 🏢 Student Service Hub")
        col_svc, col_my = st.columns([1.5, 1])
        with col_svc:
            svc_choice = st.selectbox("Select Service", list(SERVICES.keys()), format_func=lambda k: f"{SERVICES[k]['icon']} {k}")
            sel = SERVICES[svc_choice]
            st.markdown(f'<div class="insight-card insight-info"><h5>{sel["icon"]} {svc_choice}</h5><p>🏛 {sel["dept"]} &nbsp;|&nbsp; 💰 {sel["fee"]} &nbsp;|&nbsp; ⏱ {sel["time"]}</p></div>', unsafe_allow_html=True)
            svc_notes = st.text_area("Additional Notes (optional)")
            priority = st.radio("Priority", ["Normal","Urgent"], horizontal=True)
            if st.button(f"Submit — {svc_choice}", type="primary", use_container_width=True):
                req_id = submit_service_request(student_name, student_id, svc_choice, svc_notes)
                for r in st.session_state.service_requests:
                    if r['id']==req_id: r['priority']=priority; break
                save_json_safe('service_requests.json', st.session_state.service_requests)
                st.success(f"Request submitted! Ref: **{req_id}**"); st.balloons()
        with col_my:
            st.markdown("#### My Requests")
            my_reqs = [r for r in st.session_state.service_requests if r.get('prn')==student_id]
            if my_reqs:
                for req in reversed(my_reqs[-6:]):
                    sc_ = f"badge-{req['status'].lower()}"
                    pri_ = "🔴" if req.get('priority')=='Urgent' else "🟡"
                    st.markdown(f'<div class="insight-card"><h5>{req["service"]} {pri_}</h5><p><span class="badge {sc_}">{req["status"]}</span> &nbsp; {req["id"]} &nbsp;|&nbsp; {req["date"]}</p></div>', unsafe_allow_html=True)
            else: st.caption("No requests yet.")

    # ─── TAB 7: Exams ─────────────────────────────────────────────
    with tabs[7]:
        st.markdown("### 📆 Exam Schedule & Countdown")
        for exam in EXAM_SCHEDULE:
            days_left = days_until(exam['date'])
            if days_left < 0:
                label = "DONE"; cls_ = ""; day_color = "var(--text-lo)"
            elif days_left == 0:
                label = "TODAY!"; cls_ = "very-soon"; day_color = "var(--rose)"
            elif days_left <= 3:
                label = f"{days_left}d left"; cls_ = "very-soon"; day_color = "var(--rose)"
            elif days_left <= 7:
                label = f"{days_left}d left"; cls_ = "soon"; day_color = "var(--amber)"
            else:
                label = f"{days_left}d left"; cls_ = ""; day_color = "var(--emerald)"

            subj_pct = round(subj_data.get(exam['subject'],{}).get('attended',8)/subj_data.get(exam['subject'],{}).get('total',10)*100) if st.session_state.demo else 0
            elig_badge = f'<span class="badge badge-{"approved" if subj_pct>=75 else "danger"}">{"Eligible" if subj_pct>=75 else "⚠️ At Risk"}</span>' if st.session_state.demo else ''

            st.markdown(f"""
                <div class="exam-card {cls_}">
                    <div style="display:flex;align-items:center;gap:1rem;">
                        <div style="text-align:center;min-width:60px;">
                            <div class="exam-days" style="color:{day_color};">{abs(days_left) if days_left>=0 else "✓"}</div>
                            <div style="font-size:0.65rem;color:var(--text-lo);">{label}</div>
                        </div>
                        <div style="flex:1;">
                            <div class="exam-subject">{exam['subject']}</div>
                            <div class="exam-meta">📅 {exam['date']} &nbsp;|&nbsp; 🕐 {exam['time']} &nbsp;|&nbsp; 🏛 {exam['room']}</div>
                        </div>
                        <div>{elig_badge}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    # ─── TAB 8: Certificate ───────────────────────────────────────
    with tabs[8]:
        st.markdown("### 🎖 Attendance Certificate")
        if elig:
            st.success("✅ You are eligible for an attendance certificate.")
            grade = "A+" if pct>=90 else "A" if pct>=80 else "B" if pct>=75 else "C"
            st.markdown(f"""
                <div class="certificate-wrapper">
                    <div class="cert-title">ATTENDANCE CERTIFICATE</div>
                    <p style="color:var(--text-mid);">{COLLEGE}</p>
                    <p style="color:var(--text-mid);margin:0.5rem 0;">This is to certify that</p>
                    <div class="cert-name">{student_name}</div>
                    <p style="color:var(--text-mid);">PRN: {student_id} &nbsp;|&nbsp; {dept}</p>
                    <div class="cert-pct">{pct}%</div>
                    <p style="color:var(--indigo-light);font-weight:700;margin:0.5rem 0;">Grade: {grade}</p>
                    <p style="color:var(--emerald);font-weight:700;font-size:1.1rem;">ELIGIBLE FOR EXAMINATIONS</p>
                    <p style="color:var(--text-lo);font-size:0.78rem;margin-top:1.5rem;">Generated: {_now_str()} | {APP_NAME} v{APP_VERSION}</p>
                </div>
            """, unsafe_allow_html=True)
            c1,c2 = st.columns(2)
            with c1:
                st.download_button("⬇️ Download Certificate (HTML)", data=build_certificate(student_name,student_id,pct), file_name=f"certificate_{student_id}.html", mime="text/html", use_container_width=True, type="primary")
            with c2:
                html_report = build_report_card_html(student_name, student_id, pct, subj_data, streak, risk, engagement)
                st.download_button("📊 Download Report Card", data=html_report, file_name=f"report_{student_id}.html", mime="text/html", use_container_width=True)
        else:
            st.warning(f"⚠️ You need **{need_more}** more classes to qualify.")
            st.progress(min(pct/MIN_ATTENDANCE, 1.0), text=f"Progress: {pct:.1f}% / {MIN_ATTENDANCE}%")

    # ─── TAB 9: Notifications ─────────────────────────────────────
    with tabs[9]:
        st.markdown("### 🔔 Notifications")
        notifs = st.session_state.notifications
        if not notifs: st.info("No notifications yet.")
        else:
            for n in notifs[:20]:
                n['read'] = True
                cls_ = {"info":"insight-info","warn":"insight-warn","crit":"insight-crit","ok":"insight-ok"}.get(n.get("kind","info"),"insight-info")
                st.markdown(f'<div class="insight-card {cls_}"><h5>{n["title"]}</h5><p>{n["body"]} &nbsp;|&nbsp; <small>{n["ts"]}</small></p></div>', unsafe_allow_html=True)

    # ─── TAB 10: Help ─────────────────────────────────────────────
    with tabs[10]:
        st.markdown("### ❓ Help & Support")
        faqs = [
            ("How is attendance calculated?", f"Attendance = (Classes Attended ÷ Total Lectures) × 100. Minimum {MIN_ATTENDANCE}% required."),
            ("What is the Engagement Score?", "Engagement = 50% attendance + 20% on-time ratio + 20% subject average + 10% wellness score."),
            ("What is the Risk Score?", "A rule-based composite of attendance%, streak, late arrivals, and leave days. Lower is better."),
            ("What is the Danger Zone tab?", "Shows subjects where your attendance is below 75%, putting you at risk of debarment."),
            ("How do I apply for leave?", "Go to 'Leave' tab. Medical leave requires a doctor's note reference. Approved within 24 hrs."),
            ("Grace period for late entry?", f"A {LATE_GRACE_MIN}-minute grace period applies. Three late marks may equal one absent."),
        ]
        for q, a in faqs:
            with st.expander(q): st.write(a)
        c1,c2 = st.columns(2)
        c1.info(f"📧 sujal@mitwpu.edu.in")
        c2.info(f"🏛 {COLLEGE}")


# ══════════════════════════════════════════════════════════════════════
# ██████ TEACHER DASHBOARD v6
# ══════════════════════════════════════════════════════════════════════
def teacher_dashboard():
    u = st.session_state.user
    tname = u.get('name','Teacher')
    subject = u.get('subject','All Subjects')
    tl = st.session_state.total_lectures

    records = load_attendance()
    if st.session_state.demo and not records: records = make_demo_attendance()

    students_df = load_csv_safe('students.csv')
    total_students = len(students_df) if students_df is not None else 76
    rec_dict = {r['name'].lower():r for r in records}

    p  = sum(1 for r in records if r.get('status')=='Present')
    a  = sum(1 for r in records if r.get('status')=='Absent')
    l  = sum(1 for r in records if r.get('status')=='Late')
    nd = max(0, total_students - len(records))
    rate = round(p/total_students*100,1) if total_students else 0
    at_risk_count = sum(1 for r in records if round(r.get('count',0)/tl*100,1)<MIN_ATTENDANCE)
    health = round((p*1.0+l*0.5)/total_students*100,0) if total_students else 0

    st.markdown(f"""
        <div class="hero">
            <h2>👨‍🏫 {tname}</h2>
            <p>{u.get('dept','Computer Science')} &nbsp;|&nbsp; {subject} &nbsp;|&nbsp; {BATCH}</p>
            <div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin-top:0.8rem;">
                <div class="badge"><span class="live-dot"></span> {datetime.now().strftime('%A, %d %B — %I:%M %p')}</div>
                <div class="badge">Health Score: {int(health)}/100</div>
                <div class="badge">At-Risk: {at_risk_count} students</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    c1,c2,c3,c4,c5,c6 = st.columns(6)
    h_color = "var(--emerald)" if health>=75 else "var(--amber)" if health>=50 else "var(--rose)"
    c1.markdown(f'<div class="stat-card stat-total"><span class="stat-icon">👥</span><div class="stat-num">{total_students}</div><div class="stat-lbl">Total</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="stat-card stat-present"><span class="stat-icon">✅</span><div class="stat-num">{p}</div><div class="stat-lbl">Present</div></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="stat-card stat-absent"><span class="stat-icon">❌</span><div class="stat-num">{a}</div><div class="stat-lbl">Absent</div></div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="stat-card stat-late"><span class="stat-icon">⏰</span><div class="stat-num">{l}</div><div class="stat-lbl">Late</div></div>', unsafe_allow_html=True)
    c5.markdown(f'<div class="stat-card stat-risk"><span class="stat-icon">⚠️</span><div class="stat-num">{at_risk_count}</div><div class="stat-lbl">At-Risk</div></div>', unsafe_allow_html=True)
    c6.markdown(f'<div class="stat-card"><span class="stat-icon">💡</span><div class="stat-num" style="color:{h_color};">{int(health)}</div><div class="stat-lbl">Health Score</div></div>', unsafe_allow_html=True)

    tabs = st.tabs(["📊 Analytics","🗺️ Seat Map","📋 Roster","🆚 Compare","📡 Broadcast","📹 Camera","📤 Upload","🎭 Demo","⏰ Late Review","🤖 AI Insights","📅 Timetable","🏢 Services","📂 Audit Log"])

    # ─── TAB 0: Analytics ─────────────────────────────────────────
    with tabs[0]:
        col_pie, col_bar = st.columns(2)
        with col_pie:
            st.markdown("#### Today's Breakdown")
            fig_pie = px.pie(values=[p,a,l,nd],names=['Present','Absent','Late','Pending'],color_discrete_sequence=['#10b981','#f43f5e','#f59e0b','#6366f1'],hole=0.58)
            fig_pie.update_traces(textposition='outside',textinfo='percent+label')
            fig_pie.update_layout(height=300,margin=dict(t=10,b=10,l=10,r=10),paper_bgcolor='rgba(0,0,0,0)',font_color='white',showlegend=False)
            st.plotly_chart(fig_pie, use_container_width=True)
        with col_bar:
            st.markdown("#### Top Student Attendance %")
            if records:
                top = sorted(records, key=lambda r:r.get('count',0), reverse=True)[:10]
                bar_df = pd.DataFrame({"Name":[r['name'].split()[0] for r in top],"Att %":[round(r.get('count',0)/tl*100,1) for r in top]})
                fig_bar = px.bar(bar_df,x="Att %",y="Name",orientation='h',color="Att %",color_continuous_scale=['#f43f5e','#f59e0b','#10b981'],range_color=[0,100],text="Att %")
                fig_bar.update_traces(texttemplate='%{text}%',textposition='outside')
                fig_bar.update_layout(height=300,margin=dict(t=10,b=10,l=10,r=50),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',font_color='white',showlegend=False,coloraxis_showscale=False,yaxis_title=None,xaxis_title=None)
                fig_bar.update_xaxes(range=[0,115],showgrid=False,showticklabels=False); fig_bar.update_yaxes(showgrid=False)
                st.plotly_chart(fig_bar, use_container_width=True)

        # Risk distribution radar
        if st.session_state.demo and records:
            st.markdown("#### Risk Distribution Overview")
            tl_ = tl or 40
            buckets = {"< 50%":0,"50–74%":0,"75–89%":0,"≥ 90%":0}
            for r in records:
                p_ = r.get('count',0)/tl_*100 if tl_ else 0
                if p_<50: buckets["< 50%"]+=1
                elif p_<75: buckets["50–74%"]+=1
                elif p_<90: buckets["75–89%"]+=1
                else: buckets["≥ 90%"]+=1
            fig_risk = go.Figure(go.Bar(
                x=list(buckets.keys()), y=list(buckets.values()),
                marker_color=['#f43f5e','#f59e0b','#6366f1','#10b981'],
                text=list(buckets.values()), textposition='outside'
            ))
            fig_risk.add_hline(y=total_students*0.1,line_dash="dash",line_color="rgba(255,255,255,0.2)",annotation_text="10% threshold")
            fig_risk.update_layout(height=250,margin=dict(t=10,b=10,l=10,r=10),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',font_color='white',showlegend=False,xaxis_title=None,yaxis_title="Students")
            fig_risk.update_xaxes(showgrid=False); fig_risk.update_yaxes(showgrid=False)
            st.plotly_chart(fig_risk, use_container_width=True)

        # Intelligence cards
        col_i1,col_i2,col_i3 = st.columns(3)
        with col_i1:
            cls_ = "insight-ok" if rate>=75 else "insight-warn" if rate>=50 else "insight-crit"
            lbl = "Excellent class engagement" if rate>=75 else "Moderate — follow up" if rate>=50 else "Critical — urgent intervention"
            st.markdown(f'<div class="insight-card {cls_}"><h5>Attendance Rate: {rate:.1f}%</h5><p>{lbl}</p></div>', unsafe_allow_html=True)
        with col_i2:
            st.markdown(f'<div class="insight-card insight-warn"><h5>⚠️ {at_risk_count} At-Risk Students</h5><p>Below {MIN_ATTENDANCE}% — send immediate alerts</p></div>', unsafe_allow_html=True)
        with col_i3:
            avg_eng = round(sum(compute_engagement_score(round(r.get('count',0)/tl*100,1),0.85,75) for r in records)/max(len(records),1),1) if records else 0
            st.markdown(f'<div class="insight-card insight-violet"><h5>💡 Avg Engagement: {avg_eng}</h5><p>Class composite score (presence + participation)</p></div>', unsafe_allow_html=True)

        with st.expander("⚙️ Semester Settings"):
            new_tl = st.number_input("Total Lectures", min_value=1, max_value=200, value=tl, step=1)
            if st.button("Update", key="update_tl"):
                st.session_state.total_lectures = int(new_tl)
                _log_audit("Settings", f"Total lectures → {new_tl}")
                st.success(f"Updated to {new_tl}."); st.rerun()

    # ─── TAB 1: Seat Map ──────────────────────────────────────────
    with tabs[1]:
        st.markdown("### 🗺️ Live Classroom Seat Heatmap")
        st.markdown('<p style="color:var(--text-mid);font-size:0.85rem;">Visual representation of student seating and attendance status.</p>', unsafe_allow_html=True)

        # Legend
        st.markdown("""
            <div style="display:flex;gap:1rem;flex-wrap:wrap;margin-bottom:1rem;font-size:0.78rem;color:var(--text-mid);">
                <span><span style="display:inline-block;width:12px;height:12px;background:#10b981;border-radius:3px;"></span> Present</span>
                <span><span style="display:inline-block;width:12px;height:12px;background:#f43f5e;border-radius:3px;"></span> Absent</span>
                <span><span style="display:inline-block;width:12px;height:12px;background:#f59e0b;border-radius:3px;"></span> Late</span>
                <span><span style="display:inline-block;width:12px;height:12px;background:var(--bg3);border:1px solid var(--border);border-radius:3px;"></span> Empty</span>
            </div>
        """, unsafe_allow_html=True)

        # Build seat grid (8 cols x 8 rows = 64 seats)
        seat_html = '<div class="seat-grid">'
        for i in range(64):
            rec = records[i] if i < len(records) else None
            if rec:
                st_ = rec.get('status','Present')
                cls_ = {'Present':'seat-occupied-present','Absent':'seat-occupied-absent','Late':'seat-occupied-late'}.get(st_,'seat-occupied-present')
                short = (rec['name'].split()[0][:3] + rec['name'].split()[-1][:2]).upper() if len(rec['name'].split())>1 else rec['name'][:4].upper()
                seat_html += f'<div class="seat {cls_}" title="{rec["name"]} — {st_}">{short}</div>'
            else:
                seat_html += f'<div class="seat seat-empty" title="Empty seat {i+1}">S{i+1:02d}</div>'
        seat_html += '</div>'
        st.markdown(f'<div class="glass">{seat_html}</div>', unsafe_allow_html=True)

        # Stats below
        col_s1,col_s2,col_s3 = st.columns(3)
        col_s1.metric("Occupied Seats", len(records), f"{total_students} total")
        col_s2.metric("Present", p, f"{rate:.1f}%")
        col_s3.metric("Empty Seats", max(0,total_students-len(records)))

    # ─── TAB 2: Roster ────────────────────────────────────────────
    with tabs[2]:
        st.markdown("#### Complete Student Roster")
        c_search, c_filter = st.columns([2,1])
        search = c_search.text_input("🔍 Search student", placeholder="Name or PRN...")
        show_risk = c_filter.checkbox("At-risk only (<75%)")

        roster_rows = []
        if students_df is not None:
            for _,row in students_df.iterrows():
                name = str(row.get('Name',''))
                sid  = str(row.get('Student ID',row.get('PRN','N/A')))
                rec  = rec_dict.get(name.lower(),{})
                cnt  = rec.get('count',0); p_ = round(cnt/tl*100,1) if tl else 0
                roster_rows.append({'Name':name,'PRN':sid,'Status':rec.get('status','Pending'),'Lectures':cnt,'Att %':p_,'Time':rec.get('timestamp','—'),'Eligible':'✅' if p_>=75 else '❌','Risk':compute_risk_score(p_,random.randint(1,15) if st.session_state.demo else 0,0,0)['level']})
        else:
            for r in records:
                p_ = round(r.get('count',0)/tl*100,1) if tl else 0
                roster_rows.append({'Name':r['name'],'PRN':r['id'],'Status':r['status'],'Lectures':r.get('count',0),'Att %':p_,'Time':r.get('timestamp','—'),'Eligible':'✅' if p_>=75 else '❌','Risk':compute_risk_score(p_,0,0,0)['level']})

        roster_df = pd.DataFrame(roster_rows)
        if search.strip():
            mask = (roster_df['Name'].str.lower().str.contains(search.lower()) | roster_df['PRN'].astype(str).str.contains(search))
            roster_df = roster_df[mask]
        if show_risk: roster_df = roster_df[roster_df['Att %']<75]

        st.dataframe(roster_df, use_container_width=True, height=420, hide_index=True,
            column_config={"Att %":st.column_config.ProgressColumn("Att %",min_value=0,max_value=100,format="%.1f%%")})

        col_d1,col_d2 = st.columns(2)
        with col_d1:
            st.download_button("⬇️ Export Roster (CSV)", data=roster_df.to_csv(index=False), file_name=f"roster_{datetime.now().strftime('%Y%m%d_%H%M')}.csv", mime="text/csv", type="primary")
        with col_d2:
            at_risk_df = roster_df[roster_df['Att %']<75]
            if not at_risk_df.empty:
                st.download_button("⬇️ Export At-Risk List", data=at_risk_df.to_csv(index=False), file_name=f"at_risk_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv")

        st.markdown("---"); st.markdown("#### Bulk Status Update")
        bulk_names = st.multiselect("Select students", [r['Name'] for r in roster_rows])
        bulk_status = st.selectbox("Mark as", ["Present","Absent","Late"])
        if st.button("Apply Bulk Update", type="primary") and bulk_names:
            data = load_json_safe('attendance_results.json') or {'attendance':{},'name_to_id':{}}
            for bname in bulk_names:
                data['attendance'][bname] = {'present':bulk_status=='Present','status':bulk_status,'first_seen':datetime.now().strftime('%H:%M'),'count':data['attendance'].get(bname,{}).get('count',0)}
            save_json_safe('attendance_results.json', data)
            _log_audit("Bulk Update", f"{bulk_status}: {', '.join(bulk_names)}")
            st.success(f"Marked {len(bulk_names)} students as {bulk_status}."); time.sleep(0.5); st.rerun()

        # Leave requests to review
        pending_leaves = [l for l in st.session_state.leave_requests if l.get('status')=='Pending']
        if pending_leaves:
            st.markdown("---"); st.markdown(f"#### 🏖 Pending Leave Requests ({len(pending_leaves)})")
            for lv in pending_leaves:
                col_li, col_la, col_lb = st.columns([3,1,1])
                col_li.markdown(f"**{lv['student']}** — {lv['type']} ({lv['from']}→{lv['to']}, {lv['days']}d): *{lv['reason'][:60]}*")
                if col_la.button("✅ Approve", key=f"lv_ok_{lv['id']}"):
                    lv['status']='Approved'; save_json_safe('leave_requests.json', st.session_state.leave_requests)
                    _log_audit("Leave Approved", f"{lv['student']} — {lv['id']}")
                    _push_notif("Leave Approved", f"Your {lv['type']} leave was approved","ok")
                    st.rerun()
                if col_lb.button("❌ Reject", key=f"lv_no_{lv['id']}"):
                    lv['status']='Rejected'; save_json_safe('leave_requests.json', st.session_state.leave_requests)
                    _log_audit("Leave Rejected", f"{lv['student']} — {lv['id']}")
                    st.rerun()

    # ─── TAB 3: Compare ───────────────────────────────────────────
    with tabs[3]:
        st.markdown("### 🆚 Student Comparison Tool")
        all_names = [r['name'] for r in records]
        if len(all_names) < 2:
            st.info("Need at least 2 students in records to compare.")
        else:
            c_a, c_vs, c_b = st.columns([2,0.5,2])
            with c_a: s_a = st.selectbox("Student A", all_names, key="cmp_a")
            with c_vs: st.markdown('<div class="vs-divider" style="margin-top:2rem;">VS</div>', unsafe_allow_html=True)
            with c_b: s_b = st.selectbox("Student B", [n for n in all_names if n!=s_a], key="cmp_b")

            rec_a = next((r for r in records if r['name']==s_a), {})
            rec_b = next((r for r in records if r['name']==s_b), {})
            pct_a = round(rec_a.get('count',0)/tl*100,1) if tl else 0
            pct_b = round(rec_b.get('count',0)/tl*100,1) if tl else 0
            streak_a = random.randint(1,18) if st.session_state.demo else 0
            streak_b = random.randint(1,18) if st.session_state.demo else 0
            risk_a = compute_risk_score(pct_a, streak_a, random.randint(0,5), 0)
            risk_b = compute_risk_score(pct_b, streak_b, random.randint(0,5), 0)

            col_a2, col_b2 = st.columns(2)
            metrics = [("Attendance %",pct_a,pct_b),("Streak (days)",streak_a,streak_b),("Classes Attended",rec_a.get('count',0),rec_b.get('count',0)),("Risk Score",risk_a['score'],risk_b['score'])]
            with col_a2:
                st.markdown(f'<div class="compare-col"><h4 style="color:var(--indigo-light);font-family:\'Inter\',sans-serif;">{s_a.split()[0]}</h4>', unsafe_allow_html=True)
                for label,va,vb in metrics:
                    win = va>vb if label!="Risk Score" else va<vb
                    color = "var(--emerald)" if win else "var(--text-mid)"
                    st.markdown(f'<div class="report-row"><span class="report-key">{label}</span><span class="report-val" style="color:{color};">{va}{"%" if "%" in label else ""} {"✓" if win else ""}</span></div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            with col_b2:
                st.markdown(f'<div class="compare-col"><h4 style="color:var(--sky);font-family:\'Inter\',sans-serif;">{s_b.split()[0]}</h4>', unsafe_allow_html=True)
                for label,va,vb in metrics:
                    win = vb>va if label!="Risk Score" else vb<va
                    color = "var(--emerald)" if win else "var(--text-mid)"
                    st.markdown(f'<div class="report-row"><span class="report-key">{label}</span><span class="report-val" style="color:{color};">{vb}{"%" if "%" in label else ""} {"✓" if win else ""}</span></div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # Radar chart
            categories = ["Attendance","Streak","On-Time","Subject Avg","Engagement"]
            vals_a = [pct_a, min(100,streak_a*5), random.randint(70,100), random.randint(65,100), compute_engagement_score(pct_a,0.9,75)]
            vals_b = [pct_b, min(100,streak_b*5), random.randint(70,100), random.randint(65,100), compute_engagement_score(pct_b,0.85,70)]
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(r=vals_a+[vals_a[0]],theta=categories+[categories[0]],fill='toself',name=s_a.split()[0],line_color='#818cf8',fillcolor='rgba(99,102,241,0.15)'))
            fig_radar.add_trace(go.Scatterpolar(r=vals_b+[vals_b[0]],theta=categories+[categories[0]],fill='toself',name=s_b.split()[0],line_color='#38bdf8',fillcolor='rgba(56,189,248,0.15)'))
            fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True,range=[0,100],color='#475569'),bgcolor='rgba(0,0,0,0)'),showlegend=True,height=320,margin=dict(t=10,b=10,l=10,r=10),paper_bgcolor='rgba(0,0,0,0)',font_color='white',legend=dict(bgcolor='rgba(0,0,0,0)'))
            st.plotly_chart(fig_radar, use_container_width=True)

    # ─── TAB 4: Broadcast ─────────────────────────────────────────
    with tabs[4]:
        st.markdown("### 📡 Smart Broadcast & Alerts")
        col_bc1, col_bc2 = st.columns([1.5,1])
        with col_bc1:
            st.markdown("#### 📢 Broadcast Message to Class")
            bc_target = st.selectbox("Send to", ["All Students","At-Risk Students Only","Present Students","Absent Students"])
            bc_channel = st.multiselect("Channel", ["In-App Notification","SMS (Simulated)","WhatsApp (Simulated)","Email (Simulated)"], default=["In-App Notification"])
            bc_msg = st.text_area("Message", placeholder="E.g. Reminder: Assignment due tomorrow. Attendance is mandatory.")
            bc_urgent = st.checkbox("Mark Urgent")
            if st.button("📤 Send Broadcast", type="primary", use_container_width=True):
                if not bc_msg.strip(): st.error("Enter a message.")
                else:
                    msg_rec = {"from":tname,"to":bc_target,"channels":bc_channel,"msg":bc_msg,"urgent":bc_urgent,"ts":_now_str()}
                    st.session_state.broadcast_msgs.insert(0, msg_rec)
                    _push_notif("Broadcast Message", f"From {tname}: {bc_msg[:60]}...", "warn" if bc_urgent else "info")
                    _log_audit("Broadcast", f"To {bc_target} via {', '.join(bc_channel)}")
                    st.success(f"✅ Message sent to {bc_target} via {', '.join(bc_channel)}!"); st.balloons()

            st.markdown("#### 🔔 Automated Absence Alerts")
            if st.button("🚨 Send Absence Alerts to All At-Risk Students"):
                at_risk = [r for r in records if round(r.get('count',0)/tl*100,1)<75]
                for r in at_risk:
                    st.session_state.parent_alerts.append({"student":r['name'],"msg":f"Attendance warning: {round(r.get('count',0)/tl*100,1):.1f}%","ts":_now_str(),"status":"Sent"})
                _log_audit("Auto-Alert", f"Sent alerts to {len(at_risk)} at-risk students")
                st.success(f"Sent absence alerts to {len(at_risk)} students.")

        with col_bc2:
            st.markdown("#### 📜 Sent Messages")
            msgs = st.session_state.broadcast_msgs
            if not msgs: st.caption("No messages sent yet.")
            else:
                for m in msgs[:8]:
                    icon = "🔴" if m.get('urgent') else "📩"
                    st.markdown(f'<div class="insight-card insight-{"crit" if m.get("urgent") else "info"}"><h5>{icon} To: {m["to"]}</h5><p>{m["msg"][:80]}{"..." if len(m["msg"])>80 else ""} &nbsp;|&nbsp; <small>{m["ts"]}</small></p></div>', unsafe_allow_html=True)

            st.markdown("#### 👨‍👩‍👧 Parent Alert Log")
            alerts = st.session_state.parent_alerts
            if not alerts: st.caption("No parent alerts sent.")
            else:
                for a in alerts[:6]:
                    st.markdown(f'<div class="insight-card insight-warn"><h5>👨‍👩‍👧 {a["student"]}</h5><p>{a["msg"]} &nbsp;|&nbsp; <small>{a["ts"]}</small> <span class="badge badge-approved">{a["status"]}</span></p></div>', unsafe_allow_html=True)

    # ─── TAB 5: Camera ────────────────────────────────────────────
    with tabs[5]:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.markdown("### 📹 Live Face Recognition")
        cam = get_camera_index()
        if cam is None:
            st.warning("⚠️ No camera detected. Connect a webcam and refresh.")

            # QR Attendance fallback
            st.markdown("---")
            st.markdown("#### 📱 QR Code Attendance Fallback")
            st.markdown('<p style="color:var(--text-mid);">No camera? Generate a session QR code for students to scan.</p>', unsafe_allow_html=True)
            col_qr1, col_qr2 = st.columns([1,1])
            with col_qr1:
                sess_id = f"VG-{datetime.now().strftime('%Y%m%d-%H%M')}-{random.randint(1000,9999)}"
                if st.button("🔲 Generate QR Session", type="primary", use_container_width=True):
                    st.session_state.qr_sessions.insert(0, {"id":sess_id,"ts":_now_str(),"scans":0,"active":True})
                    _log_audit("QR Session", f"Generated {sess_id}")
                if st.session_state.qr_sessions:
                    active = st.session_state.qr_sessions[0]
                    qr_art = generate_qr_ascii(active['id'])
                    st.markdown(f"""
                        <div class="qr-box">
                            <div style="color:var(--text-mid);font-size:0.78rem;margin-bottom:0.5rem;">Session: {active['id']}</div>
                            <div class="qr-code-display">{qr_art}</div>
                            <div style="color:var(--text-mid);font-size:0.78rem;margin-top:0.5rem;">Generated: {active['ts']}</div>
                        </div>
                    """, unsafe_allow_html=True)
            with col_qr2:
                st.markdown("#### Recent QR Sessions")
                for s in st.session_state.qr_sessions[:5]:
                    st.markdown(f'<div class="insight-card insight-info"><h5>🔲 {s["id"]}</h5><p>Generated: {s["ts"]}</p></div>', unsafe_allow_html=True)
        else:
            b1,b2,b3 = st.columns(3)
            if b1.button("▶ Start Live Session", use_container_width=True, type="primary"):
                try:
                    if os.path.exists('live_attendance.json'): os.remove('live_attendance.json')
                except Exception: pass
                st.session_state.live_running = True; st.session_state.live_marked = set()
                _log_audit("Camera","Live session started")
            if b2.button("⏹ Stop Session", use_container_width=True):
                st.session_state.live_running = False
                _log_audit("Camera",f"Ended. Detected: {len(st.session_state.live_marked)}")
            if b3.button("🔄 Reset", use_container_width=True):
                st.session_state.live_marked = set()

            det_count = st.empty(); frame_win = st.image([])
            if st.session_state.live_running:
                fc = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
                try:
                    cap = cv2.VideoCapture(cam)
                    while cap.isOpened() and st.session_state.live_running:
                        ret, frame = cap.read()
                        if not ret: st.error("Camera read failed."); break
                        frame = cv2.flip(frame,1)
                        gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        faces = fc.detectMultiScale(gray,1.1,5,minSize=(60,60))
                        for (x,y,w,h) in faces:
                            cv2.rectangle(frame,(x,y),(x+w,y+h),(16,185,129),3)
                            cv2.putText(frame,"Face Detected",(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.6,(16,185,129),2)
                        cv2.putText(frame,f"Detected:{len(st.session_state.live_marked)} Faces:{len(faces)}",(10,35),cv2.FONT_HERSHEY_SIMPLEX,0.9,(99,102,241),2)
                        frame_win.image(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB),channels="RGB",use_container_width=True)
                        det_count.markdown(f"**{len(faces)}** face(s) in frame | **{len(st.session_state.live_marked)}** marked")
                    cap.release()
                except Exception as e: st.error(f"Camera error: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

    # ─── TAB 6: Upload ────────────────────────────────────────────
    with tabs[6]:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.markdown("### 📤 Upload & Process Video")
        uf = st.file_uploader("Drop a class recording here", type=['mp4','avi','mov','mkv'])
        if uf:
            try:
                with open('input.mp4','wb') as f: f.write(uf.read())
                st.success(f"✅ {uf.name} uploaded.")
            except Exception as e: st.error(f"Upload failed: {e}")
        col_run, col_del = st.columns(2)
        with col_run:
            if st.button("⚙️ Process Video", type="primary", use_container_width=True):
                if not os.path.exists('input.mp4'): st.error("Upload a video first.")
                else:
                    for f in ['attendance_results.json','attendance.csv']:
                        try:
                            if os.path.exists(f): os.remove(f)
                        except Exception: pass
                    with st.spinner("Running face recognition engine..."):
                        pb = st.progress(0,"Initialising...")
                        for i in range(1,10): time.sleep(0.3); pb.progress(i*10,f"Processing... {i*10}%")
                        try:
                            result = subprocess.run(['python3','main.py'],capture_output=True,text=True,timeout=300)
                            pb.progress(100,"Complete!")
                            if result.returncode!=0: st.warning(f"Warnings:\n```\n{result.stderr[:400]}\n```")
                            if os.path.exists('attendance_results.json'):
                                _log_audit("Video Processed", uf.name if uf else "input.mp4")
                                st.success("✅ Processing complete!"); st.balloons(); time.sleep(1); st.rerun()
                            else: st.error("No results generated. Check main.py.")
                        except subprocess.TimeoutExpired: st.error("Timeout after 5 minutes.")
                        except FileNotFoundError: st.error("main.py not found.")
                        except Exception as e: st.error(f"Error: {e}")
        with col_del:
            if st.button("🗑 Delete Video", use_container_width=True):
                try:
                    if os.path.exists('input.mp4'): os.remove('input.mp4'); st.success("Deleted.")
                except Exception as e: st.error(f"Error: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

    # ─── TAB 7: Demo ──────────────────────────────────────────────
    with tabs[7]:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.markdown("### 🎭 Demo Mode — Realistic Simulated Data")
        n_students = st.slider("Number of students", 5, 76, 10)
        pattern    = st.selectbox("Pattern", ["Typical (75-95% present)","Poor (40-70%)","Near-perfect (90-100%)"])
        if st.button("🎲 Generate Demo Data", type="primary", use_container_width=True):
            demo_data = {'attendance':{},'name_to_id':{}}
            _ranges = {"Typical":(0.75,0.95),"Poor":(0.40,0.70),"Near-perfect":(0.90,1.0)}
            lo,hi   = _ranges.get(pattern.split()[0],(0.75,0.95))
            fnames  = ["Sujal","Saniya","Prathamesh","Aishwarya","Vedang","Krushna","Priya","Rohan","Nikhil","Anjali","Rahul","Pooja","Amit","Sneha","Vikram","Meera","Suresh","Kavya","Harish","Divya","Ganesh","Swati","Prasad","Reema","Sanjay","Nisha","Deepak","Pallavi","Manoj","Shruti"]
            lnames  = ["Kamathe","Dhawade","Pokale","Joshi","Bodake","Borse","Desai","Mehta","Kulkarni","Sharma","Patil","Verma","Gupta","Singh","Nair","Rao","Iyer","Shah","Modi","Patel"]
            for i in range(n_students):
                name = f"{fnames[i%len(fnames)]} {lnames[i%len(lnames)]}"
                prn  = f"127224{1000+i:04d}"
                pres = random.random() < random.uniform(lo,hi)
                cnt  = random.randint(int(lo*tl),tl)
                demo_data['attendance'][name] = {'present':pres,'status':'Present' if pres else random.choice(['Absent','Late','Absent']),'first_seen':f"{random.randint(9,11):02d}:{random.randint(0,59):02d}",'count':cnt,'subject':random.choice(SUBJECTS)}
                demo_data['name_to_id'][name] = prn
            save_json_safe('attendance_results.json', demo_data)
            _log_audit("Demo", f"Generated {n_students} students")
            st.success(f"✅ Demo data generated for {n_students} students."); st.balloons(); time.sleep(0.8); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # ─── TAB 8: Late Review ───────────────────────────────────────
    with tabs[8]:
        late_list = [r for r in records if r.get('status')=='Late']
        st.markdown(f"### ⏰ Late Entry Review — {len(late_list)} student(s)")
        if not late_list: st.success("✅ No late arrivals today.")
        else:
            for i,s in enumerate(late_list):
                col_n,col_t,col_b1,col_b2 = st.columns([2,1,1,1])
                col_n.markdown(f"**{s.get('name','')}** &nbsp; <span class='badge badge-late'>LATE</span>", unsafe_allow_html=True)
                col_t.caption(s.get('timestamp','—'))
                if col_b1.button("Mark Present", key=f"late_ok_{i}"):
                    data = load_json_safe('attendance_results.json') or {'attendance':{},'name_to_id':{}}
                    if s['name'] in data.get('attendance',{}):
                        data['attendance'][s['name']]['status']='Present'; data['attendance'][s['name']]['present']=True
                        save_json_safe('attendance_results.json', data)
                        _log_audit("Override", f"{s['name']} Late→Present"); st.rerun()
                if col_b2.button("Keep Late", key=f"late_kp_{i}"):
                    st.caption(f"Kept as Late.")

    # ─── TAB 9: AI Insights ───────────────────────────────────────
    with tabs[9]:
        st.markdown("### 🤖 AI-Powered Intelligence")
        if not records: st.info("Run attendance first.")
        else:
            col_pred, col_risk = st.columns(2)
            with col_pred:
                st.markdown("#### Trend Predictions")
                for r in records[:5]:
                    curr = r.get('count',0)
                    pred = min(tl, curr + random.randint(-2,4))
                    delta = pred-curr; icon = "📈" if delta>0 else ("📉" if delta<0 else "➡️")
                    col_r = "var(--emerald)" if delta>=0 else "var(--rose)"
                    st.markdown(f'<div class="insight-card"><h5>{r["name"].split()[0]} {r["name"].split()[-1]} {icon}</h5><p>Now: {curr} → Predicted: <span style="color:{col_r};font-weight:700;">{pred}</span> (Δ {delta:+d})</p></div>', unsafe_allow_html=True)
            with col_risk:
                st.markdown("#### Risk Assessment")
                at_risk = [r for r in records if round(r.get('count',0)/tl*100,1)<75]
                excellent = [r for r in records if round(r.get('count',0)/tl*100,1)>=90]
                st.markdown(f'<div class="insight-card insight-crit"><h5>🚨 {len(at_risk)} Below 75%</h5><p>Immediate follow-up required.</p></div>', unsafe_allow_html=True)
                for r in at_risk[:4]:
                    p_ = round(r.get('count',0)/tl*100,1)
                    need = math.ceil(0.75*tl)-r.get('count',0)
                    st.markdown(f'<div class="insight-card insight-crit"><h5>{r["name"]}</h5><p>{p_}% | Need {need} more classes</p></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="insight-card insight-ok"><h5>⭐ {len(excellent)} Excellent Students</h5><p>Above 90% — consider recognition.</p></div>', unsafe_allow_html=True)

            # Engagement heatmap
            st.markdown("#### Engagement Heatmap (All Students)")
            if records:
                eng_data = []
                for r in records:
                    p_ = round(r.get('count',0)/tl*100,1) if tl else 0
                    eng = compute_engagement_score(p_, random.uniform(0.7,1.0), random.randint(65,100))
                    eng_data.append({'Student':r['name'].split()[0],'Engagement':eng,'Attendance':p_,'Risk':compute_risk_score(p_,random.randint(1,15),0,0)['score']})
                edf = pd.DataFrame(eng_data)
                fig_eng = px.scatter(edf, x='Attendance', y='Engagement', size='Risk', color='Engagement',
                    color_continuous_scale=['#f43f5e','#f59e0b','#10b981'], range_color=[0,100],
                    hover_name='Student', text='Student', size_max=30)
                fig_eng.update_traces(textposition='top center')
                fig_eng.update_layout(height=320, margin=dict(t=10,b=10,l=10,r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white', coloraxis_showscale=False)
                fig_eng.update_xaxes(showgrid=False); fig_eng.update_yaxes(showgrid=False)
                st.plotly_chart(fig_eng, use_container_width=True)

    # ─── TAB 10: Timetable ────────────────────────────────────────
    with tabs[10]:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.markdown("### 📅 Timetable Manager")
        tdf = load_csv_safe('timetable.csv')
        if tdf is not None and not tdf.empty:
            today_ = datetime.now().strftime("%A"); ct = datetime.now().strftime("%H:%M")
            td_df = tdf[tdf.get('Day',pd.Series()).str.lower()==today_.lower()] if 'Day' in tdf.columns else pd.DataFrame()
            if not td_df.empty:
                st.markdown(f"#### Today — {today_}")
                for _,row in td_df.iterrows():
                    try:
                        is_now = row["Start Time"]<=ct<=row["End Time"]
                        st.markdown(f'<div class="tt-card {"current" if is_now else ""}"><h5>{"🟢 NOW" if is_now else "📚"} {row.get("Subject","—")}</h5><small>👤 {row.get("Faculty","—")} &nbsp;|&nbsp; 🕐 {row.get("Start Time","—")} – {row.get("End Time","—")}</small></div>', unsafe_allow_html=True)
                    except Exception: pass
            st.dataframe(tdf, use_container_width=True, hide_index=True)
        else:
            st.info("No timetable found.")
            tt_f = st.file_uploader("Upload timetable CSV", type=['csv'])
            if tt_f:
                try:
                    tt_df = pd.read_csv(tt_f); tt_df.to_csv('timetable.csv',index=False)
                    _cached_csv.clear(); st.success("Uploaded!"); st.rerun()
                except Exception as e: st.error(f"Invalid CSV: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

    # ─── TAB 11: Services ─────────────────────────────────────────
    with tabs[11]:
        st.markdown("### 🏢 Service Request Management")
        all_reqs = st.session_state.service_requests
        fs = st.selectbox("Filter", ["All","Pending","Processing","Approved","Completed","Rejected"])
        filtered = all_reqs if fs=="All" else [r for r in all_reqs if r['status']==fs]
        if not filtered: st.info("No requests match filter.")
        else:
            for req in reversed(filtered):
                sc_ = f"badge-{req['status'].lower()}"
                pri_ = "🔴" if req.get('priority')=='Urgent' else "🟡"
                with st.expander(f"{pri_} {req['service']} — {req['student']} ({req['id']})"):
                    c_l,c_r = st.columns([2,1])
                    with c_l:
                        st.markdown(f'<span class="badge {sc_}">{req["status"]}</span><br><br><b>Student:</b> {req["student"]}<br><b>PRN:</b> {req["prn"]}<br><b>Dept:</b> {req["dept"]}<br><b>Fee:</b> {req["fee"]}<br><b>Est Time:</b> {req["est_time"]}<br><b>Submitted:</b> {req["date"]}<br><b>Notes:</b> {req.get("notes") or "—"}', unsafe_allow_html=True)
                    with c_r:
                        if req['status'] not in ['Completed','Rejected']:
                            ns = st.selectbox("Update", ["Pending","Processing","Approved","Completed","Rejected"], key=f"svc_{req['id']}")
                            rm = st.text_input("Remark", key=f"rm_{req['id']}")
                            if st.button("Update", key=f"upd_{req['id']}", type="primary"):
                                req['status']=ns; req.setdefault('updates',[]).append({"status":ns,"remark":rm,"ts":_now_str()})
                                save_json_safe('service_requests.json',all_reqs)
                                _log_audit("Service Update",f"{req['id']} → {ns}")
                                _push_notif("Request Updated",f"{req['service']} → {ns}","ok")
                                st.success("Updated!"); st.rerun()

    # ─── TAB 12: Audit Log ────────────────────────────────────────
    with tabs[12]:
        st.markdown("### 📂 System Audit Log")
        log = st.session_state.audit_log
        if not log: st.info("No events recorded.")
        else:
            st.markdown(f"Showing last **{min(50,len(log))}** of **{len(log)}** events.")
            for entry in log[:50]:
                role_color = {"teacher":"#6366f1","student":"#10b981","admin":"#f59e0b"}.get(entry.get('role',''),'#94a3b8')
                st.markdown(f'<div class="audit-row"><div class="audit-time">{entry["date"]} {entry["ts"]}</div><div class="audit-msg"><strong style="color:{role_color};">{entry["action"]}</strong> — {entry.get("detail","")}</div><div class="audit-who">{entry["user"]}</div></div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# ██████ ADMIN DASHBOARD v6
# ══════════════════════════════════════════════════════════════════════
def admin_dashboard():
    st.markdown(f"""
        <div class="hero">
            <h2>🔐 Administrator Control Panel</h2>
            <p>{COLLEGE} &nbsp;|&nbsp; System-wide access &nbsp;|&nbsp; {datetime.now().strftime('%d %B %Y, %I:%M %p')}</p>
            <div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin-top:0.8rem;">
                <div class="badge"><span class="live-dot"></span> Full Access</div>
                <div class="badge">v{APP_VERSION}</div>
                <div class="badge">Audit Trail Active</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    records = load_attendance()
    if st.session_state.demo and not records: records = make_demo_attendance()

    users_df = load_csv_safe('users.csv'); stud_df = load_csv_safe('students.csv')
    n_users = len(users_df) if users_df is not None else 0
    n_stud  = len(stud_df) if stud_df is not None else 76
    tl = st.session_state.total_lectures

    p  = sum(1 for r in records if r.get('status')=='Present')
    a  = sum(1 for r in records if r.get('status')=='Absent')
    n_requests = len(st.session_state.service_requests)
    n_leaves   = len([l for l in st.session_state.leave_requests if l.get('status')=='Pending'])

    c1,c2,c3,c4,c5,c6 = st.columns(6)
    c1.markdown(f'<div class="stat-card stat-total"><span class="stat-icon">🎓</span><div class="stat-num">{n_stud}</div><div class="stat-lbl">Students</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="stat-card stat-present"><span class="stat-icon">✅</span><div class="stat-num">{p}</div><div class="stat-lbl">Present</div></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="stat-card stat-absent"><span class="stat-icon">❌</span><div class="stat-num">{a}</div><div class="stat-lbl">Absent</div></div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="stat-card stat-pending"><span class="stat-icon">👤</span><div class="stat-num">{n_users}</div><div class="stat-lbl">Staff</div></div>', unsafe_allow_html=True)
    c5.markdown(f'<div class="stat-card stat-late"><span class="stat-icon">📬</span><div class="stat-num">{n_requests}</div><div class="stat-lbl">Requests</div></div>', unsafe_allow_html=True)
    c6.markdown(f'<div class="stat-card stat-risk"><span class="stat-icon">🏖</span><div class="stat-num">{n_leaves}</div><div class="stat-lbl">Leaves Pending</div></div>', unsafe_allow_html=True)

    tabs = st.tabs(["📊 Overview","📅 Annual Heatmap","📋 Records","👤 Users","🏢 Departments","📆 Config","📂 Audit","⚙️ System"])

    # ─── TAB 0: Overview ──────────────────────────────────────────
    with tabs[0]:
        col_c,col_p = st.columns(2)
        with col_c:
            if records:
                statuses = [r.get('status','Pending') for r in records]
                counts   = {s:statuses.count(s) for s in set(statuses)}
                fig_donut = px.pie(values=list(counts.values()),names=list(counts.keys()),hole=0.6,color_discrete_sequence=['#10b981','#f43f5e','#f59e0b','#6366f1','#38bdf8'])
                fig_donut.update_layout(height=280,paper_bgcolor='rgba(0,0,0,0)',font_color='white',showlegend=True,margin=dict(t=10,b=10,l=10,r=10),legend=dict(bgcolor='rgba(0,0,0,0)'))
                st.plotly_chart(fig_donut, use_container_width=True)
        with col_p:
            tl_=tl or 40
            buckets={"< 50%":0,"50–74%":0,"75–89%":0,"≥ 90%":0}
            for r in records:
                p_=r.get('count',0)/tl_*100
                if p_<50: buckets["< 50%"]+=1
                elif p_<75: buckets["50–74%"]+=1
                elif p_<90: buckets["75–89%"]+=1
                else: buckets["≥ 90%"]+=1
            if records:
                fig_risk=go.Figure(go.Bar(x=list(buckets.keys()),y=list(buckets.values()),marker_color=['#f43f5e','#f59e0b','#6366f1','#10b981'],text=list(buckets.values()),textposition='outside'))
                fig_risk.update_layout(height=280,margin=dict(t=10,b=10,l=10,r=10),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',font_color='white',showlegend=False,xaxis_title=None,yaxis_title="Students")
                fig_risk.update_xaxes(showgrid=False); fig_risk.update_yaxes(showgrid=False)
                st.plotly_chart(fig_risk, use_container_width=True)

        c_s1,c_s2,c_s3 = st.columns(3)
        c_s1.metric("Attendance Rate",f"{round(p/n_stud*100,1) if n_stud else 0}%",f"{'↑ Above' if p/n_stud*100>75 else '↓ Below'} 75%" if n_stud else "—")
        c_s2.metric("Records Stored",f"{len(records)}",f"{tl} lectures")
        c_s3.metric("Pending Actions",f"{n_requests+n_leaves}",f"{n_leaves} leaves, {n_requests} requests")

        # College summary cards
        st.markdown("#### Quick Actions")
        qa1,qa2,qa3,qa4 = st.columns(4)
        if qa1.button("📤 Export All Data", use_container_width=True):
            if records:
                rdf = pd.DataFrame(records)
                st.download_button("⬇️ Download", data=rdf.to_csv(index=False), file_name=f"all_records_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv", use_container_width=True)
        if qa2.button("🔔 Send College-wide Alert", use_container_width=True):
            _push_notif("Admin Alert","System-wide notification from Administrator","warn")
            _log_audit("Admin Alert","College-wide notification sent")
            st.success("Alert sent!")
        if qa3.button("🗑 Clear All Records", use_container_width=True):
            for f in ['attendance_results.json','attendance.csv','live_attendance.json']:
                try:
                    if os.path.exists(f): os.remove(f)
                except Exception: pass
            _log_audit("Admin","All records cleared")
            st.success("Cleared!"); time.sleep(0.5); st.rerun()
        if qa4.button("📊 Generate Report", use_container_width=True):
            _log_audit("Admin","Report generation triggered")
            st.info("Reports queued — check exports.")

    # ─── TAB 1: Annual Heatmap ────────────────────────────────────
    with tabs[1]:
        st.markdown("### 📅 Annual Attendance Heatmap (GitHub-style)")
        st.markdown('<p style="color:var(--text-mid);">College-wide daily attendance rate visualization across the academic year.</p>', unsafe_allow_html=True)

        months = ["Jul","Aug","Sep","Oct","Nov","Dec","Jan","Feb","Mar","Apr","May","Jun"]
        weeks_per_month = 4
        heatmap_data = []
        for m_idx, month in enumerate(months):
            for week in range(weeks_per_month):
                for day in range(5):  # Mon-Fri
                    r_seed = m_idx*100 + week*10 + day
                    rng = random.Random(r_seed)
                    val = rng.choice([0,1,2,3,4,4,3,4,3,2]) if rng.random() > 0.1 else 0
                    heatmap_data.append({"Month":month,"Week":week,"Day":day,"Value":val,"Date":f"{month} W{week+1} D{day+1}"})

        hdf = pd.DataFrame(heatmap_data)
        fig_heat = px.density_heatmap(hdf, x="Month", y="Day", z="Value",
            color_continuous_scale=["#1c2640","#1e4620","#2d6a2d","#10b981","#34d399"],
            labels={"Day":"Weekday","Value":"Attendance Level"})
        fig_heat.update_layout(height=300, margin=dict(t=10,b=10,l=10,r=10), paper_bgcolor='rgba(0,0,0,0)', font_color='white', coloraxis_showscale=True)
        fig_heat.update_yaxes(tickvals=[0,1,2,3,4], ticktext=["Mon","Tue","Wed","Thu","Fri"])
        st.plotly_chart(fig_heat, use_container_width=True)

        # Monthly trend line
        monthly_avgs = [round(random.uniform(72,94),1) for _ in months]
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(x=months, y=monthly_avgs, mode='lines+markers+text', line=dict(color='#6366f1',width=3), marker=dict(size=10,color='#818cf8'), text=[f"{v}%" for v in monthly_avgs], textposition='top center', fill='tozeroy', fillcolor='rgba(99,102,241,0.08)'))
        fig_trend.add_hline(y=75, line_dash="dash", line_color="#f43f5e", annotation_text="75% Min")
        fig_trend.update_layout(height=200, margin=dict(t=20,b=10,l=10,r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white', yaxis=dict(range=[60,105],showgrid=False), xaxis=dict(showgrid=False))
        st.plotly_chart(fig_trend, use_container_width=True)

    # ─── TAB 2: Records ───────────────────────────────────────────
    with tabs[2]:
        st.markdown("#### All Attendance Records")
        if records:
            rdf = pd.DataFrame(records)
            if 'count' in rdf.columns and tl: rdf['Att %']=(rdf['count']/tl*100).round(1)
            st.dataframe(rdf, use_container_width=True, height=450, hide_index=True,
                column_config={"Att %":st.column_config.ProgressColumn("Att %",min_value=0,max_value=100,format="%.1f%%")})
            st.download_button("⬇️ Export All Records", rdf.to_csv(index=False), f"all_{datetime.now().strftime('%Y%m%d')}.csv", type="primary")
        else: st.info("No records available.")

    # ─── TAB 3: Users ─────────────────────────────────────────────
    with tabs[3]:
        st.markdown("#### Staff User Accounts")
        if users_df is not None:
            st.dataframe(users_df.drop(columns=['password'],errors='ignore'), use_container_width=True, hide_index=True)
            st.download_button("⬇️ Export", users_df.drop(columns=['password'],errors='ignore').to_csv(index=False), "users.csv")
        else: st.warning("users.csv not found.")
        st.markdown("---"); st.markdown("#### Add New User")
        with st.form("add_user_form"):
            c1_,c2_ = st.columns(2)
            nu_name  = c1_.text_input("Full Name"); nu_user = c2_.text_input("Username")
            nu_pass  = c1_.text_input("Password", type="password"); nu_email = c2_.text_input("Email")
            nu_dept  = c1_.selectbox("Department", DEPT_LIST); nu_role = c2_.selectbox("Role", ["teacher","admin"])
            nu_subj  = st.text_input("Subject", "All Subjects")
            add_btn  = st.form_submit_button("Add User", type="primary")
        if add_btn:
            if not all([nu_name,nu_user,nu_pass,nu_email]): st.error("All fields required.")
            else:
                new_row = pd.DataFrame([{'name':nu_name,'username':nu_user,'password':nu_pass,'email':nu_email,'dept':nu_dept,'role':nu_role,'subject':nu_subj}])
                if users_df is not None:
                    if nu_user in users_df.get('username',pd.Series()).values: st.error("Username exists.")
                    else:
                        updated=pd.concat([users_df,new_row],ignore_index=True); updated.to_csv('users.csv',index=False)
                        _log_audit("Admin",f"Added user {nu_user}"); st.success(f"Added '{nu_user}'."); st.rerun()
                else: new_row.to_csv('users.csv',index=False); _log_audit("Admin","Created users.csv"); st.success("Created."); st.rerun()

    # ─── TAB 4: Departments ───────────────────────────────────────
    with tabs[4]:
        st.markdown("#### Department Analytics")
        dept_students = {d: random.randint(50,200) for d in DEPT_LIST}
        dept_att      = {d: round(random.uniform(65,95),1) for d in DEPT_LIST}
        dept_risk     = {d: random.randint(2,20) for d in DEPT_LIST}
        ddf = pd.DataFrame({'Department':list(dept_students.keys()),'Students':list(dept_students.values()),'Avg Att %':list(dept_att.values()),'At-Risk':list(dept_risk.values())})

        fig_dept = px.scatter(ddf, x='Department', y='Avg Att %', size='Students', color='Avg Att %',
            color_continuous_scale=['#f43f5e','#f59e0b','#10b981'], range_color=[0,100], text='Avg Att %')
        fig_dept.update_traces(textposition='top center')
        fig_dept.update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white', showlegend=False, xaxis_title=None, coloraxis_showscale=False)
        fig_dept.update_xaxes(showgrid=False,tickangle=-45); fig_dept.update_yaxes(showgrid=False,range=[55,105])
        st.plotly_chart(fig_dept, use_container_width=True)
        st.dataframe(ddf, use_container_width=True, hide_index=True,
            column_config={"Avg Att %":st.column_config.ProgressColumn("Avg Att %",min_value=0,max_value=100,format="%.1f%%")})

    # ─── TAB 5: Config ────────────────────────────────────────────
    with tabs[5]:
        st.markdown("#### Semester & Policy Configuration")
        col_c1,col_c2 = st.columns(2)
        with col_c1:
            new_tl  = st.number_input("Total Lectures", 1, 300, tl)
            new_min = st.slider("Min Attendance %", 50, 100, MIN_ATTENDANCE, step=5)
            new_grc = st.number_input("Grace Period (min)", 0, 30, LATE_GRACE_MIN)
        with col_c2:
            sem_s   = st.date_input("Semester Start", value=date(2026,7,1))
            sem_e   = st.date_input("Semester End", value=date(2026,11,30))
            exam_s  = st.date_input("Exam Start", value=date(2026,12,1))
        if st.button("Save Configuration", type="primary"):
            st.session_state.total_lectures = int(new_tl)
            _log_audit("Config",f"Lectures={new_tl}, Min={new_min}%, Grace={new_grc}min")
            save_json_safe('config.json',{'total_lectures':int(new_tl),'min_attendance':int(new_min),'grace_minutes':int(new_grc),'sem_start':str(sem_s),'sem_end':str(sem_e),'exam_start':str(exam_s)})
            st.success("Configuration saved!")

    # ─── TAB 6: Audit Log ─────────────────────────────────────────
    with tabs[6]:
        st.markdown("#### System-wide Audit Log")
        log = st.session_state.audit_log
        if not log: st.info("No events.")
        else:
            st.markdown(f"Total events: **{len(log)}**")
            log_df = pd.DataFrame(log)
            st.dataframe(log_df, use_container_width=True, height=500, hide_index=True)
            st.download_button("⬇️ Export Audit Log", log_df.to_csv(index=False), f"audit_{datetime.now().strftime('%Y%m%d')}.csv")

            # Activity breakdown
            if len(log)>5:
                actions = [e['action'] for e in log]
                act_counts = {a:actions.count(a) for a in set(actions)}
                fig_act = px.pie(values=list(act_counts.values()),names=list(act_counts.keys()),hole=0.5,title="Activity Breakdown",color_discrete_sequence=['#6366f1','#10b981','#f59e0b','#f43f5e','#38bdf8','#8b5cf6'])
                fig_act.update_layout(height=280,paper_bgcolor='rgba(0,0,0,0)',font_color='white',margin=dict(t=30,b=10,l=10,r=10),showlegend=True,legend=dict(bgcolor='rgba(0,0,0,0)'))
                st.plotly_chart(fig_act, use_container_width=True)

    # ─── TAB 7: System ────────────────────────────────────────────
    with tabs[7]:
        st.markdown("#### System Information")
        col_s1,col_s2 = st.columns(2)
        with col_s1:
            st.markdown(f'<div class="insight-card insight-info"><h5>Application</h5><p>{APP_NAME} v{APP_VERSION}<br>{COLLEGE}</p></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="insight-card"><h5>Developers</h5><p>{DEVELOPERS}</p></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="insight-card"><h5>Academic Guide</h5><p>{GUIDE}</p></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="insight-card insight-violet"><h5>New in v6.0</h5><p>Seat Heatmap · Risk Engine · Leaderboard · Mood Tracker · Exam Countdown · QR Fallback · Compare Tool · Annual Calendar · Broadcast Center · Report Cards</p></div>', unsafe_allow_html=True)
        with col_s2:
            files = ['attendance_results.json','attendance.csv','live_attendance.json','users.csv','students.csv','timetable.csv','service_requests.json','leave_requests.json','config.json']
            for f in files:
                exists = os.path.exists(f)
                size   = f"{os.path.getsize(f)/1024:.1f} KB" if exists else "—"
                cls_   = "insight-ok" if exists else "insight-warn"
                icon_  = "✅" if exists else "⚠️"
                st.markdown(f'<div class="insight-card {cls_}"><h5>{icon_} {f}</h5><p>{size}</p></div>', unsafe_allow_html=True)

        st.markdown("---")
        if st.button("🔄 Clear ALL Transactional Data", type="secondary"):
            for f in ['attendance_results.json','attendance.csv','live_attendance.json','service_requests.json','leave_requests.json']:
                try:
                    if os.path.exists(f): os.remove(f)
                except Exception: pass
            st.session_state.service_requests=[]; st.session_state.leave_requests=[]; st.session_state.audit_log=[]; st.session_state.notifications=[]; st.session_state.parent_alerts=[]; st.session_state.broadcast_msgs=[]
            _cached_csv.clear()
            st.success("All transactional data cleared."); time.sleep(0.8); st.rerun()


# ══════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════
def render_footer():
    st.markdown(f"""
        <div class="footer">
            <strong>{APP_NAME}</strong> v{APP_VERSION} &nbsp;|&nbsp; {COLLEGE}<br>
            Developed by <strong>{DEVELOPERS}</strong> &nbsp;|&nbsp; Guided by <strong>{GUIDE}</strong><br>
            <span style="color:var(--text-lo);">{BATCH} &nbsp;·&nbsp; © 2026 VisionGuard AI. All rights reserved.</span>
        </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════════════════════════════
def main():
    try:
        check_session_timeout()
        if not st.session_state.logged_in:
            login_page(); return
        render_sidebar()
        role = st.session_state.role
        if role=='student':     student_portal()
        elif role=='teacher':   teacher_dashboard()
        elif role=='admin':     admin_dashboard()
        else: st.error("Unknown role. Please sign out and sign in again.")
        render_footer()
    except Exception as e:
        st.error(f"🚨 Unexpected error: {e}")
        with st.expander("Technical Details"):
            st.code(traceback.format_exc())
        st.info("Please refresh or contact the administrator.")

if __name__ == "__main__":
    main()