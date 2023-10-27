#!/usr/bin/env python3
class Node:
    def __init__(self, data, name):
        self.data = data  # data held
        self.name = name  # book A/B/C
        self.next = None  # next node in list
        self.book_next = None  # next node of same book as current
        self.next_frequent_search = None # for part 2 analysis
        self.book_num = None
        temp = name.replace("book_","")
        temp = temp.replace(".txt","")
        self.book_num = int(temp)

    def print(self):
        print(f"Data: {self.data}, Name: {self.name}")
    
    def getInfo(self):
        return f"Data: {self.data}, Name: {self.name}"
    