conditions = [not is_A, not is_B, not is_C]
for c in conditions:
    if not c:
        return False
return True