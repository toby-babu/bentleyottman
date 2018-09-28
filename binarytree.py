from __future__ import print_function


class Node(object):
    """Tree node: left and right child + data which can be any object

    """
    def __init__(self, data):
        """Node constructor

        @param data node data object
        """
        self.left = None
        self.right = None
        self.data = data

    def insert(self, data):
        """Insert new node with data

        @param data node data object to insert
        """
        if self.data:
            if data.start.x < self.data.start.x:
                if self.left is None:
                    self.left = Node(data)
                else:
                    self.left.insert(data)
            elif data.start.x > self.data.start.x:
                if self.right is None:
                    self.right = Node(data)
                else:
                    self.right.insert(data)
            elif data.start.x == self.data.start.x:
                if data.start.y < self.data.start.y:
                    if self.left is None:
                        self.left = Node(data)
                    else:
                        self.left.insert(data)
                elif data.start.y > self.data.start.y:
                    if self.right is None:
                        self.right = Node(data)
                    else:
                        self.right.insert(data)
                elif data.start.y == self.data.start.y:
                    if data.end.x < self.data.end.x:
                        if self.left is None:
                            self.left = Node(data)
                        else:
                            self.left.insert(data)
                    elif data.end.x > self.data.end.x:
                        if self.right is None:
                            self.right = Node(data)
                        else:
                            self.right.insert(data)
                    elif data.end.x == self.data.end.x:
                        if data.end.y < self.data.end.y:
                            if self.left is None:
                                self.left = Node(data)
                            else:
                                self.left.insert(data)
                        elif data.end.y > self.data.end.y:
                            if self.right is None:
                                self.right = Node(data)
                            else:
                                self.right.insert(data)
        else:
            self.data = data

    def lookup(self, data, parent=None):
        """Lookup node containing data

        @param data node data object to look up
        @param parent node's parent
        @returns node and node's parent if found or None, None
        """
        if data.start.x < self.data.start.x:
            if self.left is None:
                return None, None
            return self.left.lookup(data, self)
        elif data.start.x > self.data.start.x:
            if self.right is None:
                return None, None
            return self.right.lookup(data, self)
        else:
            if data.start.y < self.data.start.y:
                if self.left is None:
                    return None, None
                return self.left.lookup(data, self)
            elif data.start.y > self.data.start.y:
                if self.right is None:
                    return None, None
                return self.right.lookup(data, self)
            else:
                if data.end.x < self.data.end.x:
                    if self.left is None:
                        return None, None
                    return self.left.lookup(data, self)
                elif data.end.x > self.data.end.x:
                    if self.right is None:
                        return None, None
                    return self.right.lookup(data, self)
                else:
                    if data.end.y < self.data.end.y:
                        if self.left is None:
                            return None, None
                        return self.left.lookup(data, self)
                    elif data.end.y > self.data.end.y:
                        if self.right is None:
                            return None, None
                        return self.right.lookup(data, self)
                    else:
                        return self, parent

    def delete(self, data):
        """Delete node containing data

        @param data node's content to delete
        """
        # get node containing data
        node, parent = self.lookup(data)
        if node is not None:
            children_count = node.children_count()
            if children_count == 0:
                # if node has no children, just remove it
                if parent:
                    if parent.left is node:
                        parent.left = None
                    else:
                        parent.right = None
                else:
                    self.data = None
            elif children_count == 1:
                # if node has 1 child
                # replace node by its child
                if node.left:
                    n = node.left
                else:
                    n = node.right
                if parent:
                    if parent.left is node:
                        parent.left = n
                    else:
                        parent.right = n
                else:
                    self.left = n.left
                    self.right = n.right
                    self.data = n.data
            else:
                # if node has 2 children
                # find its successor
                parent = node
                successor = node.right
                while successor.left:
                    parent = successor
                    successor = successor.left
                # replace node data by its successor data
                node.data = successor.data
                # fix successor's parent node child
                if parent.left == successor:
                    parent.left = successor.right
                else:
                    parent.right = successor.right

    def print_tree(self, label):
        """Print tree content inorder

        """
        if self.left:
            label = self.left.print_tree(label)
        print(self.data.label, end=" ")
        label = label + self.data.label + " "
        if self.right:
            label = self.right.print_tree(label)

        return label

    def children_count(self):
        """Return the number of children

        @returns number of children: 0, 1, 2
        """
        cnt = 0
        if self.left:
            cnt += 1
        if self.right:
            cnt += 1
        return cnt
