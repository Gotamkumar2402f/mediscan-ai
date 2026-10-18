"""SQLite chat memory."""
import json
import sqlite3
from src.config import MEMORY_DB

def _conn():
    MEMORY_DB.parent.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(MEMORY_DB)
    c.execute("""CREATE TABLE IF NOT EXISTS chats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)""")
    c.execute("CREATE INDEX IF NOT EXISTS idx_session ON chats(session_id)")
    return c

def save_turn(session_id: str, role: str, content):
    with _conn() as c:
        c.execute("INSERT INTO chats (session_id, role, content) VALUES (?,?,?)",
                  (session_id, role, json.dumps(content, ensure_ascii=False)))

def load_history(session_id: str, limit: int = 10):
    with _conn() as c:
        rows = c.execute(
            "SELECT role, content FROM chats WHERE session_id=? ORDER BY id DESC LIMIT ?",
            (session_id, limit)).fetchall()
    return [{"role": r, "content": json.loads(t)} for r, t in reversed(rows)]

def clear_history(session_id: str):
    with _conn() as c:
        c.execute("DELETE FROM chats WHERE session_id=?", (session_id,))