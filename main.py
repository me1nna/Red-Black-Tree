class RBTNode():
    def __init__(self, right=None, left=None, parent=None, val=None, black=True) -> None:
        self.left = left
        self.right = right
        self.val = val
        self.black = black
        self.parent = parent
        if self.right is None and self.left is None:
            self.height = 1
        else:
            self.height = max(self.left.getHeight() if self.left else 0,
                              self.right.getHeight() if self.right else 0) + 1

    def getHeight(self) -> int:
        if self is None:
            return 0
        return self.height

    def updateHeight(self) -> None:
        self.height = 1 + max(self.right.getHeight() if self.right else 0, self.left.getHeight() if self.left else 0)

    def getBlackHeight(self):
        countBlack = int(self.black)
        tmp = self.parent
        while tmp:
            countBlack += int(tmp.black)
            tmp = tmp.parent
        return countBlack

    def getRedHeight(self):
        countRed = int(not self.black)
        tmp = self.parent
        while tmp:
            countRed += int(not tmp.black)
            tmp = tmp.parent
        return countRed

    def getParent(self):
        return self.parent

    def getGrandParent(self):
        parent = self.getParent()
        if parent:
            return parent.getParent()
        return None

    def getUncle(self):
        parent = self.getGrandParent()
        if parent and parent.getParent():
            if parent.value < parent.getParent().value:
                return self.getGrandParent().right
            else:
                return self.getGrandParent().left
        return None

    def changeColor(self):
        self.black = not self.black

    def getColor(self):
        return self.color

    def __str__(self):
        if self.val == None:
            return "Pseudo Black Node with no value"
        if self.black:
            if self.left is None and self.right is None:
                return f"Black Node, value = {self.val}"
            if self.right is None:
                return f"Black Node, value = {self.val}, left child value = {self.left.val}"
            if self.left is None:
                return f"Black Node, value = {self.val}, right child value = {self.right.val}"
            return f"Black Node, value = {self.val}, left child value = {self.left.val}, and right child value = {self.right.val}"
        else:
            if self.left is None and self.right is None:
                return f"Red Node, value = {self.val}"
            if self.right is None:
                return f"Red Node, value = {self.val}, left child value = {self.left.val}"
            if self.left is None:
                return f"Red Node, value = {self.val}, right child value = {self.right.val}"
            return f"Red Node, value = {self.val}, left child value = {self.left.val}, and right child value = {self.right.val}"


class NILNode(RBTNode):
    def __init__(self):
        self.left = None
        self.right = None
        self.val = None
        self.black = True
        self.parent = None
        self.height = 1


class Tree:
    def __init__(self, root) -> None:
        self.root = root

    def in_order_traversal(self, tmp):
        if tmp is None:
            return []
        left_result = self.in_order_traversal(tmp.left)
        right_result = self.in_order_traversal(tmp.right)
        return left_result + [tmp] + right_result

    def pre_order_traversal(self, tmp):
        if tmp is None:
            return []
        left_result = self.in_order_traversal(tmp.left)
        right_result = self.in_order_traversal(tmp.right)
        return [tmp] + left_result + right_result

    def post_order_traversal(self, tmp):
        if tmp is None:
            return []
        left_result = self.in_order_traversal(tmp.left)
        right_result = self.in_order_traversal(tmp.right)
        return left_result + right_result + [tmp]

    def isBalanced(self) -> bool:
        return self.__isBalanced(self.root)

    def __isBalanced(self, tmp) -> bool:
        if not tmp:
            return True
        left_height = tmp.left.getHeight() if tmp.left else 0
        right_height = tmp.right.getHeight() if tmp.right else 0
        if abs(left_height - right_height) <= 1 and self.__isBalanced(tmp.left) and self.__isBalanced(tmp.right):
            return True
        return False


class RedBlackTree(Tree):
    def __init__(self, root=None) -> None:
        self.NIL = NILNode()
        if root is None:
            self.root = self.NIL
        elif root.black is not True:
            raise ValueError("This node can't be the root of RB-Tree")
        else:
            self.root = root

    def find(self, key):
        tmp = self.root
        while tmp is not None and tmp.val != key:
            if key < tmp.val:
                tmp = tmp.left
            else:
                tmp = tmp.right
        if tmp.val != key:
            raise KeyError(f"Node with key {key} is not found")
        return tmp

    def insert(self, val) -> None:
        new_node = RBTNode(self.NIL, self.NIL, self.NIL, val, False)
        self.__insert(new_node)
        self.__balance(new_node)
        self.root.updateHeight()

    def __insert(self, new_node: RBTNode):
        tmp = self.root
        prev_tmp = None
        while tmp != self.NIL and tmp is not None:
            prev_tmp = tmp
            if new_node.val < tmp.val:
                tmp = tmp.left
            else:
                tmp = tmp.right

        parent = prev_tmp
        new_node.parent = parent

        if parent is None:
            self.root = new_node
        elif new_node.val < parent.val:
            parent.left = new_node
        else:
            parent.right = new_node

    def __balance(self, node):
        while node.parent and node.parent.black is False:
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                if uncle.black is False:
                    node.parent.black = True
                    uncle.black = True
                    node.parent.parent.black = False
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self._left_rotate(node)
                    node.parent.black = True
                    node.parent.parent.black = False
                    self._right_rotate(node.parent.parent)
            else:
                uncle = node.parent.parent.left
                if uncle.black is not True:
                    node.parent.black = True
                    uncle.black = True
                    node.parent.parent.black = False
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self._right_rotate(node)
                    node.parent.black = True
                    node.parent.parent.black = False
                    self._left_rotate(node.parent.parent)

        self.root.black = True

    def _left_rotate(self, x):
        y = x.right
        x.right = y.left

        if y.left != self.NIL:
            y.left.parent = x

        y.parent = x.parent

        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    def _right_rotate(self, y):
        x = y.left
        y.left = x.right

        if x.right != self.NIL:
            x.right.parent = y

        x.parent = y.parent

        if y.parent is None:
            self.root = x
        elif y == y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x

        x.right = y
        y.parent = x

    def getRoot(self):
        return self.root

    def __str__(self) -> str:
        str_arr = [[] for _ in range(self.root.getHeight() + 1)]
        self.__str__helper(self.root, str_arr, 0)
        str_arr = ["; ".join(elem) for elem in str_arr]
        return '\n'.join(str_arr)

    def __str__helper(self, tmp: RBTNode, str_arr: list[list[str]], level: int) -> None:
        if tmp is not None:
            str_arr[level].append(str(tmp))
            self.__str__helper(tmp.left, str_arr, level + 1)
            self.__str__helper(tmp.right, str_arr, level + 1)
        return


def main():
    rbtnode = RBTNode(val=32)
    rbt = RedBlackTree(root=rbtnode)
    rbt.insert(35)
    rbt.insert(28)
    rbt.insert(120)
    print(rbt.getRoot().getHeight())
    print(rbt)
    print(rbt.getRoot().getHeight())

if __name__ == "__main__":
    main()