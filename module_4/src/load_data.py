# src/load_data.py

# In-memory fake database for Module 4
_db = []


def load_rows():
    """
    Placeholder. Tests patch this to return fake scraped rows.
    """
    return []


def insert_rows(rows):
    """
    Insert rows into the in-memory DB, skipping duplicates by id.
    """
    existing_ids = {row["id"] for row in _db}
    for row in rows:
        if row["id"] not in existing_ids:
            _db.append(row)
            existing_ids.add(row["id"])


def get_all_rows():
    """
    Return all stored rows.
    """
    return list(_db)


class DBSession:
    def count_rows(self):
        return len(_db)


# Tests expect this name to exist
db_session = DBSession()