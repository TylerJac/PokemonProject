def check_clauses(*args):
    for clause in args:
        if clause:
            return " AND "
    return ""