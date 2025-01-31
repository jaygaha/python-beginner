# To solve the puzzle with recursion, the first thing to do is break the original problem down into smaller sub-problems.
# The final configuration with n disks piled up to the third rod in decreasing order can be obtained by moving:
#     n - 1 disks from the source to the auxiliary rod
#     the largest disk from the source to the target
#     and then the n - 1 disks from the auxiliary rod to the target.
# So, the first thing the move function should do is calling itself with n - 1 as the first argument. But if you try to do so without defining a base case, you will get a RecursionError.
#   This happens because the function keeps calling itself indefinitely.
# Before your comment and your print() call, add the recursive function call with n - 1 as the first argument and make sure the function body executes only when n is greater than zero.
#   For now, leave the other arguments in the same order.

NUMBER_OF_DISKS = 5
A = list(range(NUMBER_OF_DISKS, 0, -1))
B = []
C = []

def move(n, source, auxiliary, target):
    if n <= 0:
        return

    # move n - 1 disks from source to auxiliary, so they are out of the way
    move(n - 1, source, target, auxiliary)

    # move the nth disk from source to target
    target.append(source.pop())

    # display our progress
    print(A, B, C, '\n')

    # move the n - 1 disks that we left on auxiliary onto target
    move(n - 1,  auxiliary, source, target)

# initiate call from source A to target C with auxiliary B
move(NUMBER_OF_DISKS, A, B, C)
