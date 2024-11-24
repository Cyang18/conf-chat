import socket
import threading
import time

# Dictionary to store the username and their corresponding peer socket
peer_usernames = {}

# Thread-safe storage for connected peers' sockets
peer_sockets = []
peer_lock = threading.Lock()

###################
# Function description:
# This function runs in a separate thread and listens for incoming messages
# on a connected peer socket.
###################
def handle_incoming_messages(peer_socket):
    try:
        # Receive and register the peer's username
        username = peer_socket.recv(1024).decode()  # Receiving username
        print(f"Peer {username} has joined the chat.")
        
        # Store the peer's socket in the peer_usernames dictionary
        with peer_lock:
            peer_usernames[peer_socket] = username
        
        # Handle incoming messages
        while True:
            message = peer_socket.recv(1024).decode()
            if message:
                print(f"{username}: {message}")
            else:
                print(f"{username} disconnected")
                break
    except Exception as e:
        print(f"Error receiving message: {e}")

    # Close the socket communication when an error occurs or communication ends
    with peer_lock:
        peer_sockets.remove(peer_socket)
    peer_socket.close()

###################
# Function description:
# Tries to connect to a peer at a specified address (hostname, port).
###################
def connect_to_peer(peer_address, username, retries=3):
    for attempt in range(retries):
        try:
            peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peer_socket.connect(peer_address)

            # Send username upon connection
            peer_socket.send(username.encode())
            print(f"Connected to {peer_address}")
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
# Listen for incoming connections
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
# Sends messages to all peers
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
# Function Description:
# Sends a private message to a specific peer
###################
def send_private_message(message, target_peer):
    try:
        target_peer.send(message.encode())
    except Exception as e:
        print(f"Error sending private message: {e}")

###################
# Function Description:
# Sends a private message to a specific peer (one-on-one)
###################
def send_private_message_to_peer(target_username, message):
    target_peer = None
    for peer_socket, peer_name in peer_usernames.items():
        if peer_name == target_username:
            target_peer = peer_socket
            break
    
    if target_peer:
        send_private_message(message, target_peer)
    else:
        print(f"Could not find peer with username {target_username}")

###################
# Starts the chat system
###################
def start_chat():
    
    print("Enter your username:")
    username = input().strip()

    print("Connecting to peers...")
    global peers
    for peer_address in peers:
        peer_socket = connect_to_peer(peer_address, username)
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

        # to message one-on-one with a peer
        elif message.lower().startswith('msg'):
            _, target_username, *msg_parts = message.split()
            private_message = " ".join(msg_parts)
            send_private_message_to_peer(target_username, private_message)
            continue
        
        send_message_to_peers(f"{username}: {message}\n")

###################
# Main function to start the chat application
###################
def main():
    global peers

    # Set peers for demonstration
    peers = [('localhost', 1000), ('localhost', 1001), ('localhost', 1002), ('localhost', 1003)]
    threading.Thread(target=listen_for_peers, daemon=True).start()
    time.sleep(2)
    start_chat()

if __name__ == "__main__":
    main()
