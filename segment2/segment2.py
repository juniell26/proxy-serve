import segment3
import time

class RateLimiter:
    def __init__(self, rate_limit):
        self.rate_limit = rate_limit
        self.last_request_time = 0

    def get_wait_time(self):
        # Calculate the time since the last request
        time_since_last_request = time.monotonic() - self.last_request_time

        # Calculate the minimum time between requests based on the rate limit
        min_time_between_requests = 1 / self.rate_limit

        # If the minimum time between requests hasn't elapsed, return the remaining time
        if time_since_last_request < min_time_between_requests:
            return min_time_between_requests - time_since_last_request

        # Otherwise, no wait time is needed
        return 0

    def wait(self):
        wait_time = self.get_wait_time()
        if wait_time > 0:
            time.sleep(wait_time)

        # Update the last request time
        self.last_request_time = time.monotonic()


def process_data(data):
    # Process the data received from the previous segment
    processed_data = data + " from segment 2"

    # Print a message indicating that the data has been processed successfully
    print("Segment 2 running...")
    #print("Data has been successfully processed!")
    
    return processed_data


# Create a rate limiter with a limit of 2 requests per second
limiter = RateLimiter(1000)

try:
    # Wait for the appropriate amount of time before processing the data
    limiter.wait()

    # Process the data
    data = "some data"
    processed_data = process_data(data)

except Exception as e:
    print("Error in Segment 2:", e)
