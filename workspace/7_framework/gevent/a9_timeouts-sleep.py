import logging
import random
import time
from typing import List, Dict, Any, Optional
import gevent
from gevent.timeout import Timeout

# Set up logging that's easy to read
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)
logger = logging.getLogger(__name__)

class TimeoutConfig:
    """Settings for timeout and sleep examples."""
    def __init__(
        self,
        sleep_min: float = 0.5,
        sleep_max: float = 2.0,
        timeout_default: float = 2.0,
        network_failure_prob: float = 0.3,
        resource_open_delay: float = 0.2,
        resource_close_delay: float = 0.1,
        multi_stage_timeouts: Optional[List[float]] = None
    ):
        self.sleep_min = sleep_min
        self.sleep_max = sleep_max
        self.timeout_default = timeout_default
        self.network_failure_prob = network_failure_prob
        self.resource_open_delay = resource_open_delay
        self.resource_close_delay = resource_close_delay
        self.multi_stage_timeouts = multi_stage_timeouts or [1.0, 3.0, 0.8]

class BasicSleepExample:
    """Shows how gevent.sleep works with multiple tasks."""
    def __init__(self, config: TimeoutConfig, num_tasks: int = 4):
        self.config = config
        self.num_tasks = num_tasks

    def task(self, task_id: int, sleep_time: float) -> str:
        """Runs a task that sleeps for a given time."""
        logger.info(f"Task {task_id}: Starting, will sleep for {sleep_time:.2f}s")
        start = time.time()
        gevent.sleep(sleep_time)
        end = time.time()
        logger.info(f"Task {task_id}: Done after {end - start:.2f}s")
        return f"Task {task_id} result"

    def run(self) -> List[str]:
        """Runs multiple tasks at the same time."""
        logger.info("=== Basic Sleep Example ===")
        start_time = time.time()
        try:
            tasks = [
                gevent.spawn(self.task, i + 1, random.uniform(self.config.sleep_min, self.config.sleep_max))
                for i in range(self.num_tasks)
            ]
            gevent.joinall(tasks)
            end_time = time.time()
            logger.info(f"All tasks done in {end_time - start_time:.2f}s")
            return [task.value for task in tasks if task.value is not None]
        except Exception as e:
            logger.error(f"Basic sleep example failed: {e}")
            return []

class TimeoutContextExample:
    """Shows how to use timeouts to stop slow operations."""
    def __init__(self, config: TimeoutConfig):
        self.config = config
        self.test_cases = [
            (1, 1.0, 2.0),  # Should succeed
            (2, 3.0, 2.0),  # Should timeout
            (3, 0.5, 1.0),  # Should succeed
            (4, 4.0, 1.0),  # Should timeout
        ]

    def operation(self, operation_id: int, duration: float) -> str:
        """Simulates a slow operation."""
        logger.info(f"Operation {operation_id}: Starting (takes {duration}s)")
        gevent.sleep(duration)
        logger.info(f"Operation {operation_id}: Done")
        return f"Result from operation {operation_id}"

    def operation_with_timeout(self, operation_id: int, duration: float, timeout: float) -> str:
        """Runs operation with a timeout."""
        try:
            with Timeout(timeout):
                result = self.operation(operation_id, duration)
                return result
        except Timeout:
            logger.info(f"Operation {operation_id}: Timeout after {timeout}s")
            return f"Operation {operation_id}: TIMED OUT"

    def run(self) -> List[str]:
        """Runs operations with different timeouts."""
        logger.info("=== Timeout Context Example ===")
        try:
            greenlets = [
                gevent.spawn(self.operation_with_timeout, op_id, duration, timeout)
                for op_id, duration, timeout in self.test_cases
            ]
            gevent.joinall(greenlets)
            results = [g.value for g in greenlets if g.value is not None]
            logger.info("Results:")
            for result in results:
                logger.info(f"  {result}")
            return results
        except Exception as e:
            logger.error(f"Timeout context example failed: {e}")
            return []

class CustomTimeoutExample:
    """Shows how to handle timeouts with a custom error."""
    class CustomTimeoutError(Exception):
        """Custom error for timeouts."""
        pass

    def __init__(self, config: TimeoutConfig, num_operations: int = 6):
        self.config = config
        self.num_operations = num_operations

    def network_operation(self, operation_id: int) -> str:
        """Simulates a network operation that might fail."""
        delay = random.uniform(self.config.sleep_min, self.config.sleep_max * 2)
        logger.info(f"Network operation {operation_id}: Starting (takes {delay:.1f}s)")
        gevent.sleep(delay)
        if random.random() < self.config.network_failure_prob:
            raise Exception(f"Network error in operation {operation_id}")
        return f"Network operation {operation_id} succeeded"

    def safe_network_call(self, operation_id: int) -> Dict[str, Any]:
        """Runs network operation with timeout and error handling."""
        try:
            with Timeout(self.config.timeout_default, self.CustomTimeoutError):
                result = self.network_operation(operation_id)
                logger.info(f"Operation {operation_id}: Success")
                return {"status": "success", "result": result}
        except self.CustomTimeoutError:
            logger.info(f"Operation {operation_id}: Timeout after {self.config.timeout_default}s")
            return {"status": "timeout", "error": "Operation took too long"}
        except Exception as e:
            logger.info(f"Operation {operation_id}: Error - {e}")
            return {"status": "error", "error": str(e)}

    def run(self) -> Dict[str, int]:
        """Runs multiple network operations and counts results."""
        logger.info("=== Custom Timeout Example ===")
        try:
            greenlets = [
                gevent.spawn(self.safe_network_call, i + 1)
                for i in range(self.num_operations)
            ]
            gevent.joinall(greenlets)
            results = [g.value for g in greenlets if g.value is not None]
            summary = {"success": 0, "timeout": 0, "error": 0}
            for result in results:
                summary[result["status"]] += 1
            logger.info(f"Summary: {summary['success']} successful, {summary['timeout']} timeouts, {summary['error']} errors")
            return summary
        except Exception as e:
            logger.error(f"Custom timeout example failed: {e}")
            return {"success": 0, "timeout": 0, "error": 0}

class ResourceTimeoutExample:
    """Shows how to clean up resources after a timeout."""
    class ResourceManager:
        """Manages a resource that needs cleanup."""
        def __init__(self, resource_id: int):
            self.resource_id = resource_id
            self.is_open = False
            self.data: List[str] = []

        def open(self, delay: float) -> None:
            """Opens the resource."""
            logger.info(f"Resource {self.resource_id}: Opening")
            gevent.sleep(delay)
            self.is_open = True
            logger.info(f"Resource {self.resource_id}: Opened")

        def process(self, duration: float) -> None:
            """Processes data with the resource."""
            if not self.is_open:
                raise Exception("Resource not open")
            logger.info(f"Resource {self.resource_id}: Processing for {duration}s")
            gevent.sleep(duration)
            self.data.append(f"Processed at {time.time()}")
            logger.info(f"Resource {self.resource_id}: Processing done")

        def close(self, delay: float) -> None:
            """Closes the resource."""
            if self.is_open:
                logger.info(f"Resource {self.resource_id}: Closing")
                gevent.sleep(delay)
                self.is_open = False
                logger.info(f"Resource {self.resource_id}: Closed")

    def __init__(self, config: TimeoutConfig):
        self.config = config
        self.test_cases = [
            (1, 1.0, 2.0),  # Should succeed
            (2, 3.0, 2.0),  # Should timeout
            (3, 0.5, 1.0),  # Should succeed
        ]

    def process_with_timeout(self, resource_id: int, process_duration: float, timeout_duration: float) -> Dict[str, Any]:
        """Processes with a resource, ensuring cleanup."""
        resource = self.ResourceManager(resource_id)
        try:
            resource.open(self.config.resource_open_delay)
            with Timeout(timeout_duration):
                resource.process(process_duration)
            logger.info(f"Resource {resource_id}: Successfully completed processing")
            return {"status": "success", "data_count": len(resource.data)}
        except Timeout:
            logger.info(f"Resource {resource_id}: Timeout after {timeout_duration}s")
            return {"status": "timeout", "data_count": len(resource.data)}
        except Exception as e:
            logger.info(f"Resource {resource_id}: Error - {e}")
            return {"status": "error", "error": str(e)}
        finally:
            resource.close(self.config.resource_close_delay)

    def run(self) -> List[Dict[str, Any]]:
        """Runs resource processing with timeouts."""
        logger.info("=== Timeout with Cleanup Example ===")
        try:
            greenlets = [
                gevent.spawn(self.process_with_timeout, res_id, proc_dur, timeout_dur)
                for res_id, proc_dur, timeout_dur in self.test_cases
            ]
            gevent.joinall(greenlets)
            results = [g.value for g in greenlets if g.value is not None]
            logger.info("Resource management results:")
            for result in results:
                logger.info(f"  Status: {result['status']}, Data processed: {result.get('data_count', 0)}")
            return results
        except Exception as e:
            logger.error(f"Resource timeout example failed: {e}")
            return []

class MultiStageTimeoutExample:
    """Shows how to use different timeouts for multiple stages."""
    def __init__(self, config: TimeoutConfig, num_operations: int = 5):
        self.config = config
        self.num_operations = num_operations

    def multi_stage_operation(self, operation_id: int) -> Dict[str, Any]:
            """Runs an operation with multiple stages, each with its own timeout."""
            results = []
            try:
                # Stage 1: Quick initialization
                with Timeout(self.config.multi_stage_timeouts[0]):
                    logger.info(f"Operation {operation_id}: Stage 1 - Quick init")
                    gevent.sleep(random.uniform(0.1, 0.8))
                    results.append("Stage 1 complete")

                # Stage 2: Main processing
                with Timeout(self.config.multi_stage_timeouts[1]):
                    logger.info(f"Operation {operation_id}: Stage 2 - Main processing")
                    gevent.sleep(random.uniform(1.0, 2.5))
                    results.append("Stage 2 complete")

                # Stage 3: Finalization
                with Timeout(self.config.multi_stage_timeouts[2]):
                    logger.info(f"Operation {operation_id}: Stage 3 - Finalization")
                    gevent.sleep(random.uniform(0.1, 1.2))
                    results.append("Stage 3 complete")

                return {"status": "success", "results": results}
            except Timeout:
                logger.info(f"Operation {operation_id}: Timeout at stage {len(results) + 1}")
                return {"status": "failed", "stage": len(results) + 1, "results": results}
            except Exception as e:
                logger.info(f"Operation {operation_id}: Error - {e}")
                return {"status": "error", "stage": len(results) + 1, "results": results}

    def run(self) -> List[Dict[str, Any]]:
        """Runs multiple multi-stage operations."""
        logger.info("=== Multiple Timeout Strategies Example ===")
        try:
            greenlets = [
                gevent.spawn(self.multi_stage_operation, i + 1)
                for i in range(self.num_operations)
            ]
            gevent.joinall(greenlets)
            results = [g.value for g in greenlets if g.value is not None]
            logger.info("Multi-stage operation results:")
            for i, result in enumerate(results, 1):
                if result["status"] == "success":
                    logger.info(f"  Operation {i}: SUCCESS - All {len(result['results'])} stages completed")
                else:
                    logger.info(f"  Operation {i}: FAILED at stage {result['stage']} - Completed {len(result['results'])} stages")
            return results
        except Exception as e:
            logger.error(f"Multi-stage timeout example failed: {e}")
            return []

def main():
    """Runs all timeout and sleep examples."""
    config = TimeoutConfig()

    # Basic Sleep Example
    basic_sleep = BasicSleepExample(config)
    basic_results = basic_sleep.run()
    logger.info(f"Basic Sleep results: {basic_results}\n" + "="*50 + "\n")

    # Timeout Context Example
    timeout_context = TimeoutContextExample(config)
    timeout_results = timeout_context.run()
    logger.info(f"Timeout Context results: {timeout_results}\n" + "="*50 + "\n")

    # Custom Timeout Example
    custom_timeout = CustomTimeoutExample(config)
    custom_results = custom_timeout.run()
    logger.info(f"Custom Timeout results: {custom_results}\n" + "="*50 + "\n")

    # Resource Timeout Example
    resource_timeout = ResourceTimeoutExample(config)
    resource_results = resource_timeout.run()
    logger.info(f"Resource Timeout results: {resource_results}\n" + "="*50 + "\n")

    # Multi-Stage Timeout Example
    multi_stage_timeout = MultiStageTimeoutExample(config)
    multi_stage_results = multi_stage_timeout.run()
    logger.info(f"Multi-Stage Timeout results: {multi_stage_results}\n" + "="*50)

if __name__ == "__main__":
    main()
