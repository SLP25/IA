class Node:
    def __init__(self, name, id = -1):
        self.id = id
        self.name = name

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def setId(self, id):
        self.id = id

    def setName(self, name):
        self.name = name

    def __str__(self):
        return f"Node: {self.name}"
    
    def __eq__(self, node):
        return node.name == self.name