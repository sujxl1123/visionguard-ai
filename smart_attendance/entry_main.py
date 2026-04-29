import threading

from config import DB_PATH, SUBJECT_NAME
from database import get_connection, init_db, create_session
from entry_tracker import run_entry_capture
from scheduler import schedule_finalization


def main():
    print("[SYSTEM] Starting smart attendance...")

    conn = get_connection(DB_PATH)
    init_db(conn)
    print("[DB] Initialized")

    stop_event = threading.Event()

    session_id = create_session(conn, SUBJECT_NAME)
    print(f"[SESSION] Created session_id = {session_id}")

    scheduler = schedule_finalization(session_id, conn, stop_event)

    try:
        run_entry_capture(session_id, conn, stop_event)
    finally:
        scheduler.shutdown()
        conn.close()
        print("[SYSTEM] Closed cleanly.")


if __name__ == "__main__":
    main()