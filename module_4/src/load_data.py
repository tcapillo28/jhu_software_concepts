_storage = []

def insert_rows(rows):
    global _storage
    for row in rows:
        if row not in _storage:
            _storage.append(row)

def get_all_rows():
    return list(_storage)

def clear_storage():
    global _storage
    _storage = []