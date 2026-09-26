from app.db import connect

SPARE_DEFAULT_N_KEY = "spare_default_n"
DEFAULT_SPARE_N = 0


def get_all() -> dict:
    conn = connect()
    try:
        return {r["key"]: r["value"] for r in conn.execute("SELECT key,value FROM settings").fetchall()}
    finally:
        conn.close()


def get_int(key: str, default: int = 0) -> int:
    conn = connect()
    try:
        row = conn.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
        if row is None or row["value"] is None or row["value"] == "":
            return default
        return int(row["value"])
    finally:
        conn.close()


def get_spare_default_n() -> int:
    return get_int(SPARE_DEFAULT_N_KEY, DEFAULT_SPARE_N)


def upsert(key: str, value: str) -> None:
    conn = connect()
    try:
        conn.execute(
            "INSERT INTO settings(key,value) VALUES (?,?) "
            "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            (key, value),
        )
        conn.commit()
    finally:
        conn.close()


def set_spare_default_n(n: int) -> int:
    upsert(SPARE_DEFAULT_N_KEY, str(int(n)))
    return get_spare_default_n()
