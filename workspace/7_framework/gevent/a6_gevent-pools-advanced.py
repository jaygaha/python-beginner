import time
import random
from typing import List, Optional
import logging
import gevent
from gevent.pool import Pool
from gevent.queue import Queue

class ProducerConsumerConfig:
    """Configuration for the ProducerConsumer system."""
    def __init__(
        self,
        num_consumers: int = 3,
        queue_size: int = 10,
        producer_delay: float = 0.1,
        consumer_min_delay: float = 0.2,
        consumer_max_delay: float = 0.8
    ):
        self.num_consumers = num_consumers
        self.queue_size = queue_size
        self.producer_delay = producer_delay
        self.consumer_min_delay = consumer_min_delay
        self.consumer_max_delay = consumer_max_delay

class ProducerConsumer:
    """
    A producer-consumer system using gevent with a thread pool and queue.

    Producers create items and put them in a task queue.
    Consumers process items concurrently and store results in a results queue.
    Uses sentinel values (None) to signal consumer shutdown.
    """
    def __init__(self, config: Optional[ProducerConsumerConfig] = None):
        self.config = config or ProducerConsumerConfig()
        self.task_queue = Queue(maxsize=self.config.queue_size)
        self.result_queue = Queue()
        self.consumer_pool = Pool(size=self.config.num_consumers)
        self.logger = logging.getLogger(__name__)

    def _produce_item(self, item_id: int) -> str:
        """Creates a single item with a simulated delay."""
        item = f"Item-{item_id}"
        self.logger.info(f"Producer: Created {item}")
        gevent.sleep(self.config.producer_delay)
        return item

    def producer(self, num_items: int) -> None:
        """Produces items and places them in the task queue."""
        try:
            self.logger.info(f"Producer: Starting production of {num_items} items")
            for i in range(num_items):
                item = self._produce_item(i + 1)
                self.task_queue.put(item)

            # Send sentinel values for each consumer
            for _ in range(self.config.num_consumers):
                self.task_queue.put(None)
            self.logger.info("Producer: Completed production and sent shutdown signals")
        except Exception as e:
            self.logger.error(f"Producer error: {str(e)}")
            raise

    def consumer(self, consumer_id: int) -> None:
        """Consumes items from the task queue until receiving a sentinel."""
        try:
            while True:
                item = self.task_queue.get()
                if item is None:
                    self.logger.info(f"Consumer {consumer_id}: Received shutdown signal")
                    break

                self.logger.info(f"Consumer {consumer_id}: Processing {item}")
                processing_time = random.uniform(
                    self.config.consumer_min_delay,
                    self.config.consumer_max_delay
                )
                gevent.sleep(processing_time)

                result = f"Processed {item} by C{consumer_id}"
                self.result_queue.put(result)
        except Exception as e:
            self.logger.error(f"Consumer {consumer_id} error: {str(e)}")
            raise

    def run(self, items_to_produce: int = 12) -> List[str]:
        """
        Runs the producer-consumer system and returns processed results.

        Args:
            items_to_produce: Number of items to produce

        Returns:
            List of processed results

        Raises:
            RuntimeError: If system execution fails
        """
        start_time = time.time()
        self.logger.info("Starting producer-consumer system")

        try:
            # Spawn producer
            producer_greenlet = gevent.spawn(self.producer, items_to_produce)

            # Spawn consumers
            for i in range(self.config.num_consumers):
                self.consumer_pool.spawn(self.consumer, i + 1)

            # Wait for completion
            producer_greenlet.join()
            self.consumer_pool.join()

            # Collect results (only the expected number of items)
            results = []
            for _ in range(items_to_produce):
                try:
                    result = self.result_queue.get_nowait()
                    results.append(result)
                except gevent.queue.Empty:
                    self.logger.warning("Result queue empty before collecting all results")
                    break

            end_time = time.time()
            self.logger.info(
                f"System completed: "
                f"Time={end_time - start_time:.2f}s, "
                f"Produced={items_to_produce}, "
                f"Processed={len(results)}"
            )
            return results

        except Exception as e:
            self.logger.error(f"System execution failed: {str(e)}")
            raise RuntimeError(f"System execution failed: {str(e)}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
    config = ProducerConsumerConfig(num_consumers=3)
    system = ProducerConsumer(config)
    results = system.run(items_to_produce=12)
