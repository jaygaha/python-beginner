# Multiprocessing Pool
# The Pool class represents a pool of worker processes.
# It has methods that allow tasks to be offloaded to the worker processes in a few different ways.
from multiprocessing import Pool
import time

work = (["A", 5], ["B", 2], ["C", 1], ["D", 3])

def work_log(work_data):
    print(f"Process {work_data[0]} waiting {work_data[1]} seconds")
    time.sleep(int(work_data[1]))
    print(f"Process {work_data[0]} Finished.")

def pool_handler():
    # create a pool of workers
    '''
        By default, the number of workers is the number of cores in the CPU.
        You can specify the number of workers by passing the processes argument to the Pool class.
    '''
    pool = Pool(processes=2)
    '''
        The map() function in the Pool class applies the function to each element in the iterable.
        It blocks the main program until all the processes are finished.
    '''
    # work_log: function to be applied to each element in the iterable
    # work: iterable
    pool.map(work_log, work)

if __name__ == "__main__":
    pool_handler()


# Output
'''
Process A waiting 5 seconds
Process B waiting 2 seconds
Process B Finished.
Process C waiting 1 seconds
Process C Finished.
Process D waiting 3 seconds
Process A Finished.
Process D Finished.
'''