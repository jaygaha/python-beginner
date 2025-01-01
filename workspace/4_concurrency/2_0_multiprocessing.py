# Multiprocessing: It is a package that supports spawning processes using an API similar to the threading module.
# The multiprocessing package offers both local and remote concurrency, effectively side-stepping the Global Interpreter Lock
# by using subprocesses instead of threads.
# Must terminate the process after the execution of the code.

from multiprocessing import Process, cpu_count

print()
print(f"Number of CPU cores: {cpu_count()}")

def print_continent(continent="Asia"):
    print(f"Continent: {continent}")

# confirm that the code is running in the main process
if __name__ == "__main__":
    names = ["Asia", "Africa", "Europe", "North America", "South America", "Australia", "Antarctica"]
    processes = []

    # initiate the process with any number of arguments
    process = Process(target=print_continent)
    processes.append(process)
    process.start()

    # initiate the process with arguments
    for name in names:
        process = Process(target=print_continent, args=(name,))
        processes.append(process)
        process.start()

    # terminate the process
    for process in processes:
        process.join()