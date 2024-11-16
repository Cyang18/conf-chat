import socket
import threading
import time




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
# Function description:
# Connecting to the peers
###################
def start_chat():
    print("Enter your username:")
    username = input().strip()

    print("Connecting to peers...")
    global peers
    for peer_address in peers:
        peer_socket = connect_to_peer(peer_address)
        if peer_socket:
            #print(peer_address)
            print(f"Connected to peer at {peer_address}")

    # if the peers are connected begin the comm. with the peers
    while True:
        message = input(f"{username}: ")
        if message.lower() == 'exit':
            print(f"{username} has left the chat.")
            break

        # add a if statement here maybe to allow the user to change their name.
        if message.lower() == 'rename':
            break
        send_message_to_peers(f"{username}: {message}\n")

# main:
def main():

    global peers
    # use case testing find to other peers.
    peers = [('localhost', 1001), ('localhost', 1002)]
    threading.Thread(target=listen_for_peers, daemon=True).start()
    start_chat()


if __name__ == "__main__":
    main()
