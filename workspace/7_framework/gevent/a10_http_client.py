import logging
import time
from typing import List, Dict, Any
import gevent
from gevent import monkey
import requests

# Apply monkey patching for HTTP requests
monkey.patch_all()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)
logger = logging.getLogger(__name__)

class HttpClientConfig:
    """Configuration for HTTP client examples."""
    def __init__(
        self,
        default_timeout: float = 10.0,
        session_timeout: float = 5.0,
        retry_timeout: float = 2.0,
        max_retries: int = 2,
        session_delay: float = 0.1,
        max_concurrent_timeout: float = 15.0,
        retry_base_delay: float = 0.5
    ):
        self.default_timeout = default_timeout
        self.session_timeout = session_timeout
        self.retry_timeout = retry_timeout
        self.max_retries = max_retries
        self.session_delay = session_delay
        self.max_concurrent_timeout = max_concurrent_timeout
        self.retry_base_delay = retry_base_delay

class ConcurrentHttpRequests:
    """Handles concurrent HTTP GET requests."""
    def __init__(self, config: HttpClientConfig):
        self.config = config
        self.urls = [
            'https://httpbin.org/delay/1',
            'https://httpbin.org/delay/2',
            'https://httpbin.org/json',
            'https://httpbin.org/html',
            'https://httpbin.org/status/200',
            'https://httpbin.org/headers'
        ]

    def fetch_url(self, url: str, request_id: int) -> Dict[str, Any]:
        """Fetches a URL and returns response information."""
        start_time = time.time()
        try:
            logger.info(f"Request {request_id}: Starting GET {url}")
            response = requests.get(url, timeout=self.config.default_timeout)
            end_time = time.time()
            result = {
                'request_id': request_id,
                'url': url,
                'status_code': response.status_code,
                'response_time': end_time - start_time,
                'content_length': len(response.content),
                'headers': dict(response.headers),
                'success': True
            }
            logger.info(f"Request {request_id}: Done in {result['response_time']:.2f}s "
                        f"(Status: {result['status_code']})")
            return result
        except Exception as e:
            end_time = time.time()
            logger.info(f"Request {request_id}: Error - {e}")
            return {
                'request_id': request_id,
                'url': url,
                'error': str(e),
                'response_time': end_time - start_time,
                'success': False
            }

    def run(self) -> Dict[str, Any]:
        """Runs concurrent HTTP requests and summarizes results."""
        logger.info("=== Concurrent HTTP Requests ===")
        logger.info(f"Making {len(self.urls)} concurrent HTTP requests")
        start_time = time.time()
        try:
            greenlets = [
                gevent.spawn(self.fetch_url, url, i + 1)
                for i, url in enumerate(self.urls)
            ]
            gevent.joinall(greenlets, timeout=self.config.max_concurrent_timeout)
            end_time = time.time()

            successful_requests = [g.value for g in greenlets if g.value and g.value['success']]
            failed_requests = [g.value for g in greenlets if g.value and not g.value['success']]

            summary = {
                'successful': len(successful_requests),
                'failed': len(failed_requests),
                'total_time': end_time - start_time,
                'avg_response_time': (
                    sum(r['response_time'] for r in successful_requests) / len(successful_requests)
                    if successful_requests else 0.0
                )
            }
            logger.info(f"All requests done in {summary['total_time']:.2f}s")
            logger.info(f"Results: {summary['successful']} successful, {summary['failed']} failed")
            if successful_requests:
                logger.info(f"Average response time: {summary['avg_response_time']:.2f}s")
            return summary
        except Exception as e:
            logger.error(f"Concurrent requests failed: {e}")
            return {'successful': 0, 'failed': 0, 'total_time': 0.0, 'avg_response_time': 0.0}

class HttpSessionRequests:
    """Handles HTTP requests using a session for connection pooling."""
    def __init__(self, config: HttpClientConfig):
        self.config = config
        self.base_url = 'https://httpbin.org'
        self.endpoints_list = [
            ['json', 'headers', 'user-agent', 'ip'],
            ['uuid', 'base64/aGVsbG8gd29ybGQ=', 'delay/1'],
            ['status/200', 'status/201', 'status/202']
        ]

    def make_session_requests(self, session_id: int, endpoints: List[str]) -> List[Dict[str, Any]]:
        """Makes requests using a single session."""
        session = requests.Session()
        session.headers.update({
            'User-Agent': f'Gevent-Client-Session-{session_id}',
            'Accept': 'application/json'
        })
        results = []
        try:
            for i, endpoint in enumerate(endpoints):
                url = f"{self.base_url}/{endpoint}"
                start_time = time.time()
                logger.info(f"Session {session_id}: Request {i+1} to {endpoint}")
                try:
                    response = session.get(url, timeout=self.config.session_timeout)
                    end_time = time.time()
                    result = {
                        'session_id': session_id,
                        'request_num': i + 1,
                        'endpoint': endpoint,
                        'status_code': response.status_code,
                        'response_time': end_time - start_time,
                        'content_type': response.headers.get('content-type', 'unknown')
                    }
                    results.append(result)
                    logger.info(f"Session {session_id}: Request {i+1} done ({result['response_time']:.2f}s)")
                except Exception as e:
                    logger.info(f"Session {session_id}: Request {i+1} error - {e}")
                    results.append({
                        'session_id': session_id,
                        'request_num': i + 1,
                        'endpoint': endpoint,
                        'error': str(e)
                    })
                gevent.sleep(self.config.session_delay)
        finally:
            session.close()
        return results

    def run(self) -> List[Dict[str, Any]]:
        """Runs multiple sessions concurrently."""
        logger.info("=== HTTP Session with Connection Pooling ===")
        try:
            greenlets = [
                gevent.spawn(self.make_session_requests, i + 1, endpoints)
                for i, endpoints in enumerate(self.endpoints_list)
            ]
            gevent.joinall(greenlets)
            results = []
            for i, greenlet in enumerate(greenlets, 1):
                session_results = greenlet.value or []
                results.extend(session_results)
                if session_results:
                    success_count = sum(1 for r in session_results if r.get('status_code', 400) < 400)
                    avg_time = sum(r['response_time'] for r in session_results if 'response_time' in r) / len(session_results) if session_results else 0.0
                    logger.info(f"Session {i}: {success_count}/{len(session_results)} successful, avg time: {avg_time:.2f}s")
            return results
        except Exception as e:
            logger.error(f"Session requests failed: {e}")
            return []

class PostRequests:
    """Handles concurrent POST requests with JSON data."""
    def __init__(self, config: HttpClientConfig):
        self.config = config
        self.post_url = 'https://httpbin.org/post'
        self.test_data = [
            {'user_id': 1, 'action': 'login', 'timestamp': time.time(), 'metadata': {'client': 'gevent-test'}},
            {'user_id': 2, 'action': 'purchase', 'items': ['item1', 'item2'], 'total': 29.99},
            {'message': 'Hello from gevent!', 'priority': 'high', 'tags': ['test', 'concurrent']}
        ]

    def send_post(self, request_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Sends a POST request with JSON data."""
        try:
            logger.info(f"POST Request {request_id}: Sending data to {self.post_url}")
            start_time = time.time()
            response = requests.post(
                self.post_url,
                json=data,
                headers={'Content-Type': 'application/json'},
                timeout=self.config.default_timeout
            )
            end_time = time.time()
            try:
                response_data = response.json()
            except:
                response_data = {"raw_content": response.text[:100]}
            result = {
                'request_id': request_id,
                'status_code': response.status_code,
                'response_time': end_time - start_time,
                'response_data': response_data,
                'success': response.status_code < 400
            }
            logger.info(f"POST Request {request_id}: Response {result['status_code']} in {result['response_time']:.2f}s")
            return result
        except Exception as e:
            logger.info(f"POST Request {request_id}: Error - {e}")
            return {
                'request_id': request_id,
                'error': str(e),
                'success': False
            }

    def run(self) -> List[Dict[str, Any]]:
            """Runs concurrent POST requests."""
            logger.info("=== POST Requests Example ===")
            try:
                greenlets = [
                    gevent.spawn(self.send_post, i + 1, data)
                    for i, data in enumerate(self.test_data)
                ]
                gevent.joinall(greenlets)
                results = [g.value for g in greenlets if g.value is not None]
                logger.info("POST Request Results:")
                for result in results:
                    if result['success']:
                        logger.info(f"  Request {result['request_id']}: SUCCESS "
                                    f"(Status: {result['status_code']}, Time: {result['response_time']:.2f}s)")
                    else:
                        logger.info(f"  Request {result['request_id']}: FAILED")
                return results
            except Exception as e:
                logger.error(f"POST requests failed: {e}")
                return []

class ResilientHttpRequests:
    """Handles HTTP requests with retries and error handling."""
    def __init__(self, config: HttpClientConfig):
        self.config = config
        self.urls = [
            'https://httpbin.org/status/200',
            'https://httpbin.org/status/500',
            'https://httpbin.org/delay/3',
            'https://httpbin.org/status/404',
            'https://definitely-not-a-real-url.com'
        ]

    def resilient_request(self, url: str) -> Dict[str, Any]:
        """Makes an HTTP request with retry logic."""
        for attempt in range(self.config.max_retries):
            try:
                logger.info(f"Attempt {attempt + 1}/{self.config.max_retries} for {url}")
                start_time = time.time()
                response = requests.get(url, timeout=self.config.retry_timeout)
                end_time = time.time()
                if response.status_code < 400:
                    logger.info(f"Success on attempt {attempt + 1}: Status {response.status_code}")
                    return {
                        'success': True,
                        'status_code': response.status_code,
                        'response_time': end_time - start_time,
                        'attempts': attempt + 1,
                        'content_length': len(response.content),
                        'url': url
                    }
                else:
                    logger.info(f"HTTP error on attempt {attempt + 1}: Status {response.status_code}")
                    if attempt == self.config.max_retries - 1:
                        return {
                            'success': False,
                            'error': f'HTTP {response.status_code}',
                            'attempts': attempt + 1,
                            'url': url
                        }
            except requests.exceptions.Timeout:
                logger.info(f"Timeout on attempt {attempt + 1}")
                if attempt == self.config.max_retries - 1:
                    return {
                        'success': False,
                        'error': 'Timeout',
                        'attempts': attempt + 1,
                        'url': url
                    }
            except Exception as e:
                logger.info(f"Error on attempt {attempt + 1}: {e}")
                if attempt == self.config.max_retries - 1:
                    return {
                        'success': False,
                        'error': str(e),
                        'attempts': attempt + 1,
                        'url': url
                    }
            if attempt < self.config.max_retries - 1:
                wait_time = (2 ** attempt) * self.config.retry_base_delay
                logger.info(f"Waiting {wait_time}s before retry")
                gevent.sleep(wait_time)
        return {'success': False, 'error': 'Max retries exceeded', 'attempts': self.config.max_retries, 'url': url}

    def run(self) -> List[Dict[str, Any]]:
            """Runs resilient HTTP requests with retries."""
            logger.info("=== HTTP Error Handling and Retries ===")
            logger.info("Testing resilient HTTP requests")
            try:
                greenlets = [
                    gevent.spawn(self.resilient_request, url)
                    for url in self.urls
                ]
                gevent.joinall(greenlets, timeout=self.config.max_concurrent_timeout)
                results = [g.value for g in greenlets if g.value is not None]
                logger.info("Resilient Request Results:")
                for result in results:
                    if result['success']:
                        logger.info(f"  {result['url']}: SUCCESS after {result['attempts']} attempts "
                                    f"(Status: {result['status_code']})")
                    else:
                        logger.info(f"  {result['url']}: FAILED after {result['attempts']} attempts "
                                    f"(Error: {result['error']})")
                return results
            except Exception as e:
                logger.error(f"Resilient requests failed: {e}")
                return []

def main():
    """Runs all HTTP client examples."""
    config = HttpClientConfig()

    # Concurrent HTTP Requests
    concurrent_requests = ConcurrentHttpRequests(config)
    concurrent_summary = concurrent_requests.run()
    logger.info(f"Concurrent Requests summary: {concurrent_summary}\n" + "="*50 + "\n")

    # HTTP Session Requests
    session_requests = HttpSessionRequests(config)
    session_results = session_requests.run()
    logger.info(f"Session Requests results: {len(session_results)} requests processed\n" + "="*50 + "\n")

    # POST Requests
    post_requests = PostRequests(config)
    post_results = post_requests.run()
    logger.info(f"POST Requests results: {len(post_results)} requests processed\n" + "="*50 + "\n")

    # Resilient HTTP Requests
    resilient_requests = ResilientHttpRequests(config)
    resilient_results = resilient_requests.run()
    logger.info(f"Resilient Requests results: {len(resilient_results)} requests processed\n" + "="*50)

if __name__ == "__main__":
    main()
