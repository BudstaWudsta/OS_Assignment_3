import subprocess
import signal
import sys
import queue
import threading

# create a new queue object
data_queue = queue.Queue()

# signal handler for SIGINT signal (Ctrl+C)
def signal_handler(signal, frame):
    # terminate the subprocesses
    for process in processes:
        if process.poll() is None:
            process.terminate()
    sys.exit(0)

# function to start the nc command in a separate thread
def start_nc(hostname, port):
    # start the nc command
    process = subprocess.Popen(["nc", hostname, str(port)], stdin=subprocess.PIPE)

    # read data from the queue and send it to the nc command
    while True:
        try:
            data = data_queue.get(timeout=1)
            process.stdin.write(data)
            process.stdin.flush()
        except queue.Empty:
            if process.poll() is not None:
                break

    # close the stdin pipe and wait for the process to exit
    process.stdin.close()
    process.wait()

# main
if __name__ == "__main__":
    connections = [("localhost", 1024, "input_1.txt"), ("localhost", 1024,"input_2.txt"), ("localhost", 1024, "input_3.txt")]

    # list to store references to the subprocesses
    processes = []

    # list to store references to the threads
    threads = []

    # loop over each hostname and port combination
    for hostname, port, text in connections:
        print(f"Connecting to {hostname}:{port}")
        # start a new thread to run the nc command
        t = threading.Thread(target=start_nc, args=(hostname, port))
        t.start()
        # add the thread to the list of threads
        threads.append(t)

    # send data to the server using the queue
    for _, _, text in connections:
        with open(text, "rb") as f:
            data = f.read()
            data_queue.put(data)

    # wait for the threads to exit
    for t in threads:
        t.join()

    # set up signal handler for SIGINT signal (Ctrl+C)
    signal.signal(signal.SIGINT, signal_handler)