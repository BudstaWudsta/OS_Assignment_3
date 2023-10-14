from Node import Node

class Tree:
    def __init__(self) -> None:
        self.head = None
        self.name_heads = []
        self.pattern_head = None
        self.depth = 0

    def append(self, data, name, pattern):
        self.depth += 1
        print(f"creating new node with name {name}, {data}")
        new_node = Node(data, name)

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
                found = True
                break
        if found == False:
            self.name_heads.append(new_node)

        # going down until end
        last = self.head

        last_same = None
        last_pattern = None
        if last.name == name:
            last_same = last

        if pattern in last.data:
            last_pattern = last

        while last.next:
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
            last_same.book_next = new_node
        if last_pattern is not None:
            last_pattern.next_frequent_search = new_node

        last.next = new_node

    def print(self):
        next = self.head
        print (f"depth {self.depth}")
        while next:
            print(f"Data: {next.data}, Name: {next.name}")
            next = next.next

    def print_name(self, name):
        next = None
        for i in self.name_heads:
            if i.name == name:
                next = i
        while next:
            print(f"Data: {next.data}, Name: {next.name}")
            next = next.next_same

    def print_pattern(self):
        next = self.pattern_head
        while next:
            print(f"Data: {next.data}, Name: {next.name}")
            next = next.next_frequent_search
