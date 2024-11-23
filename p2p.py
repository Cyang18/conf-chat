import socket
import threading
import time

# Dictionary used to view and store peers' addresses
# so that hopefully the peers can find each other
peers = []

# Channel the user joins
current_channel = None

# Thread-safe storage for connected peers' sockets
peer_sockets = []
peer_lock = threading.Lock()

# Global password
chat_password = None
###################
# Function description:
# This function runs in a separate thread and listens for incoming messages
# on a connected peer socket. If the password is valid, it processes messages.
###################
def handle_incoming_messages(peer_socket):
    try:
        # Verify password
        received_password = peer_socket.recv(1024).decode()
        if received_password != chat_password:
            print("Peer failed password authentication. Disconnecting...")
            peer_socket.close()
            return

        # Notify successful connection
        peer_socket.send("AUTH_SUCCESS".encode())
        print("Peer authenticated successfully.")

        # Handle incoming messages
        while True:
            message = peer_socket.recv(1024).decode()
            if message:
                print(f"New message: {message}")
            else:
                print("Peer disconnected")
                break
    except Exception as e:
        print(f"Error receiving message: {e}")

    # Close the socket communication when an error occurs or communication ends
    with peer_lock:
        peer_sockets.remove(peer_socket)
    peer_socket.close()


###################
# Function description:
# Tries to connect to a peer at a specified address (hostname, port) with password validation.
###################
def connect_to_peer(peer_address, retries=3):
    for attempt in range(retries):
        try:
            peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peer_socket.connect(peer_address)

            # Send password for authentication
            peer_socket.send(chat_password.encode())
            auth_response = peer_socket.recv(1024).decode()
            if auth_response != "AUTH_SUCCESS":
                print("Peer rejected connection due to password mismatch.")
                peer_socket.close()
                return None

            print(f"Connected and authenticated with {peer_address}")
            with peer_lock:
                peer_sockets.append(peer_socket)
            threading.Thread(target=handle_incoming_messages, args=(peer_socket,), daemon=True).start()
            return peer_socket

        except ConnectionRefusedError:
            print(f"Connection to {peer_address} failed. Retrying... ({attempt + 1}/{retries})")
            time.sleep(3)
        except Exception as e:
            print(f"Unexpected error: {e}")
            break

    print(f"Failed to connect to {peer_address} after {retries} attempts.")
    return None

###################
# Function description:
# Listen for incoming connections and validate passwords.
###################
def listen_for_peers(port=1000):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Try to listen on the main port
    try:
        server.bind(('0.0.0.0', port))  # Listen on the given port
        server.listen(5)
    except OSError:
        # If the port is occupied, try the next port
        return listen_for_peers(port + 1)

    print(f"Listening for peers on port {port}...")

    while True:
        peer_socket, peer_address = server.accept()
        print(f"Connection attempt from {peer_address}")

        # Handle the connection in a separate thread
        threading.Thread(target=handle_incoming_messages, args=(peer_socket,), daemon=True).start()




###################
# Function Description:
# Sends the messages to the peers
###################
def send_message_to_peers(message):
    with peer_lock:
        for peer_socket in peer_sockets:
            try:
                peer_socket.send(message.encode())
            # In case of error, remove the peer socket from the list
            except Exception as e:
                print(f"Error sending message: {e}")
                peer_sockets.remove(peer_socket)
                peer_socket.close()


###################
###################
# Function description:
# Starts the chat system.
###################
def start_chat():
    global chat_password

    print("Set a password for this chat:")
    chat_password = input("Password: ").strip()

    print("Enter your username:")
    username = input().strip()

    print("Connecting to peers...")
    global peers
    for peer_address in peers:
        peer_socket = connect_to_peer(peer_address)
        if peer_socket:
            print(f"Connected to peer at {peer_address}")

    # If the peers are connected, begin communication
    while True:
        message = input(f"{username}: ")
        if message.lower() == 'exit':
            print(f"{username} has left the chat.")
            break

        # Add an option to rename
        if message.lower() == 'rename':
            print("Enter new username:")
            username = input().strip()
            continue

        send_message_to_peers(f"{username}: {message}\n")


###################
# Main function to start the chat application.
###################
def main():
    global peers

    # Use case testing two find other peers
    peers = [('localhost', 1001), ('localhost', 1002)]
    threading.Thread(target=listen_for_peers, daemon=True).start()
    time.sleep(2)
    start_chat()


if __name__ == "__main__":
    main()
