import streamlit as st
import cv2
import os
import pandas as pd
from datetime import datetime
import time

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="VisionGuard AI - Student Registration",
    page_icon="📸",
    layout="centered"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem; border-radius: 15px; margin-bottom: 1.5rem;
        text-align: center; color: white;
    }
    .step-box {
        background: #f8f9fa; padding: 1.5rem; border-radius: 10px;
        border-left: 5px solid #667eea; margin: 1rem 0;
    }
    .success-box {
        background: #d4edda; padding: 1.5rem; border-radius: 10px;
        border-left: 5px solid #28a745; margin: 1rem 0;
    }
    .stButton > button {
        font-weight: 600; border-radius: 10px; padding: 0.8rem 2rem;
        font-size: 1.1rem;
    }
    .big-number {
        font-size: 4rem; font-weight: 700; color: #667eea;
    }
</style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE ====================
if 'step' not in st.session_state: st.session_state.step = 1
if 'photos_taken' not in st.session_state: st.session_state.photos_taken = 0
if 'student_name' not in st.session_state: st.session_state.student_name = None
if 'student_prn' not in st.session_state: st.session_state.student_prn = None
if 'photos' not in st.session_state: st.session_state.photos = []
if 'registration_complete' not in st.session_state: st.session_state.registration_complete = False

# ==================== FUNCTIONS ====================
def load_students():
    try:
        if os.path.exists('students.csv'):
            return pd.read_csv('students.csv')
    except: pass
    return None

def get_camera():
    cap = cv2.VideoCapture(0)
    return cap if cap.isOpened() else None

def take_photo(cap):
    ret, frame = cap.read()
    if ret:
        return cv2.flip(frame, 1)
    return None

def save_student_photos(name, photos_list):
    folder_path = os.path.join('dataset', name)
    os.makedirs(folder_path, exist_ok=True)
    for i, photo in enumerate(photos_list):
        filepath = os.path.join(folder_path, f"selfie_{i+1}.jpg")
        cv2.imwrite(filepath, photo)
    return folder_path

def go_to_step(step_num):
    st.session_state.step = step_num
    st.rerun()

# ==================== HEADER ====================
st.markdown("""
    <div class="main-header">
        <h1>📸 VisionGuard AI</h1>
        <p style="font-size:1.2rem;">Self-Registration Portal</p>
        <p style="opacity:0.8;">Register your face in 1 minute - No admin needed!</p>
    </div>
""", unsafe_allow_html=True)

# ==================== STEP 1: SELECT STUDENT ====================
if st.session_state.step == 1:
    st.markdown("### 👤 Step 1: Who are you?")
    st.markdown('<div class="step-box">', unsafe_allow_html=True)
    
    students_df = load_students()
    
    if students_df is None:
        st.error("❌ students.csv not found!")
    else:
        search = st.text_input("🔍 Search your name or PRN", placeholder="Type your name or PRN number...")
        
        if search:
            filtered = students_df[
                students_df['Name'].str.lower().str.contains(search.lower()) |
                students_df['Student ID'].astype(str).str.contains(search)
            ]
            
            if not filtered.empty:
                st.write(f"**Found {len(filtered)} matches:**")
                
                for _, row in filtered.iterrows():
                    col1, col2, col3 = st.columns([3, 2, 1])
                    with col1:
                        st.write(f"**{row['Name']}**")
                    with col2:
                        st.write(f"PRN: {row['Student ID']}")
                    with col3:
                        if st.button("Select ✅", key=f"select_{row['Student ID']}"):
                            st.session_state.student_name = row['Name']
                            st.session_state.student_prn = row['Student ID']
                            folder_path = os.path.join('dataset', row['Name'])
                            if os.path.exists(folder_path):
                                existing = len([f for f in os.listdir(folder_path) if f.endswith(('.jpg','.png','.jpeg'))])
                                st.session_state.existing_photos = existing
                            else:
                                st.session_state.existing_photos = 0
                            go_to_step(2)
            else:
                st.warning("No students found. Try different search.")
        else:
            st.info("👆 Type your name or PRN to find yourself")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== STEP 2: TAKE PHOTOS ====================
elif st.session_state.step == 2:
    st.markdown(f"### 📸 Step 2: Take Photos for {st.session_state.student_name}")
    
    if st.session_state.existing_photos > 0:
        st.info(f"📁 You already have {st.session_state.existing_photos} photos. Adding more improves recognition.")
    
    st.markdown('<div class="step-box">', unsafe_allow_html=True)
    
    st.markdown("""
    ### 📋 Photo Instructions:
    1. **Photo 1:** Look straight at camera (Front face)
    2. **Photo 2:** Turn head slightly LEFT
    3. **Photo 3:** Turn head slightly RIGHT  
    4. **Photo 4:** Smile or different expression
    5. **Photo 5:** Move a bit closer/further
    
    **Tip:** Good lighting + clear face = Better recognition!
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        FRAME_WINDOW = st.image([])
        
        cap = get_camera()
        if cap is None:
            st.error("❌ No camera detected! Allow camera access.")
        else:
            ret, frame = cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                photo_num = st.session_state.photos_taken + 1
                guides = ["Look STRAIGHT ahead 👤", "Turn head LEFT 👈", "Turn head RIGHT 👉", 
                         "SMILE or change expression 😊", "Move CLOSER or FURTHER 📏"]
                
                if photo_num <= 5:
                    guide_text = guides[photo_num - 1]
                else:
                    guide_text = "✅ Done! Click Save"
                
                cv2.putText(frame, f"Photo {photo_num}/5: {guide_text}", (20, 40), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(frame, f"Photos taken: {st.session_state.photos_taken}", (20, 80), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                
                FRAME_WINDOW.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            
            with col2:
                st.markdown(f"""
                <div style="text-align:center;">
                    <div class="big-number">{st.session_state.photos_taken}</div>
                    <p>Photos Taken</p>
                    <p style="color:#666;">of 5 required</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.session_state.photos_taken < 5:
                    if st.button("📸 CAPTURE PHOTO", use_container_width=True, type="primary"):
                        photo = take_photo(cap)
                        if photo is not None:
                            st.session_state.photos.append(photo)
                            st.session_state.photos_taken += 1
                            st.rerun()
                        else:
                            st.error("Failed to capture!")
                
                if st.session_state.photos_taken >= 5:
                    if st.button("💾 SAVE & FINISH", use_container_width=True, type="primary"):
                        save_student_photos(st.session_state.student_name, st.session_state.photos)
                        st.session_state.registration_complete = True
                        go_to_step(3)
                
                if st.button("🔄 Reset Photos", use_container_width=True):
                    st.session_state.photos = []
                    st.session_state.photos_taken = 0
                    st.rerun()
            
            cap.release()
    
    if st.session_state.photos:
        st.markdown("---")
        st.markdown("### 📷 Captured Photos:")
        cols = st.columns(min(5, len(st.session_state.photos)))
        for i, photo in enumerate(st.session_state.photos):
            with cols[i]:
                st.image(cv2.cvtColor(photo, cv2.COLOR_BGR2RGB), caption=f"Photo {i+1}")

# ==================== STEP 3: COMPLETE ====================
elif st.session_state.step == 3:
    st.markdown(f"""
        <div class="success-box">
            <h2>🎉 Registration Complete!</h2>
            <p><strong>Student:</strong> {st.session_state.student_name}</p>
            <p><strong>PRN:</strong> {st.session_state.student_prn}</p>
            <p><strong>Photos Saved:</strong> {st.session_state.photos_taken}</p>
            <p><strong>Location:</strong> dataset/{st.session_state.student_name}/</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.success("✅ You're now registered! The attendance system will recognize you.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📸 Register Another Student", use_container_width=True):
            st.session_state.step = 1
            st.session_state.photos_taken = 0
            st.session_state.photos = []
            st.session_state.registration_complete = False
            st.rerun()
    with col2:
        if st.button("🏠 Go to Login", use_container_width=True):
            st.markdown("Open dashboard: `streamlit run smart_attendance/database.py`")

st.markdown("---")
st.caption("VisionGuard AI | Self-Registration Portal | Students can register from any device")

