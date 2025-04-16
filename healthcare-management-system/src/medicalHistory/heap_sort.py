def heapify(array, n, i):
    largest = i  # Initialize largest as root
    left = 2 * i + 1  # left = 2*i + 1
    right = 2 * i + 2  # right = 2*i + 2

    # If left child is larger than root
    if left < n and array[left]['date'] > array[largest]['date']:
        largest = left

    # If right child is larger than largest so far
    if right < n and array[right]['date'] > array[largest]['date']:
        largest = right

    # If largest is not root
    if largest != i:
        array[i], array[largest] = array[largest], array[i]  # Swap

        # Recursively heapify the affected sub-tree
        heapify(array, n, largest)

def heap_sort(medical_history):
    n = len(medical_history)

    # Build a max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(medical_history, n, i)

    # One by one extract elements from heap
    for i in range(n - 1, 0, -1):
        medical_history[i], medical_history[0] = medical_history[0], medical_history[i]  # Swap
        heapify(medical_history, i, 0)  # Heapify the root element

    return medical_history