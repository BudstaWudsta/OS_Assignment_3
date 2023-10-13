import socket
from _thread import *
import threading
import sys

class node:
    def __init__(self, data, name):
        self.data = data  # data held
        self.name = name  # book A/B/C
        self.next = None  # next node in list
        self.next_same = None  # next node of same type as current
        self.pattern_next = None 
        self.depth=0
        pass
    
    def print(self):
        print(f"Data: {self.data}, Name: {self.name}")



class tree:
    def __init__(self, head,pattern) -> None:
        self.head = head
        self.name_heads = []
        self.pattern_head = None
        self.depth = 0
        if pattern in head.data:
            self.pattern_head = head
        self.name_heads.append(head)
        pass

    def append(self, data, name,pattern):
        self.depth+=1
        new_node = node(data, name)
        new_node.depth = self.depth

        # base case
        if self.head is None:
            self.head = new_node
            self.name_heads.append(new_node)
            return
        
        if self.pattern_head is None:
            if pattern in data:
                self.pattern_head = new_node
        
        found = False
        for i in self.name_heads:
            if i.name == name:
                found=True
                break
        if found==False:
            self.name_heads.append(new_node)

        # going down until end
        last = self.head
        last_same = None
        last_pattern = None
        while (last.next):
            if last.name == name:
                last_same = last
            if pattern in last.data:
                last_pattern = last
            last = last.next
        
        # sets to next node of same name 
        # so book A to book A
        if last_same is not None:
            last_same.next_same = new_node
        if last_pattern is not None:
            last_pattern.pattern_next = new_node

        last.next = new_node
    
    def print(self):
        next = self.head
        while(next):
            print(f"Data: {next.data}, Name: {next.name}, Depth: {next.depth}")
            next = next.next
            
    def print_name(self,name):
        next=None
        for i in self.name_heads:
            if i.name == name:
                next=i
        while(next):
            print(f"Data: {next.data}, Name: {next.name}, Depth: {next.depth}")
            next = next.next_same
    
    def print_pattern(self):
        next = self.pattern_head
        while(next):
            print(f"Data: {next.data}, Name: {next.name}, Depth: {next.depth}")
            next = next.pattern_next

def threaded(c):
    while True:
 
        # data received from client
        data = c.recv(1024)
        # assume recieve new data you replace the variabel
        # so store the data in an array for later
        if not data:
            print('Bye')
             
            # lock released on exit
            # print_lock.release()
            break
        if data:
            lock.acquire()
            
            print("got somth")
            # reverse the given string from client
            data = data[::-1]
    
            # send back reversed string to client
            c.send(data)
            
            lock.release()
 
        
 
    # connection closed
    c.close()

lock = threading.Lock()

if __name__ == "__main__":
    pattern = "Hello"
    t1 = node("Hello world","A")
    test = tree(t1,pattern)
    test.append("Hey world","B",pattern)
    test.append("How are you","A",pattern)
    test.append("Hello there","A",pattern)
    # test.print()
    test.print_name("A")
    # test.print_pattern()
    
    # test.head.next_same.print() 
    
    exit()
    
    host = ""
 
    # reserve a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)
 
    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")
 
    # a forever loop until client wants to exit
    while True:
 
        # establish connection with client
        c, addr = s.accept()
 
        # lock acquired by client
        print('Connected to :', addr[0], ':', addr[1])
 
        # Start a new thread and return its identifier
        start_new_thread(threaded, (c,))
    s.close()