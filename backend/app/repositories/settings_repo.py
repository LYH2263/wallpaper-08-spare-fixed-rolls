from app.db import connect


def get_all() -> dict:
    conn = connect()
    try:
        return {r["key"]: r["value"] for r in conn.execute("SELECT key,value FROM settings").fetchall()}
    finally:
        conn.close()


def set_value(key: str, value: str) -> None:
    conn = connect()
    try:
        conn.execute("INSERT OR REPLACE INTO settings(key,value) VALUES (?,?)", (key, value))
        conn.commit()
    finally:
        conn.close()
