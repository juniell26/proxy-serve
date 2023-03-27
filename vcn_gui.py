import tkinter as tk
import main

class Dashboard(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Create a label to display the example data
        self.data_label = tk.Label(self, text="Example Data:")
        self.data_label.pack()

        # Create a frame to contain the list of data
        self.data_frame = tk.Frame(self)
        self.data_frame.pack()

        # Create a list of example data
        example_data = ["Data 1", "Data 2", "Data 3, Data 4, Data 5, Data 6, Data 7, Data 8, Data 9, Data 10"]

        # Create a label for each data item and add it to the frame
        for data_item in example_data:
            label = tk.Label(self.data_frame, text=data_item)
            label.pack(side="top", fill="both", expand=True)

        # Create a button to process the data
        self.process_button = tk.Button(self, text="Process Data", command=self.process_data)
        self.process_button.pack()

        # Create a text box to display the response
        self.response_text = tk.Text(self)
        self.response_text.pack()

        # Create a button to send a request to the proxy server
        self.send_button = tk.Button(self, text="Send Request", command=self.send_request)
        self.send_button.pack()

    def process_data(self):
        self.data_label.config(text="Example Data: Hello World")

    def send_request(self):
        # Send a request to the proxy server and display the response in the text box
        response = main.send_request()
        self.response_text.delete('1.0', tk.END)
        self.response_text.insert(tk.END, response)


if __name__ == "__main__":
    # Create a Tkinter window and set its properties
    root = tk.Tk()
    root.title("Dashboard")
    root.geometry("400x300")

    # Create the dashboard and run the Tkinter event loop
    dashboard = Dashboard(master=root)
    dashboard.mainloop()
