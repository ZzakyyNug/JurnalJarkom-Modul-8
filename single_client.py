from socket import *

# Server configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5005

# Function to send an HTTP GET request to the server
def send_request(path="/index.html"):
    try:
        # Create a socket connection to the Web Server + Proxy
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

        print("\n--- Response from Server ---\n")
        print(response.decode(errors="replace"))  # Decode the response safely, handling non-text characters

    except Exception as e:
        print(f"Client error: {e}")
    finally:
        client_socket.close()  # Close the socket connection

if __name__ == "__main__":
    # Modify the path here according to the file you want to request or proxy
    send_request("/backend.html")