#!/usr/bin/env python3
from Node import Node

import EventManager

class Tree:
    def __init__(self) -> None:
        self.head = None
        self.tail = None
        self.name_heads = {}
        self.depth = 0

    def append_node(self, node):
        self.append(node.data, node.name)

    def append(self, data, name):
        
        self.depth += 1
        new_node = Node(data, name)
        #new_node.print()
        # base case
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            self.name_heads[name] = new_node
            EventManager.tree_head_event.set()
            return

        # if pattern head is none, set it to the first node with the pattern
        #if pattern in data and self.pattern_head is None:
            #self.pattern_head = new_node

        # If this is the first node with this name, add it to the name_heads list
        if not name in self.name_heads:
            self.name_heads[name] = new_node

        # last node with the same name
        last_same = None

        # going down until end
        current = self.head

        while current:
            if current.name == name:
                last_same = current
            current = current.next

        # sets to next node of same name
        # so book A to book A
        if last_same is not None:
            last_same.book_next = new_node

        self.tail.next = new_node
        self.tail = new_node
       

    # Print the whole tree, in order
    def print(self):
        next_node = self.head

        while next_node:
            print(f"Data: {next_node.data}, Name: {next_node.name}")
            next_node = next_node.next

    # Print the whole tree of a specific book name, in order
    def print_name(self, name):
        if not name in self.name_heads:
            return
        
        next_node = self.name_heads[name]

        while next_node:
            print(f"Data: {next_node.data}, Name: {next_node.name}")
            next_node = next_node.book_next

    # Write all lines of a book to file {name}.txt
    def write_book_to_file(self, name):
        if not name in self.name_heads:
            return
        
        current = self.name_heads[name]
        file_path = f"{name}.txt"
        with open(file_path, "w") as file:
            while current:
                # only add newline if there are more lines after this
                if current.book_next is not None:
                    file.write(str(current.data) + "\n")
                else:
                    file.write(str(current.data))
                current = current.book_next

    # Print all lines of a with a particular pattern
    def print_pattern(self):
        next_node = self.pattern_head

        while next_node:
            print(f"Data: {next_node.data}, Name: {next_node.name}")
            next_node = next_node.next_frequent_search
