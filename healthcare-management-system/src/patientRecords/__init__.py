def quick_sort(patient_records):
    if len(patient_records) <= 1:
        return patient_records
    pivot = patient_records[len(patient_records) // 2]
    left = [x for x in patient_records if x < pivot]
    middle = [x for x in patient_records if x == pivot]
    right = [x for x in patient_records if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)