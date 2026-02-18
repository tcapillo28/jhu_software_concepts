# src/state.py

scrape_running = {"value": False}

def is_busy():
    return scrape_running["value"]

def set_busy(value: bool):
    scrape_running["value"] = value