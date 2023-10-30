#!/usr/bin/env python3
class Node:
    def __init__(self, data, name):
        self.data = data  # data held
        self.name = name  # book A/B/C
        self.next = None  # next node in list
        self.book_next = None  # next node of same book as current
        self.next_frequent_search = None # for part 2 analysis

    def print(self):
        print(f"Data: {self.data}, Name: {self.name}")
