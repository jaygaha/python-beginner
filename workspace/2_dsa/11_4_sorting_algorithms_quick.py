# Quick sort algorithm
# Quick Sort is a divide and conquer algorithm that was invented by Tony Hoare in 1960.
# It is a comparison-based sorting algorithm that uses a divide and conquer strategy to divide a list into two sublists.
# Time: O(n log n) Space: O(log n)

def quick_sort(unsorted):
    length = len(unsorted)
    if length <= 1:
        return unsorted
    else:
        pivot = unsorted.pop()

    items_greater = []
    items_lower = []

    for item in unsorted:
        if item > pivot:
            items_greater.append(item) # append to the items_greater list
        else:
            items_lower.append(item) # append to the items_lower list

    # Recursion
    return quick_sort(items_lower) + [pivot] + quick_sort(items_greater)



# Output

unsorted_list = [64, 34, 25, 12, 22, 11, 90, 22, 11, 90]
print(quick_sort(unsorted_list)) # [11, 11, 12, 22, 22, 25, 34, 64, 90, 90]