import queue
import threading
from flask import Flask, render_template

app = Flask(__name__)

# Create a queue to pass data between threads
data_queue = queue.Queue()

# Function to start the server in a separate thread
def run_server():
    from main import start_server
    start_server(8000, data_queue)

# Start the server in a separate thread
server_thread = threading.Thread(target=run_server)
server_thread.start()

@app.route('/')
def index():
    # Get the latest data from the queue
    try:
        data = data_queue.get_nowait()
    except queue.Empty:
        data = None
    return render_template('dashboard.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
