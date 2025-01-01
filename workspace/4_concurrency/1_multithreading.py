# Multithreading: Running multiple threads simultaneously
# Used to perform multiple tasks at the same time
# Good for I/O bound tasks like reading files or fetching data from the APIs
# threading.Thread(target=my-func)
# Each thread has its own memory space

import threading
import time

def walk_dog(name):
    time.sleep(8)
    print(f"Finish Walking the {name} dog")

def take_out_trash():
    time.sleep(3)
    print("Taking out the trash")

def get_mail():
    time.sleep(4)
    print("Getting the mail")

# Create threads
# target: function to be executed
# tuple is used to pass arguments to the function
# args: arguments to be passed to the function
chore1 = threading.Thread(target=walk_dog, args=("German Shepherd",))
# start() method is used to start the thread
chore1.start()

chore2 = threading.Thread(target=take_out_trash)
chore2.start()

chore3 = threading.Thread(target=get_mail)
chore3.start()

# join() method is used to wait for the threads to finish
chore1.join()
chore2.join()
chore3.join()

print("All chores are done")

# Output:
# Taking out the trash
# Getting the mail
# Walking the dog

# Running in the main thread
# walk_dog()
# take_out_trash()
# get_mail()

# Output:
# Walking the dog
# Taking out the trash
# Getting the mail
