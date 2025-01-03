from hash_distribution import plot, distribute
from custom_hash_func import custom_hash_func
from string import printable

print(plot(distribute(printable, num_containers=2)))

'''
  0 ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■ (54)
  1 ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■         (46)
  None
'''

print(plot(distribute(printable, num_containers=8)))

'''
  0 ■■■■■■■■■■■■■■■■ (16)
  1 ■■■■■■■■■■■■■■■■ (16)
  2 ■■■■■■■■■■■■■    (13)
  3 ■■■■■■■■■■■■     (12)
  4 ■■■■■■■■■■■      (11)
  5 ■■■■■■■■■■■■■■   (14)
  6 ■■■■■■■■■■■■     (12)
  7 ■■■■■■           (6)
  None
'''

print(custom_hash_func("a"),
custom_hash_func("b"),
custom_hash_func("c"))

'''
  175 176 177
'''

print(plot(distribute(printable, num_containers=6, hash_function=custom_hash_func)))

'''
  0 ■■■■■■■■■■■■■■■■   (16)
  1 ■■■■■■■■■■■■■■■■   (16)
  2 ■■■■■■■■■■■■■■■    (15)
  3 ■■■■■■■■■■■■■■■■■■ (18)
  4 ■■■■■■■■■■■■■■■■■  (17)
  5 ■■■■■■■■■■■■■■■■■■ (18)
'''