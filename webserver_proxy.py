from socket import *
import threading
import os
import mimetypes

# Configuration
PROXY_HOST = 'localhost'
PROXY_PORT = 5005
BACKEND_HOST = 'localhost'
BACKEND_PORT = 5006
CACHE_DIR = './cache'

# Create cache directory if it does not exist
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

# Cache tracker
cache_tracker = {}

# Function to retrieve Content-Type of a file
def get_content_type(filename):
    content_type, _ = mimetypes.guess_type(filename)
    return content_type or "application/octet-stream"

# Function to fetch a file from the backend if it is not available in the proxy
def fetch_from_backend(filename):
    try:
        backend_socket = socket(AF_INET, SOCK_STREAM)
        backend_socket.connect((BACKEND_HOST, BACKEND_PORT))
        print(f"[Proxy] Forwarding '{filename}' to backend server...")

        backend_socket.send(filename.encode())

        response = b""
        while True:
            chunk = backend_socket.recv(4096)
            if not chunk:
                break
            response += chunk

        backend_socket.close()
        return response
    except Exception as e:
        print("[Proxy] Error fetching from backend:", e)
        return b"<h1>500 Internal Server Error (from backend)</h1>"

# Function to handle each client connection
def handle_client(connectionSocket, addr):
    print(f"[Proxy] Connection received from {addr}")

    try:
        # Fill in start (baris 52)
        request = connectionSocket.recv(2048).decode()
        # Fill in end (baris 54)
        if not request:
            print("[Proxy] No request received.")
            return

        print("[Proxy] Client request:\n", request)

        # Parse filename from HTTP request
        request_line = request.splitlines()[0]
        parts = request_line.split()
        if len(parts) < 2:
            connectionSocket.sendall(b"HTTP/1.1 400 Bad Request\r\n\r\n")
            return

        filename = parts[1]
        if filename == '/':
            filename = '/index.html'
        filepath = filename[1:]  # Remove leading "/"

        # Check if the file exists in the cache
        if filename in cache_tracker and os.path.exists(cache_tracker[filename]):
            print(f"[Proxy] Cache HIT for {filename}")
            with open(cache_tracker[filename], 'rb') as f:
                content = f.read()
        elif os.path.exists(filepath):
            print(f"[Proxy] File found locally: {filepath}")
            with open(filepath, 'rb') as f:
                content = f.read()

            # Save to cache
            cache_path = os.path.join(CACHE_DIR, os.path.basename(filepath))
            with open(cache_path, 'wb') as cache_file:
                cache_file.write(content)
            cache_tracker[filename] = cache_path
        else:
            print(f"[Proxy] File NOT found locally, forwarding to backend.")
            content = fetch_from_backend(filename)

        # Determine Content-Type
        content_type = get_content_type(filename)
        header = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\n\r\n"
        connectionSocket.sendall(header.encode() + content)

    except Exception as e:
        print(f"[Proxy] An error occurred while processing the request: {e}")
        error_message = b"HTTP/1.1 500 Internal Server Error\r\n\r\n<h1>500 Internal Server Error</h1>"
        # Fill in start (baris 96)
        connectionSocket.sendall(error_message)
        # Fill in end
    finally:
        connectionSocket.close()
        print(f"[Proxy] Connection from {addr} closed.\n")

# Set up socket to accept client connections
# Fill in start (baris 100)
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((PROXY_HOST, PROXY_PORT))
serverSocket.listen(5)
# Fill in end
print(f"[Proxy] Server running on {PROXY_HOST}:{PROXY_PORT}")

# Main loop
try:
    while True:
        # Fill in start (baris 102)
        clientSocket, clientAddress = serverSocket.accept()
        # Fill in end

        # Fill in start (baris 118)
        client_thread = threading.Thread(target=handle_client, args=(clientSocket, clientAddress))
        # Fill in end

        # Fill in start (baris 121)
        client_thread.start()
        # Fill in end
except KeyboardInterrupt:
    print("\n[Proxy] Server manually shut down.")
finally:
    serverSocket.close()
