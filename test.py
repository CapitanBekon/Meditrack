def quickSort(array):
    if len(array) <= 1:  #End array early for optimal performance
        return array
    pivot = array[len(array) // 2] #Establish pivot as the middle element of the array
    #swaps around the pivot to sort the array
    left = [x for x in array if x < pivot] 
    middle = [x for x in array if x == pivot]
    right = [x for x in array if x > pivot]
    # This is a recursive call to sort the left and right sub-arrays
    return quickSort(left) + middle + quickSort(right)