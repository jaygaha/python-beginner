# Selection Sort
# Selection Sort is a simple sorting algorithm that works by selecting the smallest (or largest) element from
# the unsorted portion of the list and swapping it with the first unsorted element.
# Slow algorithm, not recommended for large datasets.
# Time: O(n^2) Space: O(1)

def selection_sort(arr):
    for i in range(len(arr)):
        minimum = i

        for j in range(i+1, len(arr)):
            if arr[j] < arr[minimum]:
                minimum = j

        # swap the minimum element with the first element
        arr[minimum], arr[i] = arr[i], arr[minimum]

    return arr

# Output

unsorted_list = [19, 2, 31, 45, 30, 11, 121, 27]
print(selection_sort(unsorted_list)) # [2, 11, 19, 27, 30, 31, 45, 121]