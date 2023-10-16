from Node import Node


class Tree:
    def __init__(self) -> None:
        self.head = None
        self.tail = None
        self.name_heads = []
        self.pattern_head = None
        self.depth = 0

    # Append a new node to the tree
    def append(self, data, name, pattern):
        self.depth += 1
        new_node = Node(data, name)

        # base case
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            self.name_heads.append(new_node)
            return

        # if pattern head is none, set it to the first node with the pattern
        if pattern in data and self.pattern_head is None:
            self.pattern_head = new_node

        # If this is the first node with this name, add it to the name_heads list
        if not any(node.name == name for node in self.name_heads):
            self.name_heads.append(new_node)

        # last node with the same name
        last_same = None

        # last node with the same pattern
        last_pattern = None

        # going down until end
        current = self.head

        while current:
            if current.name == name:
                last_same = current
            if pattern in current.data:
                last_pattern = current
            current = current.next

        # sets to next node of same name
        # so book A to book A
        if last_same is not None:
            last_same.book_next = new_node
        if last_pattern is not None:
            last_pattern.next_frequent_search = new_node

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
        next_node = next((node for node in self.name_heads if node.name == name), None)

        while next_node:
            print(f"Data: {next_node.data}, Name: {next_node.name}")
            next_node = next_node.book_next

    def print_pattern(self):
        next_node = self.pattern_head

        while next_node:
            print(f"Data: {next_node.data}, Name: {next_node.name}")
            next_node = next_node.next_frequent_search
