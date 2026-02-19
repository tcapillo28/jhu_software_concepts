_busy = False

def is_busy():
    return _busy

def set_busy(value: bool):
    global _busy
    _busy = value