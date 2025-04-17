from socket import *
import os
import threading

# Backend server configuration
BACKEND_PORT = 5006
BACKEND_FILES_DIR = "./static"  # Dedicated folder for backend files

# Function to handle backend requests
def handle_backend(conn, addr):
    try:
        # Receive the requested filename from the client
        filename = conn.recv(1024).decode()
        print(f"[Backend] Request: {filename} from {addr}")
        
        # Default to 'backend.html' if the request is for '/'
        if filename == '/':
            filename = '/backend.html'
        
        # Construct the file path by joining with BACKEND_FILES_DIR
        filepath = os.path.join(BACKEND_FILES_DIR, filename[1:])  # filename[1:] removes the leading '/'

        # Check if the file exists in the BACKEND_FILES_DIR directory
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                data = f.read()
            conn.sendall(data)  # Send the file content back to the client
        else:
            conn.send(b"<h1>404 Not Found (Backend)</h1>")  # File not found response
    except Exception as e:
        print(f"[Backend] Error: {e}")
        conn.send(b"<h1>500 Server Error (Backend)</h1>")  # Internal server error response
    finally:
        conn.close()  # Close the connection with the client

# Create and configure the server socket
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', BACKEND_PORT))  # Bind to all available interfaces on BACKEND_PORT
serverSocket.listen(5)  # Allow up to 5 queued connections
print(f"[Backend] Server running on port {BACKEND_PORT}")

# Main loop to accept incoming connections
while True:
    conn, addr = serverSocket.accept()  # Accept a new client connection
    threading.Thread(target=handle_backend, args=(conn, addr)).start()  # Handle each client in a separate thread