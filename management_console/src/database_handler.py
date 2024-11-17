import sqlite3
from datetime import datetime
from .models import LogEntry

DB_PATH = 'management_console/data/logs.db'

def initialize_database():
    """Initialize the database and create the logs table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            uid INTEGER PRIMARY KEY AUTOINCREMENT,
            datetime TEXT DEFAULT CURRENT_TIMESTAMP,
            source TEXT NOT NULL,
            log TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_log(entry: LogEntry) -> LogEntry:
    """Insert a new log entry into the database and return the full entry with the generated uid."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO logs (datetime, source, log) VALUES (?, ?, ?)",
        (entry.timestamp.isoformat(), entry.source, entry.log)  # Convert timestamp to ISO 8601 string
    )
    # Get the UID of the last inserted row
    entry_id = cursor.lastrowid
    conn.commit()
    conn.close()

    # Return the LogEntry object with the generated uid
    return LogEntry(uid=entry_id, source=entry.source, log=entry.log, timestamp=entry.timestamp)



def delete_log(log_id: int) -> bool:
    """Delete a log entry by ID. Returns True if deleted, False if not found."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM logs WHERE uid = ?", (log_id,))
    conn.commit()
    changes = conn.total_changes
    conn.close()
    return changes > 0

def clear_all_logs() -> int:
    """Delete all log entries from the database and return the number of logs deleted."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM logs")
    deleted_count = cursor.rowcount  # Get the number of deleted rows
    conn.commit()
    conn.close()
    return deleted_count

def update_log(log_id: int, updated_entry: LogEntry) -> bool:
    """Update a log entry by ID. Returns True if updated, False if not found."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE logs SET datetime = ?, source = ?, log = ? WHERE uid = ?",
        (updated_entry.timestamp.isoformat(), updated_entry.source, updated_entry.log, log_id)
    )
    conn.commit()
    changes = conn.total_changes
    conn.close()
    return changes > 0


def get_log(log_id: int) -> LogEntry | None:
    """Retrieve a log entry by ID. Returns the log or None if not found."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT uid, datetime, source, log FROM logs WHERE uid = ?", (log_id,)
    )
    row = cursor.fetchone()
    conn.close()
    if row:
        return LogEntry(uid=row[0], timestamp=row[1], source=row[2], log=row[3])  # Map fields correctly
    return None

def get_all_logs() -> list[LogEntry]:
    """Retrieve all log entries from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT uid, datetime, source, log FROM logs ORDER BY datetime DESC")
    rows = cursor.fetchall()
    conn.close()

    return [
        LogEntry(
            uid=row[0],
            timestamp=row[1],
            source=row[2],
            log=row[3]
        ) for row in rows
    ]
