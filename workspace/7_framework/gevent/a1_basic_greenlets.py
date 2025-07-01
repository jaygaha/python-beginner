import gevent
from gevent import Greenlet

def simple_task(name, duration):
    """
    A simple task that simulates work by sleeping

        Args:
            name (str): Name of the task
            duration (int): How long to sleep
    """

    print(f"Task {name} starting")
    # gevent.sleep() yields control to other greenlets
    gevent.sleep(duration)
    print(f"Task {name} completed after {duration} seconds")
    return f"Result from {name}"


# Method 1: Using gevent.spawn()
print("Method 1: Using gevent.spawn()")
# spawn() creates and starts a greenlet immediately
greenlet1 = gevent.spawn(simple_task, "A", 2)
greenlet2 = gevent.spawn(simple_task, "B", 1)
greenlet3 = gevent.spawn(simple_task, "C", 3)

# Wait for all greenlets to complete and get their results
results = gevent.joinall([greenlet1, greenlet2, greenlet3], timeout=10)
print("All tasks completed")

# Access individual results
print("Individual results:")
# for result in results:
#     print(result.value)
print(f"Greenlet1 result: {greenlet1.value}")
print(f"Greenlet2 result: {greenlet2.value}")
print(f"Greenlet3 result: {greenlet3.value}")


# It will generates = 50 times
print("\n" + "="*50 + "\n")

# Method 2: Using Greenlet class directly
print("Method 2: Using Greenlet class")

class CustomGreenlet(Greenlet):
    """
    Custom greenlet class that inherits from Greenlet
    """
    def __init__(self, name, duration):
        Greenlet.__init__(self)  # Initialize parent class
        self.name = name
        self.duration = duration

    def _run(self):
        """
        Override _run method to define what the greenlet does
        """
        print(f"Custom greenlet {self.name} starting")
        gevent.sleep(self.duration)
        print(f"Custom greenlet {self.name} finished")
        return f"Custom result from {self.name}"

# Create custom greenlets
custom1 = CustomGreenlet("X", 1)
custom2 = CustomGreenlet("Y", 2)

# Start them manually
custom1.start()
custom2.start()

# Wait for completion
gevent.joinall([custom1, custom2])
print(f"Custom1 result: {custom1.value}")
print(f"Custom2 result: {custom2.value}")
