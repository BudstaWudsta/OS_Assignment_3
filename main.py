import socket
import select
from _thread import *
import threading
import sys
import argparse
from Tree import Tree
import time

lock = threading.Lock()

def analysis(tree):      
    while (tree.pattern_head is None):
        continue
    
    next = tree.pattern_head
    
    while(True):
        tree.frequency[next.book_num-1] += 1
        
        if tree.frequency[next.book_num-1] > tree.most_freq_count:
            tree.most_freq_count = tree.frequency[next.book_num-1]
            tree.most_freq_name = next.name
        
        while next.next_frequent_search is None:
            continue
        
        next = next.next_frequent_search
    return

def interval_write(tree,interval):
    while(True):
        time.sleep(interval)
        print(f"Most Freq: {tree.most_freq_name}")
    return

def handle_client(client_socket, tree, name, pattern):
    lines = []
    data = ""

    while True:
        # data received from client
        if client_socket._closed:
            break
        # checking if there is still data to be read
        readable, _, _ = select.select([client_socket], [], [], 1)

        if client_socket in readable:
            # recieving data
            data = client_socket.recv(1024)

            # removing extra charaacters
            data = str(data)
            data = data[2:]
            data = data[:-1]

            # spliting input based on new lines
            data = data.split("\\n")

            for d in data:
                lines.append(d)

            
            while lines:
                with lock:
                    line = lines.pop(0)
                    tree.append(line, name, pattern)

        else:
            # connection closed
            print(f"Closing client: {name}")
            client_socket.close()
            break


if __name__ == "__main__":
    tree = Tree()
    
    threading.Thread(target=analysis,args=tree).start()
    threading.Thread(target=interval_write,args=(tree,5)).start()

    connections = 0

    host = ""

    port = 1234

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--listenport", help="port to listen on", type=int)
    parser.add_argument("-p", "--pattern", help="pattern to search for", type=str)
    args = parser.parse_args()
    print(f"listen: {args.listenport}")
    print(f"pattern: {args.pattern}")
    port = args.listenport
    pattern = args.pattern

    # Create IPv4 TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Allow instant reconnect (by default, TCP enforces a timeout on reconnect so the socket can't be reused immediately)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((host, port))
    print(f"binded to {host}:{port}")

    server_socket.listen(5)
    print("listening")

    # a forever loop until client wants to exit
    while connections < 10:
        # Blocking function to wait for new connection
        client_socket, address = server_socket.accept()

        # lock acquired by client
        print("Connected to :", address[0], ":", address[1])

        # Start a new thread and return its identifier
        setname = f"book_{connections:02d}.txt"
        connections += 1

        t = threading.Thread(
            target=handle_client, args=(client_socket, tree, setname, pattern)
        )
        t.start()

    # wait for all threads to finish
    main_thread = threading.current_thread()
    for t in threading.enumerate():
        if t is not main_thread:
            t.join()

    tree.print()
