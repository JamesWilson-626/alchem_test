import random
import time
from datetime import datetime
import requests
import logging
from typing import Dict

class OrderProcessor:
    def __init__(self):
        self.api_url = "http://127.0.0.1:8000/logs/"
        self.logger = logging.getLogger(__name__)

    def _send_log(self, source: str, message: str) -> None:
        """Send log data to the API endpoint."""
        log_data = {
            "source": source,
            "log": message,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        try:
            response = requests.post(self.api_url, json=log_data)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to send log: {str(e)}")

    def process_order(self, order_id: int) -> None:
        """Simulate processing an order with success and failure scenarios."""
        try:
            # Simulate processing time
            processing_time = random.uniform(0.5, 2.0)
            time.sleep(processing_time)

            # Randomly simulate a failure
            if random.random() < 0.2:  # 20% chance of failure
                raise Exception("Payment processing failed")

            # Log successful order processing
            self._send_log(
                source="OrderProcessor",
                message=f"Order {order_id} processed successfully in {processing_time:.2f}s"
            )

        except Exception as e:
            # Log error in order processing
            self._send_log(
                source="OrderProcessor",
                message=f"ERROR: Failed to process order {order_id}: {str(e)}"
            )

class UserAuthenticator:
    def __init__(self):
        self.api_url = "http://127.0.0.1:8000/logs/"
        self.logger = logging.getLogger(__name__)

    def _send_log(self, source: str, message: str) -> None:
        """Send log data to the API endpoint."""
        log_data = {
            "source": source,
            "log": message,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        try:
            response = requests.post(self.api_url, json=log_data)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to send log: {str(e)}")

    def authenticate_user(self, user_id: str) -> bool:
        """Simulate user authentication process."""
        try:
            # Simulate authentication delay
            auth_time = random.uniform(0.1, 0.5)
            time.sleep(auth_time)

            # Simulate authentication success/failure
            is_authenticated = random.random() > 0.1  # 90% success rate

            self._send_log(
                source="UserAuthenticator",
                message=f"User {user_id} authentication {'successful' if is_authenticated else 'failed'} (time: {auth_time:.2f}s)"
            )

            return is_authenticated

        except Exception as e:
            self._send_log(
                source="UserAuthenticator",
                message=f"ERROR: Authentication system error for user {user_id}: {str(e)}"
            )
            return False

def run_simulator(duration_seconds: int = 60):
    """Run the simulator for a specified duration."""
    order_processor = OrderProcessor()
    user_authenticator = UserAuthenticator()
    
    start_time = time.time()
    order_id = 1000
    
    print(f"Starting simulator for {duration_seconds} seconds...")
    
    while time.time() - start_time < duration_seconds:
        # Simulate user authentication
        user_id = f"user_{random.randint(1, 100)}"
        user_authenticator.authenticate_user(user_id)
        
        # Simulate order processing
        order_processor.process_order(order_id)
        order_id += 1
        
        # Random delay between events
        time.sleep(random.uniform(0.5, 2.0))
    
    print("Simulator finished.")

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Run simulator for 30 sec by default
    run_simulator(30)