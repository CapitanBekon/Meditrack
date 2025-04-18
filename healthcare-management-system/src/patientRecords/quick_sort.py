def quick_sort(records, key=lambda x: x['dob']):
    """
    Perform Quick Sort on a list of records.
    
    :param records: List of records to be sorted.
    :param key: A function that extracts the value to sort by (default is 'dob').
    :return: A sorted list of records.
    """
    # Base case: If the list has 0 or 1 elements, it is already sorted
    if len(records) <= 1:
        return records

    # Choose the middle element as the pivot
    pivot = records[len(records) // 2]

    # Partition the list into three parts:
    # 1. Elements less than the pivot
    left = [x for x in records if key(x) < key(pivot)]

    # 2. Elements equal to the pivot
    middle = [x for x in records if key(x) == key(pivot)]

    # 3. Elements greater than the pivot
    right = [x for x in records if key(x) > key(pivot)]

    # Recursively sort the left and right partitions, and combine them with the middle
    return quick_sort(left, key) + middle + quick_sort(right, key)

# Example list of records
records = [
    {"name": "Alice", "dob": "1990-01-01"},
    {"name": "Bob", "dob": "1985-05-15"},
    {"name": "Charlie", "dob": "1992-07-20"}
]

# Sort records by 'dob'
sorted_records = quick_sort(records, key=lambda x: x['dob'])

# Output the sorted records
print(sorted_records)