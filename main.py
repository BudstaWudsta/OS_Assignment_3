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



class Tree:
    def __init__(self) -> None:
        
        self.head = None
        self.name_heads = []
        self.pattern_head = None
        self.depth = 0

        pass

    def append(self, data, name,pattern):
        # increase depth by 1
        self.depth+=1
        
        new_node = node(data, name)
        
        # set node depth
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
        if last.name == name:
            last_same = last
            
        if pattern in last.data:
            last_pattern = last
            
        while (last.next):
            # print(f"{last.name} {name}")
            if last.name == name:
                last_same = last
            if pattern in last.data:
                last_pattern = last
            last = last.next
        
        if last.name == name:
            last_same = last
            
        if pattern in last.data:
            last_pattern = last
        
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

def main(c, tree, name,pattern):
    lines = []
    
    while True:
 
        # data received from client
        data = c.recv(1024)

        if not data:
            # print('Disconnected')
            print(f"{name}")
            c.send(name.encode())
            tree.print_pattern()
            
            break
        
        else:
            
            # removing extra charaacters
            data = str(data)
            data = data[2:]
            data = data[:-1]
                    
            # spliting input based on new lines
            data = data.split('\\n')
        
            for d in data:
                # if d != '':
                lines.append(d)
                
            # print(lines)
            
            while(lines):
                lock.acquire()
                                
                thing = lines.pop(0)
                # thing += "\n"
                thing_str = thing
                # send back data to client
                thing = thing.encode()
                                
                tree.append(thing_str, name, pattern)
                
                # try:
                #     c.send(thing)
                # except:
                #     print("send error")
                
                lock.release()
            if lines is None:
                c.close()
 
        
 
    # connection closed
    c.close()

lock = threading.Lock()

if __name__ == "__main__":
    # p = "Hello"
    
    # tree = Tree()
    
    # tree.append("Hello world","A",p)
    # tree.append("Hey world","A",p)
    # tree.append("Hi world", "B", p)
    # tree.append("Hello world", "B", p)
    # tree.append("Hello world","A",p)
        
    # tree.print()
    # tree.print_name("B")
    # tree.print_pattern()
    
    # exit()
    
    tree = Tree()
    
    connections = 1
    
    host = ""
 
    port = 1234
    
    # input here    
    port = int(sys.argv[2])
    
    pattern = sys.argv[4]
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("binded to ", port)
 
    s.listen(5)
    print("listening")
 
    # a forever loop until client wants to exit
    while True:
 
        # establish connection with client
        c, addr = s.accept()
 
        # lock acquired by client
        print('Connected to :', addr[0], ':', addr[1])
 
        # Start a new thread and return its identifier
        name = f"book_{connections:02d}.txt"
        connections+=1
        start_new_thread(main, (c,tree,name,pattern))
    s.close()