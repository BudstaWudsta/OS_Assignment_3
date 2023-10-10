

class node:
    def __init__(self, data, name):
        self.data = data  # data held
        self.name = name  # book A/B/C
        self.next = None  # next node in list
        self.next_same = None  # next node of same type as current
        pass


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
        while (last.next):
            if last.name == name:
                last_same = last
            last = last.next
        
        # sets to next node of same name 
        # so book A to book A
        last_same.next_same = new_node

        last.next = new_node
