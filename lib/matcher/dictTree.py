import re

class Node:
    def __init__(self, lines=[]):
        self.lines = lines
        self.children = {}

class DictTree:
    def __init__(self):
        self.root = Node()
    
    def insert(self, token, line):
        p = self.root
            
        for c in token:
            if not p.children.has_key(c):
                p.children[c] = Node()
            p = p.children[c]

        p.lines.append(line)

    def search(self, token):
        p = self.root  
        for c in token:
            if not p.children.has_key(c):
                return None
            p = p.children[c]

        return p.lines

if __name__ == '__main__':
    dt = DictTree()
    dt.insert('aaab', 100)
    dt.insert('aa:::ab', 101)
    dt.insert('aacccjjab', 102)
    dt.insert('aaab', 103)
    dt.insert('aaab', 104)
    dt.insert('aaab', 100)
    dt.insert('aaab', 100)
    dt.insert('aaab', 100)
    dt.insert('aaab', 100)
    dt.insert('cccaaab', 100)
    dt.insert('aaab', 100)
    dt.insert('aaab', 100)
    print dt.search('aa:::ab')
    print dt.search('cccaaab')
