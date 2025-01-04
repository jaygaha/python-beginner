# Insertion Sort Algorithm
# Sorting Algorithms: arrange elements in a list in a specific order

def insertion_sort(arr):
    index_length = range(1, len(arr)) # Start with 1 as we assume that the first element is sorted

    for i in index_length:
        value_to_sort = arr[i]

        while arr[i-1] > value_to_sort and i > 0:
            arr[i], arr[i-1] = arr[i-1], arr[i]
            i -= 1

    return arr

# Output
print(insertion_sort([7,8,9,8,7,6,5,6,7,8,9,8,7,6,5,6,7,8])) # [5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 8, 9, 9, 9]