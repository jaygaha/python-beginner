# Shell Sort Algorithm
# Shell Sort is an optimization over insertion sort. It starts by sorting pairs of elements far apart from each other,
# then progressively reducing the gap between elements to be compared.

def shell_sort(arr):
    indexing_length = len(arr)
    gap = indexing_length // 2

    while gap > 0:
        for i in range(gap, indexing_length):
            temp = arr[i]
            j = i

            # Sort the sub list for this gap
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap

            arr[j] = temp

        # Reduce the gap for the next element
        gap //= 2

    return arr

# Output
unsorted_list = [7, 6, 8, 9, 3,2, 10, 5, 1, 4]
print(shell_sort(unsorted_list)) # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]