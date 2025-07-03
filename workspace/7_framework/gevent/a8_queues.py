import logging
import random
import time
from typing import List, Any
import gevent
from gevent.queue import Queue, LifoQueue, PriorityQueue, JoinableQueue, Empty, Full

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class QueueSyncConfig:
    """Configuration for queue synchronization examples."""
    def __init__(
        self,
        producer_delay_min: float = 0.1,
        producer_delay_max: float = 0.5,
        consumer_delay_min: float = 0.2,
        consumer_delay_max: float = 0.8,
        worker_delay_min: float = 0.5,
        worker_delay_max: float = 1.5,
        queue_size: int = 5,
        timeout: float = 2.0,
        num_items_per_producer: int = 3,
        num_producers: int = 2,
        num_consumers: int = 3
    ):
        self.producer_delay_min = producer_delay_min
        self.producer_delay_max = producer_delay_max
        self.consumer_delay_min = consumer_delay_min
        self.consumer_delay_max = consumer_delay_max
        self.worker_delay_min = worker_delay_min
        self.worker_delay_max = worker_delay_max
        self.queue_size = queue_size
        self.timeout = timeout
        self.num_items_per_producer = num_items_per_producer
        self.num_producers = num_producers
        self.num_consumers = num_consumers

class BasicQueueSync:
    """Demonstrates basic queue usage with producers and consumers."""
    def __init__(self, config: QueueSyncConfig):
        self.config = config
        self.queue = Queue(maxsize=self.config.queue_size)
        self.results: List[int] = []

    def producer(self, producer_id: int) -> None:
        """Produces items and puts them in the queue."""
        try:
            for i in range(self.config.num_items_per_producer):
                item = f"P{producer_id}-Item{i+1}"
                logger.info(f"Producer {producer_id}: Producing {item}")
                self.queue.put(item)
                gevent.sleep(random.uniform(
                    self.config.producer_delay_min,
                    self.config.producer_delay_max
                ))
            logger.info(f"Producer {producer_id}: Finished producing {self.config.num_items_per_producer} items")
        except Exception as e:
            logger.error(f"Producer {producer_id} error: {str(e)}")
            raise

    def consumer(self, consumer_id: int) -> int:
        """Consumes items from the queue until timeout."""
        items_processed = 0
        try:
            while True:
                try:
                    item = self.queue.get(timeout=self.config.timeout)
                    logger.info(f"Consumer {consumer_id}: Processing {item}")
                    gevent.sleep(random.uniform(
                        self.config.consumer_delay_min,
                        self.config.consumer_delay_max
                    ))
                    items_processed += 1
                except Empty:
                    logger.info(f"Consumer {consumer_id}: No more items, shutting down")
                    break
            logger.info(f"Consumer {consumer_id}: Processed {items_processed} items total")
            return items_processed
        except Exception as e:
            logger.error(f"Consumer {consumer_id} error: {str(e)}")
            raise

    def run(self) -> List[int]:
        """Runs the basic queue example."""
        logger.info("*** Running Basic Queue Example ***")
        try:
            producers = [gevent.spawn(self.producer, i + 1) for i in range(self.config.num_producers)]
            consumers = [gevent.spawn(self.consumer, i + 1) for i in range(self.config.num_consumers)]

            gevent.joinall(producers)
            logger.info("All producers finished")
            gevent.joinall(consumers, timeout=self.config.timeout)
            logger.info("All consumers finished")
            logger.info(f"Final queue size: {self.queue.qsize()}")

            return self.results
        except Exception as e:
            logger.error(f"Basic queue sync failed: {str(e)}")
            raise

class LifoQueueSync:
    """Demonstrates LIFO queue (stack-like) behavior."""
    def __init__(self, config: QueueSyncConfig):
        self.config = config
        self.queue = LifoQueue()
        self.items = ['First', 'Second', 'Third', 'Fourth', 'Fifth']

    def run(self) -> List[str]:
        """Runs the LIFO queue example."""
        logger.info("*** Running LIFO Queue Example ***")
        try:
            for item in self.items:
                self.queue.put(item)
                logger.info(f"Added to LIFO queue: {item}")

            logger.info("Retrieving from LIFO queue (Last-In-First-Out)")
            results = []
            while not self.queue.empty():
                item = self.queue.get()
                logger.info(f"Got from LIFO queue: {item}")
                results.append(item)
            return results
        except Exception as e:
            logger.error(f"LIFO queue sync failed: {str(e)}")
            raise

class PriorityQueueSync:
    """Demonstrates priority queue with prioritized tasks."""
    class Task:
        """Task with priority for PriorityQueue."""
        def __init__(self, priority: int, description: str):
            self.priority = priority
            self.description = description
            self.created_at = time.time()

        def __lt__(self, other: Any) -> bool:
            return self.priority < other.priority

        def __repr__(self) -> str:
            return f"Task(priority={self.priority}, desc='{self.description}')"

    def __init__(self, config: QueueSyncConfig):
        self.config = config
        self.queue = PriorityQueue()
        self.tasks = [
            self.Task(3, "Low priority task"),
            self.Task(1, "High priority task"),
            self.Task(2, "Medium priority task"),
            self.Task(1, "Another high priority task"),
            self.Task(4, "Very low priority task")
        ]

    def run(self) -> List[str]:
        """Runs the priority queue example."""
        logger.info("*** Running Priority Queue Example ***")
        try:
            for task in self.tasks:
                self.queue.put(task)
                logger.info(f"Added task: {task}")

            logger.info("Processing tasks by priority")
            results = []
            while not self.queue.empty():
                task = self.queue.get()
                logger.info(f"Processing: {task}")
                gevent.sleep(self.config.consumer_delay_min)
                results.append(str(task))
            return results
        except Exception as e:
            logger.error(f"Priority queue sync failed: {str(e)}")
            raise

class JoinableQueueSync:
    """Demonstrates JoinableQueue with task tracking."""
    def __init__(self, config: QueueSyncConfig):
        self.config = config
        self.queue = JoinableQueue()
        self.num_tasks = 8

    def worker(self, worker_id: int) -> None:
        """Processes tasks from JoinableQueue and marks them done."""
        try:
            while True:
                try:
                    task = self.queue.get(timeout=self.config.timeout)
                    logger.info(f"Worker {worker_id}: Processing task '{task}'")
                    work_time = random.uniform(
                        self.config.worker_delay_min,
                        self.config.worker_delay_max
                    )
                    gevent.sleep(work_time)
                    logger.info(f"Worker {worker_id}: Completed task '{task}' in {work_time:.2f}s")
                    self.queue.task_done()
                except Empty:
                    logger.info(f"Worker {worker_id}: No more tasks, stopping")
                    break
        except Exception as e:
            logger.error(f"Worker {worker_id} error: {str(e)}")
            raise

    def run(self) -> None:
        """Runs the JoinableQueue example."""
        logger.info("*** Running JoinableQueue Example ***")
        try:
            tasks = [f"Task-{i+1}" for i in range(self.num_tasks)]
            for task in tasks:
                self.queue.put(task)
            logger.info(f"Added {len(tasks)} tasks to JoinableQueue")

            workers = [gevent.spawn(self.worker, i + 1) for i in range(self.config.num_consumers)]
            logger.info("Waiting for all tasks to be completed")
            self.queue.join()
            logger.info("All tasks completed")

            gevent.joinall(workers, timeout=1)
        except Exception as e:
            logger.error(f"JoinableQueue sync failed: {str(e)}")
            raise

class ExceptionQueueSync:
    """Demonstrates queue with custom exception handling."""
    def __init__(self, config: QueueSyncConfig):
        self.config = config
        self.queue = Queue(maxsize=2)
        self.items = [f"Item-{i}" for i in range(6)]
        self.max_items_per_consumer = 5

    def producer(self) -> None:
        """Produces items, handling full queue exceptions."""
        try:
            for item in self.items:
                try:
                    self.queue.put(item, timeout=self.config.timeout)
                    logger.info(f"Successfully added: {item}")
                except Full:
                    logger.warning(f"Queue full! Could not add: {item}")
                gevent.sleep(self.config.producer_delay_min)
        except Exception as e:
            logger.error(f"Producer error: {str(e)}")
            raise

    def consumer(self, consumer_id: int) -> int:
        """Consumes items, handling empty queue exceptions."""
        processed = 0
        try:
            while processed < self.max_items_per_consumer:
                try:
                    item = self.queue.get(timeout=self.config.timeout)
                    logger.info(f"Consumer {consumer_id}: Got {item}")
                    processed += 1
                    gevent.sleep(self.config.consumer_delay_max)
                except Empty:
                    logger.info(f"Consumer {consumer_id}: Queue empty, waiting")
                    gevent.sleep(self.config.consumer_delay_min)
            logger.info(f"Consumer {consumer_id}: Finished processing {processed} items")
            return processed
        except Exception as e:
            logger.error(f"Consumer {consumer_id} error: {str(e)}")
            raise

    def run(self) -> int:
        """Runs the queue exception handling example."""
        logger.info("*** Running Queue Exception Handling Example ***")
        try:
            consumer_greenlet = gevent.spawn(self.consumer, 1)
            gevent.sleep(self.config.producer_delay_min)  # Let consumer start
            producer_greenlet = gevent.spawn(self.producer)
            gevent.joinall([producer_greenlet, consumer_greenlet], raise_error=True)
            logger.info("Queue exception handling example completed")
            return consumer_greenlet.value or 0
        except Exception as e:
            logger.error(f"Exception queue sync failed: {str(e)}")
            raise

def main():
    """Runs all queue synchronization examples."""
    config = QueueSyncConfig()

    # Basic Queue
    basic_queue = BasicQueueSync(config)
    basic_results = basic_queue.run()
    logger.info(f"Basic Queue results: {basic_results}\n" + "="*50 + "\n")

    # LIFO Queue
    lifo_queue = LifoQueueSync(config)
    lifo_results = lifo_queue.run()
    logger.info(f"LIFO Queue results: {lifo_results}\n" + "="*50 + "\n")

    # Priority Queue
    priority_queue = PriorityQueueSync(config)
    priority_results = priority_queue.run()
    logger.info(f"Priority Queue results: {priority_results}\n" + "="*50 + "\n")

    # JoinableQueue
    joinable_queue = JoinableQueueSync(config)
    joinable_queue.run()
    logger.info("JoinableQueue completed\n" + "="*50 + "\n")

    # Exception Queue
    exception_queue = ExceptionQueueSync(config)
    exception_results = exception_queue.run()
    logger.info(f"Exception Queue results: {exception_results}\n" + "="*50)

if __name__ == "__main__":
    main()
