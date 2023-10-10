

class node:
    def __init__(self,data,name):
        self.data = data # data held
        self.name = name # book A/B/C
        self.head = None # head/root of node
        self.next = None # next node in list
        self.next_same = None # next node of same type as current 
        pass
    
class tree:
    def __init__(self,head) -> None:
        self.head = head
        pass

    def append(self,data,name):
        new_node = node(data,name)
        
        if self.head is None:
            self.head = new_node
            return

        last = self.head
        while(last.next):
            last = last.next
        
        last.next = new_node