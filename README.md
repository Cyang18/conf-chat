# Peer-to-Peer Chat Application

## Overview
This is a simple peer-to-peer chat application implemented using Python's `socket` and `threading` modules. It allows users to connect to multiple peers, send public messages, and send private messages to specific users. The application features multi-threaded communication to handle incoming messages and connections simultaneously.

## Features
- **Send Messages to All Peers:** Broadcast messages to all connected peers.
- **Private Messaging:** Send private messages to specific users.
   - By using 'msg'
   ```Example:
   msg 'username' 'message'
   ```
- **Dynamic Usernames:** Users can choose or rename their usernames at any time.
   - By using 'rename'
   ```Example
   rename
   Brian
   ```
- **Peer Tracker:** A separate tracker script (`tracker.py`) keeps track of connected peers and their usernames.

## Architecture

### Peer-to-Peer Architecture

This chat application uses a **decentralized peer-to-peer (P2P) architecture**, where each peer functions both as a client and a server. Key characteristics of the architecture include:

- **No Central Server:** Peers connect directly to each other without a central server, forming a decentralized network.
- **Multi-threaded Communication:** Each peer handles incoming and outgoing messages in separate threads, ensuring non-blocking communication.
- **Message Broadcasting and Private Messaging:** Messages can be broadcast to all peers or sent privately to a specific peer by username.
- **Peer Management (Tracker):** The `tracker.py` script tracks connected peers, displaying their usernames and IP addresses.

## Workflow

1. **Peer Setup:**
   - When the application starts, it attempts to connect to the specified peers defined in the `peers` list. If a connection is successful, it sends the username to the peer.
   
2. **Listening for Peers:**
   - The server thread continuously listens for incoming connections from other peers on specified ports. Once a connection is accepted, a new thread is spawned to handle incoming messages from the peer.

3. **Messaging:**
   - Users can send messages to all connected peers or direct messages to specific peers. Messages are sent over the peer sockets and broadcasted or delivered privately based on the type of message.

4. **Peer Tracking:**
   - **tracker.py** listens for incoming connections on a specified port, accepts connections, and registers the peers by their usernames.
   - It can display the list of connected peers at regular intervals.

## Requirements

- Python 3.9.18 (or higher)

## Setup

1. **Clone the repository:**
   ```bash
   [git clone https://github.com/yourusername/p2p-chat.git](https://github.com/Cyang18/conf-chat.git)
   cd p2p-chat
   ```

2. **Run the Tracker:**
   To keep track of the connected peers, you need to run `tracker.py` in a separate terminal:
   ```bash
   python tracker.py
   ```
   This script will listen for incoming connections on a specified port and display the usernames and addresses of connected peers.

3. **Run the Chat Application:**
   To start the chat application, run the following command on the terminal:
   ```bash
   python p2p.py
   ```
   Note: To create multiple peers, create mutlple instances on the terminal.
   
5. **Configuration:**
   - You can modify the `peers` list in the `main()` function of `p2p.py` to include other peer addresses and ports for connecting to additional peers.

## Developed by
- Chris Yang
- Jedidiah Pollard
