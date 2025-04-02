import sys
from pathlib import Path

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

class TreeNode:
    def __init__(self, key, value, colour = 'red'):
        self.key = key
        self.value = value
        self.colour = colour
        self.left = None
        self.right = None
        self.parent = None

class RedBlackTree:
    def __init__(self):
        self.nil = TreeNode(None, None, 'black')
        self.root = self.nil

    def Insert(self, key, value):
        new_node = TreeNode(key, value)
        new_node.left = self.nil
        new_node.right = self.nil
        new_node.colour = 'red'
        parent = None
        current = self.root

        while current != self.nil:
            parent = current
            if key < current.key:
                current = current.left
            else:
                current = current.right
        new_node.parent = parent

        if parent == None:
            self.root = new_node
        elif key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        if new_node.parent == None:
            new_node.colour = 'black'
            return
        if new_node.parent.parent == None:
            return

        self.FixInsert(new_node)

    def FixInsert(self, node):
        while node != self.root and node.parent.colour == 'red':
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                if uncle.colour == 'red':
                    node.parent.colour = 'black'
                    uncle.colour = 'black'
                    node.parent.parent.colour = 'red'
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self.LeftRotate(node)
                    node.parent.colour = 'black'
                    node.parent.parent.colour = 'red'
                    self.RightRotate(node.parent.parent)
            else:
                uncle = node.parent.parent.left
                if uncle.colour == 'red':
                    node.parent.colour = 'black'
                    uncle.colour = 'black'
                    node.parent.parent.colour = 'red'
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self.RightRotate(node)
                    node.parent.colour = 'black'
                    node.parent.parent.colour = 'red'
                    self.LeftRotate(node.parent.parent)
        self.root.colour = 'black'

    def LeftRotate(self, node):
        right_node = node.right
        node.right = right_node.left
        if right_node.left != self.nil:
            right_node.left.parent = node
        right_node.parent = node.parent
        if node.parent == None:
            self.root = right_node
        elif node == node.parent.left:
            node.parent.left = right_node
        else:
            node.parent.right = right_node
        right_node.left = node
        node.parent = right_node

    def RightRotate(self, node):
        left_node = node.left
        node.left = left_node.right
        if left_node.right != self.nil:
            left_node.right.parent = node
        left_node.parent = node.parent
        if node.parent == None:
            self.root = left_node
        elif node == node.parent.right:
            node.parent.right = left_node
        else:
            node.parent.left = left_node
        left_node.right = node
        node.parent = left_node

    def Search(self, key):
        current = self.root
        while current != self.nil and key != current.key:
            if key < current.key:
                current = current.left
            else:
                current = current.right
        return None if current == self.nil else current
    
    def Delete(self, key):
        node = self.Search(key)
        if node is None:
            raise KeyError(f"Key {key} not found")
        y = node
        y_original_colour = y.colour
        if node.left == self.nil:
            x = node.right
            self.Transplant(node, node.right)
        elif node.right == self.nil:
            x = node.left
            self.Transplant(node, node.left)
        else:
            y = self.Minimum(node.right)
            y_original_colour = y.colour
            x = y.right
            if y.parent == node:
                x.parent = y
            else:
                self.Transplant(y, y.right)
                y.right = node.right
                y.right.parent = y
            self.Transplant(node, y)
            y.left = node.left
            y.left.parent = y
            y.colour = node.colour
        if y_original_colour == 'black':
            self.FixDelete(x)

    def Transplant(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def FixDelete(self, x):
        while x != self.root and x.colour == 'black':
            if x == x.parent.left:
                w = x.parent.right
                if w.colour == 'red':
                    w.colour = 'black'
                    x.parent.colour = 'red'
                    self.LeftRotate(x.parent)
                    w = x.parent.right
                if w.left.colour == 'black' and w.right.colour == 'black':
                    w.colour = 'red'
                    x = x.parent
                else:
                    if w.right.colour == 'black':
                        w.left.colour = 'black'
                        w.colour = 'red'
                        self.RightRotate(w)
                        w = x.parent.right
                    w.colour = x.parent.colour
                    x.parent.colour = 'black'
                    w.right.colour = 'black'
                    self.LeftRotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.colour == 'red':
                    w.colour = 'black'
                    x.parent.colour = 'red'
                    self.RightRotate(x.parent)
                    w = x.parent.left
                if w.right.colour == 'black' and w.left.colour == 'black':
                    w.colour = 'red'
                    x = x.parent
                else:
                    if w.left.colour == 'black':
                        w.right.colour = 'black'
                        w.colour = 'red'
                        self.LeftRotate(w)
                        w = x.parent.left
                    w.colour = x.parent.colour
                    x.parent.colour = 'black'
                    w.left.colour = 'black'
                    self.RightRotate(x.parent)
                    x = self.root
        x.colour = 'black'

    def Minimum(self, node):
        while node.left != self.nil:
            node = node.left
        return node
    
    def Maximum(self, node):
        while node.right != self.nil:
            node = node.right
        return node
    
    def __iter__(self):
        self.stack = []
        self.current = self.root
        while self.current != self.nil:
            self.stack.append(self.current)
            self.current = self.current.left
        return self
    
    def __next__(self):
        if not self.stack:
            raise StopIteration
        node = self.stack.pop()
        current = node.right
        while current != self.nil:
            self.stack.append(current)
            current = current.left
        return node.key, node.value
    
    def __len__(self):
        count = 0
        for _ in self:
            count += 1
        return count
    
    def __getitem__(self, key):
        node = self.Search(key)
        if node is None:
            raise KeyError(f"Key {key} not found")
        return node.value
    
    def __setitem__(self, key, value):
        node = self.Search(key)
        if node is None:
            raise KeyError(f"Key {key} not found")
        else:
            node.value = value

    def __contains__(self, key):
        return self.Search(key) is not None
    
    def __delitem__(self, key):
        self.Delete(key)

    def Append(self, key, value):
        self.Insert(key, value)