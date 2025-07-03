import logging
import random
import time
from typing import List, Dict, Any, Optional
import gevent
from gevent.event import Event, AsyncResult

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class EventSyncConfig:
    """Configuration for event synchronization examples."""
    def __init__(
        self,
        producer_delay_min: float = 2.0,
        producer_delay_max: float = 4.0,
        async_comp_delay_min: float = 1.0,
        async_comp_delay_max: float = 3.0,
        async_timeout: float = 5.0,
        failure_probability: float = 0.2,
        stage_delays: Optional[List[float]] = None
    ):
        self.producer_delay_min = producer_delay_min
        self.producer_delay_max = producer_delay_max
        self.async_comp_delay_min = async_comp_delay_min
        self.async_comp_delay_max = async_comp_delay_max
        self.async_timeout = async_timeout
        self.failure_probability = failure_probability
        self.stage_delays = stage_delays or [1.0, 1.5, 1.0]

class BasicEventSync:
    """Demonstrates basic event synchronization with one producer and multiple consumers."""
    def __init__(self, config: EventSyncConfig, num_consumers: int = 3):
        self.config = config
        self.data_ready_event = Event()
        self.shared_data: Optional[Dict[str, Any]] = None
        self.num_consumers = num_consumers

    def producer(self) -> None:
        """Produces data and signals consumers when ready."""
        try:
            logger.info("Producer: Starting data preparation")
            gevent.sleep(random.uniform(self.config.producer_delay_min, self.config.producer_delay_max))

            self.shared_data = {
                'timestamp': time.time(),
                'data': [random.randint(1, 100) for _ in range(10)],
                'status': 'ready'
            }
            logger.info("Producer: Data ready, signaling consumers")
            self.data_ready_event.set()
        except Exception as e:
            logger.error(f"Producer error: {str(e)}")
            raise

    def consumer(self, consumer_id: int) -> str:
        """Waits for data and processes it."""
        try:
            logger.info(f"Consumer {consumer_id}: Waiting for data")
            self.data_ready_event.wait()
            logger.info(f"Consumer {consumer_id}: Got data signal, processing")

            if self.shared_data:
                avg = sum(self.shared_data['data']) / len(self.shared_data['data'])
                logger.info(f"Consumer {consumer_id}: Processed data, average = {avg:.2f}")
                return f"Consumer {consumer_id} completed"
            else:
                logger.warning(f"Consumer {consumer_id}: No data available")
                return f"Consumer {consumer_id} failed: No data"
        except Exception as e:
            logger.error(f"Consumer {consumer_id} error: {str(e)}")
            raise

    def run(self) -> List[str]:
        """Runs the basic event synchronization example."""
        logger.info("*** Running Basic Event Synchronization ***")
        try:
            greenlets = [gevent.spawn(self.producer)] + [
                gevent.spawn(self.consumer, i + 1) for i in range(self.num_consumers)
            ]
            results = gevent.joinall(greenlets, raise_error=True)
            return [g.value for g in results[1:] if g.value]
        except Exception as e:
            logger.error(f"Basic event sync failed: {str(e)}")
            raise

class AsyncResultSync:
    """Demonstrates AsyncResult for handling asynchronous computations."""
    def __init__(self, config: EventSyncConfig, num_computations: int = 5):
        self.config = config
        self.num_computations = num_computations

    def computation(self, computation_id: int) -> AsyncResult:
        """Performs async computation and returns result via AsyncResult."""
        result = AsyncResult()

        def do_work():
            try:
                logger.info(f"Computation {computation_id}: Starting work")
                gevent.sleep(random.uniform(
                    self.config.async_comp_delay_min,
                    self.config.async_comp_delay_max
                ))

                if random.random() < self.config.failure_probability:
                    raise Exception(f"Computation {computation_id} failed!")

                value = random.randint(100, 1000)
                logger.info(f"Computation {computation_id}: Completed with result {value}")
                result.set(value)
            except Exception as e:
                logger.error(f"Computation {computation_id} error: {str(e)}")
                result.set_exception(e)

        gevent.spawn(do_work)
        return result

    def run(self) -> List[str]:
        """Runs the async computation example."""
        logger.info("*** Running AsyncResult Example ***")
        logger.info("Starting multiple async computations")
        results = []
        async_results = [self.computation(i + 1) for i in range(self.num_computations)]

        for i, async_result in enumerate(async_results, 1):
            try:
                value = async_result.get(timeout=self.config.async_timeout)
                logger.info(f"Got result from computation {i}: {value}")
                results.append(f"Computation {i}: {value}")
            except Exception as e:
                logger.error(f"Computation {i} failed: {str(e)}")
                results.append(f"Computation {i} failed: {str(e)}")

        return results

class MultiStageProcess:
    """Coordinates multiple processing stages using events."""
    def __init__(self, config: EventSyncConfig):
        self.config = config
        self.stage_events = [Event() for _ in range(3)]
        self.results: Dict[str, str] = {}

    def stage_worker(self, stage_num: int) -> None:
        """Worker for a specific stage, waiting for the previous stage."""
        stage_name = f"Stage {stage_num}"
        try:
            if stage_num > 1:
                logger.info(f"{stage_name}: Waiting for Stage {stage_num-1}")
                self.stage_events[stage_num-2].wait()

            logger.info(f"{stage_name}: Processing")
            gevent.sleep(self.config.stage_delays[stage_num-1])

            self.results[f'stage{stage_num}'] = (
                f"Stage {stage_num} data prepared" if stage_num == 1
                else f"Processed: {self.results[f'stage{stage_num-1}']}"
            )
            logger.info(f"{stage_name}: Complete")
            self.stage_events[stage_num-1].set()
        except Exception as e:
            logger.error(f"{stage_name} error: {str(e)}")
            raise

    def monitor(self) -> None:
        """Monitors progress of all stages."""
        try:
            for i, event in enumerate(self.stage_events, 1):
                logger.info(f"Monitor: Waiting for Stage {i}")
                event.wait()
                logger.info(f"Monitor: Stage {i} completed")

            logger.info("Monitor: All stages complete")
            logger.info(f"Final results: {self.results}")
        except Exception as e:
            logger.error(f"Monitor error: {str(e)}")
            raise

    def run(self) -> Dict[str, str]:
        """Runs the multi-stage process."""
        logger.info("*** Running Multiple Event Coordination ***")
        try:
            greenlets = [
                gevent.spawn(self.stage_worker, i + 1) for i in range(3)
            ] + [gevent.spawn(self.monitor)]
            gevent.joinall(greenlets, raise_error=True)
            return self.results
        except Exception as e:
            logger.error(f"Multi-stage process failed: {str(e)}")
            raise

class TimeoutEventSync:
    """Demonstrates event handling with timeout."""
    def __init__(self, config: EventSyncConfig):
        self.config = config
        self.timeout_event = Event()

    def slow_setter(self) -> None:
        """Sets event after a long delay."""
        try:
            logger.info("Slow setter: Will set event in 5 seconds")
            gevent.sleep(5)
            self.timeout_event.set()
            logger.info("Slow setter: Event set")
        except Exception as e:
            logger.error(f"Slow setter error: {str(e)}")
            raise

    def patient_waiter(self) -> str:
        """Waits indefinitely for event."""
        try:
            logger.info("Patient waiter: Waiting indefinitely")
            self.timeout_event.wait()
            logger.info("Patient waiter: Got the event")
            return "Patient waiter: Completed"
        except Exception as e:
            logger.error(f"Patient waiter error: {str(e)}")
            raise

    def impatient_waiter(self, timeout: float = 2.0) -> str:
        """Waits with timeout for event."""
        try:
            logger.info(f"Impatient waiter: Waiting with {timeout} second timeout")
            if self.timeout_event.wait(timeout=timeout):
                logger.info("Impatient waiter: Got the event in time")
                return "Impatient waiter: Completed"
            else:
                logger.info("Impatient waiter: Timeout, giving up")
                return "Impatient waiter: Timeout"
        except Exception as e:
            logger.error(f"Impatient waiter error: {str(e)}")
            raise

    def run(self) -> List[str]:
        """Runs the event timeout example."""
        logger.info("*** Running Event Timeout Example ***")
        try:
            greenlets = [
                gevent.spawn(self.slow_setter),
                gevent.spawn(self.patient_waiter),
                gevent.spawn(self.impatient_waiter, timeout=2.0)
            ]
            results = gevent.joinall(greenlets, raise_error=True)
            return [g.value for g in results[1:] if g.value]
        except Exception as e:
            logger.error(f"Event timeout example failed: {str(e)}")
            raise

def main():
    """Runs all event synchronization examples."""
    config = EventSyncConfig()

    # Run Basic Event Synchronization
    basic_sync = BasicEventSync(config)
    basic_results = basic_sync.run()
    logger.info(f"Basic Event results: {basic_results}\n" + "="*50 + "\n")

    # Run AsyncResult Example
    async_sync = AsyncResultSync(config)
    async_results = async_sync.run()
    logger.info(f"AsyncResult results: {async_results}\n" + "="*50 + "\n")

    # Run Multi-Stage Process
    multi_stage = MultiStageProcess(config)
    multi_results = multi_stage.run()
    logger.info(f"Multi-Stage results: {multi_results}\n" + "="*50 + "\n")

    # Run Event Timeout Example
    timeout_sync = TimeoutEventSync(config)
    timeout_results = timeout_sync.run()
    logger.info(f"Timeout Event results: {timeout_results}\n" + "="*50)

if __name__ == "__main__":
    main()
