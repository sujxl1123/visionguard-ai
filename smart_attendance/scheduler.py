import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from config import GRACE_CUTOFF, MIN_DETECTIONS


def finalize_attendance(session_id, conn, stop_event):
    stop_event.set()
    cutoff_dt = datetime.datetime.combine(datetime.date.today(), GRACE_CUTOFF)

    conn.execute(
        """
        UPDATE detections
        SET status = 'PRESENT'
        WHERE session_id = ?
          AND det_count >= ?
          AND first_seen <= ?
        """,
        (session_id, MIN_DETECTIONS, cutoff_dt)
    )

    conn.execute(
        """
        UPDATE detections
        SET status = 'LATE'
        WHERE session_id = ?
          AND status = 'PENDING'
        """,
        (session_id,)
    )

    conn.execute(
        "UPDATE sessions SET finalized = 1 WHERE session_id = ?",
        (session_id,)
    )

    conn.commit()
    print(f"[FINALIZED] Session {session_id} locked.")


def schedule_finalization(session_id, conn, stop_event):
    scheduler = BackgroundScheduler()
    cutoff_today = datetime.datetime.combine(datetime.date.today(), GRACE_CUTOFF)

    scheduler.add_job(
        finalize_attendance,
        trigger="date",
        run_date=cutoff_today,
        args=[session_id, conn, stop_event],
        id=f"finalize_{session_id}",
        replace_existing=True,
    )

    scheduler.start()
    print(f"[SCHEDULER] Finalization set for {cutoff_today}")
    return scheduler