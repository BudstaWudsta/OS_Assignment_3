#!/usr/bin/env python3

import socket
import select
from _thread import *
import threading
import sys
import argparse
from Tree import Tree
import time

lock = threading.Lock()


def handle_client(client_socket, tree, name, pattern):

    data = ""
    print(f"startinc connection w {name}")
    # Check if there is a file created (in case of blank book)
    created_before = False
 
    while True:
        # data received from client
        if client_socket._closed:
            break
        # checking if there is still data to be read
        readable, _, _ = select.select([client_socket], [], [], 1)
        
        blankdata = False

        if client_socket in readable:
            data = client_socket.recv(1024)

            # if data isnt blank
            if data != b"":
                # removing extra charaacters
                data = str(data)[2:-1]

                # spliting input based on new lines
                data = data.split("\\n")
                
                while data:
                    with lock:
                        line = data.pop(0)
                        tree.append(line, name, pattern)

                created_before = True
            else:
                blankdata = True

        if (client_socket not in readable) or blankdata:
            if not created_before:
                tree.append("", name, pattern)
            client_socket.close()
            break

    # Finished reading in data, now can write to file
    tree.write_book_to_file(name)

if __name__ == "__main__":
    tree = Tree()

    connections = 0

    host = "0.0.0.0"

    port = 12345

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--listenport", default=12345, help="port to listen on", type=int)
    parser.add_argument("-p", "--pattern", help="pattern to search for", type=str)
    args = parser.parse_args()
    port = args.listenport
    pattern = args.pattern 
    
    # Create IPv4 TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Allow instant reconnect (by default, TCP enforces a timeout on reconnect so the socket can't be reused immediately)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((host, port))

    server_socket.listen(5)

    # a forever loop until client wants to exit
    while True:
        # Blocking function to wait for new connection
        client_socket, address = server_socket.accept()

        # Start a new thread and return its identifier
        name = "book_{:02d}".format(connections + 1)
        connections += 1

        t = threading.Thread(
            target=handle_client, args=(client_socket, tree, name, pattern)
        )
        t.start()
