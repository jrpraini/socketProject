import socket
import tkinter as tk
from tkinter import scrolledtext

# Function to send commands to the tracker
def send_command():
    command = command_entry.get()  # Get the input command
    if command:
        tracker_ip = '127.0.0.1'  # Assuming tracker is local
        tracker_port = 5000  # Tracker listening port

        try:
            # Open socket connection to the tracker
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((tracker_ip, tracker_port))
            client.send(command.encode('utf-8'))

            # Receive response from the tracker
            response = client.recv(1024).decode('utf-8')
            display_response(f"Response: {response}")
            client.close()

        except Exception as e:
            display_response(f"Error: {str(e)}")
    else:
        display_response("No command entered.")

# Function to display the response in the UI
def display_response(message):
    response_text.config(state=tk.NORMAL)
    response_text.insert(tk.END, message + "\n")
    response_text.config(state=tk.DISABLED)

# Tkinter UI setup
window = tk.Tk()
window.title("Six card golf")

# Label for Command Input
command_label = tk.Label(window, text="Enter Command:")
command_label.pack()

# Entry widget to input the command
command_entry = tk.Entry(window, width=50)
command_entry.pack()

# Button to send the command
send_button = tk.Button(window, text="Enter", command=send_command)
send_button.pack()

# Scrolled Text widget to display the tracker responses
response_text = scrolledtext.ScrolledText(window, width=60, height=30, state=tk.DISABLED)
response_text.pack()

# Start the UI loop
window.mainloop()
