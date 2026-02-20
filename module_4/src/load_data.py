_db = []

def insert_rows(rows):
    """Insert rows into the in-memory DB."""
    global _db
    _db.extend(rows)

def get_all_rows():
    """Return all stored rows."""
    return list(_db)