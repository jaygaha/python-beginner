import logging
import random
import time
from typing import List, Dict, Any
import gevent
from gevent.timeout import Timeout

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)
logger = logging.getLogger(__name__)

class ErrorHandlingConfig:
    """Configuration for error handling example."""
    def __init__(
        self,
        task_timeout: float = 2.0,
        task_delay_min: float = 0.5,
        task_delay_max: float = 3.0,
        failure_probability: float = 0.3,
        num_tasks: int = 5
    ):
        self.task_timeout = task_timeout
        self.task_delay_min = task_delay_min
        self.task_delay_max = task_delay_max
        self.failure_probability = failure_probability
        self.num_tasks = num_tasks

class ErrorHandlingExample:
    """Demonstrates error handling with gevent for concurrent tasks."""
    def __init__(self, config: ErrorHandlingConfig):
        self.config = config

    def process_task(self, task_id: int) -> Dict[str, Any]:
        """Simulates a task that might fail due to timeout, input, or network errors."""
        logger.info(f"Task {task_id}: Starting")
        start_time = time.time()
        try:
            # Simulate variable task duration
            delay = random.uniform(self.config.task_delay_min, self.config.task_delay_max)
            with Timeout(self.config.task_timeout):
                gevent.sleep(delay)

            # Simulate invalid input error
            if random.random() < self.config.failure_probability:
                raise ValueError(f"Task {task_id}: Invalid input data")

            # Simulate network error
            if random.random() < self.config.failure_probability:
                raise ConnectionError(f"Task {task_id}: Network failure")

            # Successful task
            result = f"Task {task_id} result"
            logger.info(f"Task {task_id}: Completed in {time.time() - start_time:.2f}s")
            return {"task_id": task_id, "status": "success", "result": result}

        except Timeout:
            logger.info(f"Task {task_id}: Timeout after {self.config.task_timeout}s")
            return {"task_id": task_id, "status": "timeout", "error": "Task took too long"}
        except ValueError as e:
            logger.info(f"Task {task_id}: Input error - {e}")
            return {"task_id": task_id, "status": "error", "error": str(e)}
        except ConnectionError as e:
            logger.info(f"Task {task_id}: Network error - {e}")
            return {"task_id": task_id, "status": "error", "error": str(e)}
        except Exception as e:
            logger.info(f"Task {task_id}: Unexpected error - {e}")
            return {"task_id": task_id, "status": "error", "error": str(e)}

    def run(self) -> List[Dict[str, Any]]:
            """Runs multiple tasks concurrently with error handling."""
            logger.info("=== Error Handling Example ===")
            try:
                start_time = time.time()
                greenlets = [
                    gevent.spawn(self.process_task, i + 1)
                    for i in range(self.config.num_tasks)
                ]
                gevent.joinall(greenlets)
                results = [g.value for g in greenlets if g.value is not None]

                # Summarize results
                summary = {
                    "success": sum(1 for r in results if r is not None and r["status"] == "success"),
                    "timeout": sum(1 for r in results if r is not None and r["status"] == "timeout"),
                    "error": sum(1 for r in results if r is not None and r["status"] == "error")
                }
                logger.info(f"Summary: {summary['success']} successful, "
                            f"{summary['timeout']} timeouts, "
                            f"{summary['error']} errors in {time.time() - start_time:.2f}s")
                return results
            except Exception as e:
                logger.error(f"Error handling example failed: {e}")
                return []

def main():
    """Runs the error handling example."""
    config = ErrorHandlingConfig()
    example = ErrorHandlingExample(config)
    results = example.run()
    logger.info(f"Results: {results}")

if __name__ == "__main__":
    main()
