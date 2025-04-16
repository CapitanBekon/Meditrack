def merge_sort(appointments):
    if len(appointments) > 1:
        mid = len(appointments) // 2  # Finding the mid of the array
        left_half = appointments[:mid]  # Dividing the elements into 2 halves
        right_half = appointments[mid:]

        merge_sort(left_half)  # Sorting the first half
        merge_sort(right_half)  # Sorting the second half

        i = j = k = 0

        # Copy data to temp arrays L[] and R[]
        while i < len(left_half) and j < len(right_half):
            if left_half[i]['time'] < right_half[j]['time']:  # Assuming appointments have a 'time' key
                appointments[k] = left_half[i]
                i += 1
            else:
                appointments[k] = right_half[j]
                j += 1
            k += 1

        # Checking if any element was left
        while i < len(left_half):
            appointments[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            appointments[k] = right_half[j]
            j += 1
            k += 1

    return appointments