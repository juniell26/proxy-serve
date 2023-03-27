import segment4

class MaxClientsReached(Exception):
    pass

def process_data(data, client_counter):
    try:
        # Increment the client counter
        client_counter += 1

        # Check if the maximum number of clients has been reached
        if client_counter > 1000:
            raise MaxClientsReached("Maximum number of clients reached")

        # Process the data received from the previous segment
        processed_data = data + " from segment 3"

        # Print a message indicating that the segment is running
        print("Segment 3 running...")

        return processed_data, client_counter

    except MaxClientsReached as e:
        print("Error in Segment 3:", e)
        # Raise the exception to the previous segment
        raise e
    except Exception as e:
        print("Error in Segment 3:", e)
