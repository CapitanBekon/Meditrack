def quick_sort(records, key=lambda x: x['dob']):
    if len(records) <= 1:
        return records
    pivot = records[len(records) // 2]
    left = [x for x in records if key(x) < key(pivot)]
    middle = [x for x in records if key(x) == key(pivot)]
    right = [x for x in records if key(x) > key(pivot)]
    return quick_sort(left, key) + middle + quick_sort(right, key)