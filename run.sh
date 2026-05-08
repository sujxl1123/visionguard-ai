#!/bin/bash
cd "/Users/sujalkamthe/Desktop/human counting"
source .venv/bin/activate
echo ""
echo "╔════════════════════════════════════════════╗"
echo "║       VISIONGUARD AI PRO LAUNCHER          ║"
echo "╚════════════════════════════════════════════╝"
echo ""
echo "1. Attendance Dashboard"
echo "2. Crowd Counter"
echo "3. Student Registration"
echo ""
read -p "Enter choice (1-3): " choice

case $choice in
    1) streamlit run smart_attendance/database.py ;;
    2) streamlit run crowd_dashboard.py --server.port 8507 ;;
    3) streamlit run student_register.py --server.port 8508 ;;
    *) echo "Invalid choice" ;;
esac
