#!/usr/bin/env python3

import socket
import select
from _thread import *
import threading
import sys
import argparse
import EventManager
from Tree import Tree
import time

#
tree_write_lock = threading.Lock()
analysis_lock = threading.Lock()

tree_head_event = threading.Event()

analysis_condition = threading.Condition()
current_thread_turn = 1


def analysis_thread(threadnumber, waittime, tree, pattern):
    global current_thread_turn
    EventManager.tree_head_event.wait()
    pattern_tree = Tree()
    current_node = tree.head

    while True:
        with analysis_condition:
            # Wait for the condition that it's this thread's turn
            while current_thread_turn != threadnumber:
                analysis_condition.wait()

            print(f"Running Analysis Thread: {threadnumber}")

            # append all 'new' nodes to linked list
            while current_node is not None:
                if pattern in current_node.data and current_node != pattern_tree.tail:
                    pattern_tree.append_node(current_node)

                if current_node.next is None:
                    break
                current_node = current_node.next

            # To record book titles and frequency of pattern occurence 
            frequency_count = {}

            # Iterate through tree to count occurrences of pattern
            current = pattern_tree.head
            while current is not None:
                if not current.name in frequency_count:
                    frequency_count[current.name] = 0
                frequency_count[current.name] += 1
                current = current.next

            # Sort in descending order by frequency of pattern occurrence
            sorted_items = sorted(frequency_count.items(), key=lambda item: item[1], reverse=True)

            print (f"Books ordered by the occurence of \"{pattern}\":")
            for key, value in sorted_items:
                print(f"{key}: {value}")

            # Once this thread is finished, switch turns and notify the other thread
            current_thread_turn = 2 if threadnumber == 1 else 1

            # Wake up all threads waiting on this condition
            analysis_condition.notify_all()
            
            # wait for x seconds
            time.sleep(waittime)


def handle_client(client_socket, tree, name, pattern):

    data = ""

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
                    with tree_write_lock:
                        line = data.pop(0)
                        tree.append(line, name)

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
    parser.add_argument("-l", "--listenport", default=12345,
                        help="port to listen on", type=int)
    parser.add_argument("-p", "--pattern",
                        help="pattern to search for", type=str)
    args = parser.parse_args()
    port = args.listenport
    pattern = args.pattern

    # Create IPv4 TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Allow instant reconnect (by default, TCP enforces a timeout on reconnect so the socket can't be reused immediately)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((host, port))

    server_socket.listen(5)

    analysis1 = threading.Thread(
        target=analysis_thread, args=(1, 2, tree, pattern)
    )
    analysis2 = threading.Thread(
        target=analysis_thread, args=(2, 2, tree, pattern)
    )

    analysis1.start()
    analysis2.start()

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
