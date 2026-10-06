import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path("data") / "rewear.db"
DB_PATH.parent.mkdir(exist_ok=True)

def connect():
    return sqlite3.connect(DB_PATH)

def init_db():
    with connect() as con:
        con.execute("""
        CREATE TABLE IF NOT EXISTS wardrobe (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_path TEXT NOT NULL,
            category TEXT NOT NULL,
            color TEXT,
            occasion TEXT,
            season TEXT,
            style TEXT,
            notes TEXT,
            wear_count INTEGER DEFAULT 0,
            created_at TEXT
        )
        """)
        con.commit()

def add_item(image_path, category, color, occasion, season, style, notes):
    with connect() as con:
        con.execute("""
        INSERT INTO wardrobe
        (image_path, category, color, occasion, season, style, notes, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (image_path, category, color, occasion, season, style, notes, datetime.now().isoformat()))
        con.commit()

def get_items():
    with connect() as con:
        con.row_factory = sqlite3.Row
        return [dict(row) for row in con.execute("SELECT * FROM wardrobe ORDER BY id DESC").fetchall()]

def mark_worn(item_id):
    with connect() as con:
        con.execute("UPDATE wardrobe SET wear_count = wear_count + 1 WHERE id=?", (item_id,))
        con.commit()

def delete_item(item_id):
    with connect() as con:
        con.execute("DELETE FROM wardrobe WHERE id=?", (item_id,))
        con.commit()
