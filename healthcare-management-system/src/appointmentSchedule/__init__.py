def merge_sort(appointments):
    if len(appointments) > 1:
        mid = len(appointments) // 2
        left_half = appointments[:mid]
        right_half = appointments[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0

        while i < len(left_half) and j < len(right_half):
            if left_half[i]['time'] < right_half[j]['time']:
                appointments[k] = left_half[i]
                i += 1
            else:
                appointments[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            appointments[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            appointments[k] = right_half[j]
            j += 1
            k += 1

__all__ = ['merge_sort']