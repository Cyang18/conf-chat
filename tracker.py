import socket
import threading
import time

# Dictionary to store the username and their corresponding peer socket
peer_usernames = {}
peer_lock = threading.Lock()

###################
# Function to handle incoming connections and manage peer names
###################
def handle_peer_connection(peer_socket):
    try:
        # Receive and register the peer's username
        username = peer_socket.recv(1024).decode()  # Receiving username
        print(f"Peer {username} has joined the chat.")
        
        # Store the peer's socket in the peer_usernames dictionary
        with peer_lock:
            peer_usernames[peer_socket] = username
        
        # Handle incoming messages (only for renames in this case)
        while True:
            message = peer_socket.recv(1024).decode()
            if message:
                # Check if the message is a rename request
                if message.lower().startswith("rename"):
                    new_username = message.split(" ", 1)[1]  
                    with peer_lock:
                        # Update the username in the dictionary
                        peer_usernames[peer_socket] = new_username
                    print(f"Peer {username} renamed to {new_username}.")
                    username = new_username  
            else:
                print(f"{username} disconnected.")
                break
    except Exception as e:
        print(f"Error handling peer: {e}")
    finally:
        with peer_lock:
            if peer_socket in peer_usernames:
                del peer_usernames[peer_socket]
        peer_socket.close()

###################
# Function to listen for new peer connections
###################
def listen_for_peers(port=1000):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind(('0.0.0.0', port))  # Bind to the port
        server.listen(5)
        print(f"Listening for peers on port {port}...")
    except OSError:
        return listen_for_peers(port + 1)

    while True:
        peer_socket, peer_address = server.accept()
        print(f"Connection attempt from {peer_address}")
        threading.Thread(target=handle_peer_connection, args=(peer_socket,), daemon=True).start()

###################
# Function to show the current list of peers
###################
def display_peers():
    with peer_lock:
        print("Current peers:")
        for peer_socket, username in peer_usernames.items():
            print(f"- {username} (Address: {peer_socket.getpeername()})")

###################
# Main function to start the peer management server
###################
def main():
    threading.Thread(target=listen_for_peers, daemon=True).start()

    while True:
        display_peers()
        time.sleep(10) 

if __name__ == "__main__":
    main()

