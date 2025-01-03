# Stacks: Operations are performed LIFO (last in, first out), which means that the last element added will be the first one removed.
# A stack can be implemented using an array or a linked list.
# If the stack runs out of memory, it’s called a stack overflow.

stk = []

# Append tp top of stack - O(1)
stk.append(5)

print(stk) # [5]

stk.append(4)
stk.append(3)
print(stk) # [5, 4, 3]

# Pop fom stack - O(1)

x = stk.pop()

print(x) # 3
print(stk) # [5, 4]

# Check what's on the top of stack O(1)
print(stk[-1]) # 4
