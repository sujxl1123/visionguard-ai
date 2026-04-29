import sqlite3, pandas as pd, os
from datetime import datetime
DB = 'visionguard.db'
def ms():
    if not os.path.exists('students.csv'): return
    conn = sqlite3.connect(DB)
    df = pd.read_csv('students.csv')
    for _,r in df.iterrows():
        p,n = str(r['Student ID']), str(r['Name'])
        e = n.lower().replace(' ','.') + '@mitwpu.edu.in'
        conn.execute('INSERT OR REPLACE INTO students VALUES (?,?,?,?,?,?,?)', (p,n,e,'CSE','DSBDA',datetime.now().strftime('%Y-%m-%d'),0))
    conn.commit(); conn.close()
    print('Students done')
def mu():
    if not os.path.exists('users.csv'): return
    conn = sqlite3.connect(DB)
    df = pd.read_csv('users.csv')
    for _,r in df.iterrows():
        conn.execute('INSERT OR REPLACE INTO users VALUES (?,?,?,?,?,?,?,?)', (str(r['username']),str(r['password']),str(r['role']),str(r['name']),str(r.get('email','')),str(r.get('department','')),str(r.get('class_assigned','')),str(r.get('student_id',''))))
    conn.commit(); conn.close()
    print('Users done')
def mt():
    if not os.path.exists('timetable.csv'): return
    conn = sqlite3.connect(DB)
    df = pd.read_csv('timetable.csv')
    for _,r in df.iterrows():
        conn.execute('INSERT INTO timetable VALUES (?,?,?,?,?,?,?)', (None,str(r['Day']),str(r['Start Time']),str(r['End Time']),str(r['Subject']),str(r['Faculty']),str(r['Class'])))
    conn.commit(); conn.close()
    print('Timetable done')
import database_setup
database_setup.create_database()
ms(); mu(); mt()
conn = sqlite3.connect(DB)
for t in ['students','users','timetable']:
    c = conn.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0]
    print(f'{t}: {c}')
conn.close()
print('Done!')
