import threading
from socket import *
import time
import random

# Server configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5005

# List of paths to be requested by clients randomly
TEST_PATHS = [
    "/index.html",
    "/about.html",
    "/backend.html",
    "/doesnotexist.html",  # For testing 404 errors
]

# Individual client function
def client_thread(client_id):
    try:
        # Randomly select a path from TEST_PATHS
        path = random.choice(TEST_PATHS)
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect((SERVER_HOST, SERVER_PORT))

        # Construct an HTTP GET request
        request = f"GET {path} HTTP/1.1\r\nHost: {SERVER_HOST}\r\nConnection: close\r\n\r\n"
        client_socket.sendall(request.encode())

        # Receive the server's response
        response = b""
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            response += data

        # Print the client's request and the server's response header
        print(f"\n--- [Client {client_id}] Request to {path} ---")
        print(response.decode(errors="replace").split("\r\n\r\n")[0])  # Only display the response header

    except Exception as e:
        print(f"[Client {client_id}] Error: {e}")
    finally:
        client_socket.close()  # Close the socket connection

# Main function to run multiple clients concurrently
def run_multi_clients(client_count=10):
    threads = []
    for i in range(client_count):
        t = threading.Thread(target=client_thread, args=(i+1,))
        threads.append(t)
        t.start()
        time.sleep(0.1)  # Add a small delay between clients for natural simulation

    # Wait for all threads to complete
    for t in threads:
        t.join()

if __name__ == "__main__":
    run_multi_clients(client_count=10)  # You can adjust the number of clients here