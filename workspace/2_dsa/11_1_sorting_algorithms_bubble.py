# Sorting Algorithms: arrange elements in a list in a specific order

# 1. Bubble Sort
# Bubble Sort is a simple sorting algorithm that repeatedly steps through the list,
# compares adjacent elements and swaps them if they are in the wrong order. The pass through the list is repeated until the list is sorted.
# The algorithm, which is a comparison sort, is named for the way smaller elements "bubble" to the top of the list.

# Time Complexity: O(n^2)
# Space Complexity: O(1)

def bubble_sort(arr):
    indexing_length = len(arr) - 1 # Scan not apply comparision starting with last item of list (No item to right)
    is_sorted = False

    while not is_sorted:
        is_sorted = True
        for i in range(0, indexing_length):
            if arr[i] > arr[i+1]: # if current element is greater than the next element
                is_sorted = False
                arr[i], arr[i+1] = arr[i+1], arr[i] # swap

    return arr


# Output
print(bubble_sort([3, 5, 8, 1, 2, 9, 4])) # [1, 2, 3, 4, 5, 8, 9]
print(bubble_sort([4, 6, 8, 3, 2, 5, 7, 8, 9])) # [2, 3, 4, 5, 6, 7, 8, 8, 9]