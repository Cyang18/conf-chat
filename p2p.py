import socket
import threading
import time






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
