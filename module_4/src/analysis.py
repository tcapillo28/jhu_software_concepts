from .load_data import get_all_rows

def compute_analysis():
    rows = get_all_rows()
    total = len(rows)

    return {
        "total_rows": total,
        "accept_rate": f"{(sum(1 for r in rows if r.get('decision') == 'Accepted') / total * 100):.2f}%" if total else "0.00%",
        "Answer": "Some analysis result"
    }