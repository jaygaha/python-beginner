# Python multiprocessing example

from multiprocessing import Lock, Process,Queue, current_process
import time
# function to add data to queue. Empty exception is handled by the caller
import queue

def do_job(tasks_to_accomplish, tasks_that_are_done):
    while True:
        try:
            '''
                try to get task from the queue. get_nowait() function will
                raise queue.Empty exception if the queue is empty.
                queue(False) function would do the same task also.
            '''
            task = tasks_to_accomplish.get_nowait()
            print(task)
        except queue.Empty:
            break
        else:
            '''
                if no exception has been raised, add the task completion
                message to task_that_are_done queue
            '''
            print(task)
            tasks_that_are_done.put(task + ' is done by ' + current_process().name)
            time.sleep(.5)
    return True

def main():
    numer_of_task = 10
    number_of_processes = 4
    tasks_to_accomplish = Queue()
    tasks_that_are_done = Queue()
    processes = []

    for i in range(numer_of_task):
        tasks_to_accomplish.put("Task no " + str(i))

    # creating processes
    for w in range(number_of_processes):
        p = Process(target=do_job, args=(tasks_to_accomplish, tasks_that_are_done))
        processes.append(p)
        p.start()

    # completing process
    for p in processes:
        p.join()

    # print the output
    while not tasks_that_are_done.empty():
        print(tasks_that_are_done.get())

if __name__ == "__main__":
    main()