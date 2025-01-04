# Merge Sort Algorithm:
# Merge Sort is a divide and conquer algorithm that was invented by John von Neumann in 1945.
# It is a comparison-based sorting algorithm that uses a divide and conquer strategy to divide a list into two sublists.
# It then sorts the sublists and merges them to produce a sorted list.

def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    # Split Array in into right and left
    middle = len(arr) // 2
    left = arr[:middle]
    right = arr[middle:]

    left = merge_sort(left)
    right = merge_sort(right)

    return list(merge(left, right))

# Merge the sorted halves
def merge(left, right):
    result = []
    left_pointer = right_pointer = 0

    while left_pointer < len(left) and right_pointer < len(right):
        if left[left_pointer] < right[right_pointer]:
            result.append(left[left_pointer])
            left_pointer += 1
        else:
            result.append(right[right_pointer])
            right_pointer += 1

    result.extend(left[left_pointer:])
    result.extend(right[right_pointer:])
    return result

unsorted_list = [64, 34, 25, 12, 22, 11, 90]
print(merge_sort(unsorted_list)) # [11, 12, 22, 25, 34, 64, 90]