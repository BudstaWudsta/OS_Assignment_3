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
        pass
    
    def print(self):
        print(f"Data: {self.data}, Name: {self.name}")



class tree:
    def __init__(self, head) -> None:
        self.head = head
        pass

    def append(self, data, name):
        new_node = node(data, name)

        # base case
        if self.head is None:
            self.head = new_node
            return

        # going down until end
        last = self.head
        last_same = None
        while (last.next):
            if last.name == name:
                last_same = last
            last = last.next
        
        # sets to next node of same name 
        # so book A to book A
        if last_same is not None:
            last_same.next_same = new_node

        last.next = new_node
    
    def print(self):
        next = self.head
        while(next):
            print(f"Data: {next.data}, Name: {next.name}")
            next = next.next

if __name__ == "__main__":
    # t1 = node(1,"book A")
    # test = tree(t1)
    # test.append(2,"book B")
    # test.append(3,"book A")
    # # test.print()
    
    # test.head.next_same.print() 
    
    for line in sys.stdin:
        print(line)