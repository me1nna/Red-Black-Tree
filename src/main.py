import random
import time


class RBTNode():
    '''
    Класс, представляющий узел красно-черного дерева.
    '''
    def __init__(self, right=None, left=None, parent=None, val=None, black=True) -> None:
        '''
        Инициализация узла красно-черного дерева.
        :param right: ссылка на правого сына
        :param left: ссылка на левого сына
        :param parent: ссылка на родителя
        :param val: значение, соответсвующе узлу
        :param black: True - узел черный, False - красный
        '''
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
        '''
        Метод, помогающий быстро получить высоту узла
        :return: int, высота
        '''
        if self is None:
            return 0
        return self.height

    def updateHeight(self) -> None:
        '''
        Метод, помогающий обновить высоту узла
        :return: None
        '''
        self.height = 1 + max(self.right.getHeight() if self.right else 0, self.left.getHeight() if self.left else 0)

    def getParent(self):
        '''
        Метод для быстрого получения ссылки на родителя узла
        :return: parent
        '''
        return self.parent

    def getGrandParent(self):
        '''
        Метод для быстрого получения ссылки на прародителя текущего узла
        :return: grandparent
        '''
        parent = self.getParent()
        if parent:
            return parent.getParent()
        return None

    def getUncle(self):
        '''
        Метод для быстрого получения дядюшки текущего узла
        :return: ссылка на дядю (или тётю)
        '''
        parent = self.getParent()
        if parent and parent.getParent():
            if parent.val < parent.getParent().val:
                return self.getGrandParent().right
            else:
                return self.getGrandParent().left
        return None

    def changeColor(self):
        '''
        Изменяем цвет текущего узла на противоположный
        :return:
        '''
        self.black = not self.black

    def getColor(self):
        '''
        Метод позволяющий быстро получить цвет текущего узла
        :return: False - Red, True - Black
        '''
        return self.black

    def __str__(self):
        '''
        Метод для представления узла в виде строки

        :return: Строковое представление объекта в виде строки.
        '''
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
    '''
    Класс, представляющий ниль-узел, наследуется от обычного узла красно-черного дерева
    '''
    def __init__(self):
        '''
        Инициализация ниль-узла красно-черного дерева, который должен быть во-первых мнимым, во-вторых черным
        :param right: None
        :param left: None
        :param parent: None
        :param val: None
        :param black: True (всегда черный)
        '''
        self.left = None
        self.right = None
        self.val = None
        self.black = True
        self.parent = None
        self.height = 1


class Tree:
    '''
    Класс, представляющий реализацию классического бинарного дерева поиска
    '''
    def __init__(self, root) -> None:
        '''
        Иницилазицаия дерева
        :param root: корень
        '''
        self.root = root

    def inOrderTraversal(self, tmp):
        '''
        Проход по дереву в симметричном порядке
        :param tmp: текущий узел, через который проходим
        :return: рекурсивно возвращаем симметричное представление дерева
        '''
        if tmp is None:
            return []
        left_result = self.inOrderTraversal(tmp.left)
        right_result = self.inOrderTraversal(tmp.right)
        return left_result + [tmp] + right_result

    def preOrderTraversal(self, tmp):
        '''
        Проход по дереву в прямом порядке
        :param tmp: текущий узел, через который проходим
        :return: рекурсивно возвращаем прямое представление дерева
        '''
        if tmp is None:
            return []
        left_result = self.preOrderTraversal(tmp.left)
        right_result = self.preOrderTraversal(tmp.right)
        return [tmp] + left_result + right_result

    def postOrderTraversal(self, tmp):
        '''
        Проход по дереву в обратном порядке
        :param tmp: текущий узел, через который проходим
        :return: рекурсивно возвращаем обратное представление дерева
        '''
        if tmp is None:
            return []
        left_result = self.postOrderTraversal(tmp.left)
        right_result = self.postOrderTraversal(tmp.right)
        return left_result + right_result + [tmp]

    def isBalanced(self) -> bool:
        '''
        Проверка дерева на сбалансированность
        :return: True - сбалансировано, False - нет
        '''
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
    '''
    Класс, представляющий красно-черное дерево
    '''
    def __init__(self, root=None) -> None:
        '''
        Инициализация кч-дерева
        :param root: корень
        '''
        self.NIL = NILNode()
        if root is None:
            self.root = self.NIL
        elif root.black is not True:
            raise ValueError("This node can't be the root of RB-Tree")
        else:
            self.root = root

    def find(self, val):
        '''
        Поиск узла с заданным значением
        :param key: заданное значение
        :return: узел с найденным значением
        '''
        tmp = self.getRoot()
        while tmp is not self.NIL and tmp.val != val:
            if val < tmp.val:
                tmp = tmp.left
            else:
                tmp = tmp.right
        return tmp

    def insert(self, val) -> None:
        '''
        Вставка значения в кч-дерево
        :param val: значение
        :return:
        '''
        new_node = RBTNode(self.NIL, self.NIL, self.NIL, val, False)
        self.__insert(new_node)
        self.__balance(new_node)
        self.root.updateHeight()

    def __insert(self, new_node: RBTNode) -> None:
        '''
        Приватный метод для вставки значения
        :param new_node: новый узел, который нужно вставить в дерево
        :return:
        '''
        tmp = self.getRoot()
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

    def __balance(self, node: RBTNode) -> None:
        '''
        Метод, осуществляющий балансировку красно-черного дерева
        :param node: узел, с которого происходит балансировка
        :return:
        '''
        while node.getParent() and node.getParent().black is False:
            if node.getParent() == node.getGrandParent().left:
                uncle = node.getUncle()
                if uncle.black is False:
                    node.getParent().black = True
                    uncle.black = True
                    node.getGrandParent().black = False
                    node = node.getGrandParent()
                else:
                    if node == node.getParent().right:
                        node = node.getParent()
                        self.__left_rotate(node)
                    node.parent.black = True
                    node.parent.parent.black = False
                    self.__right_rotate(node.parent.parent)
            else:
                uncle = node.getUncle()
                if uncle.black is not True:
                    node.parent.black = True
                    uncle.black = True
                    node.parent.parent.black = False
                    node = node.getGrandParent()
                else:
                    if node == node.getParent().left:
                        node = node.getParent()
                        self.__right_rotate(node)
                    node.parent.black = True
                    node.parent.parent.black = False
                    self.__left_rotate(node.parent.parent)

        self.root.black = True

    def __left_rotate(self, x):
        '''
        Левый поворот дерева вокруг узла
        :param x: узел, вокруг которого крутимся
        :return:
        '''
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

    def __right_rotate(self, y):
        '''
        Правый поворот вокруг узла
        :param y: узел, вокруг котрого крутимся
        :return:
        '''
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
        '''
        Метод для быстрого получения узла дерева
        :return:
        '''
        return self.root

    def __str__(self) -> str:
        '''
        Метод для строкового представления дерева
        :return: строковое представление
        '''
        str_arr = [[] for _ in range(self.root.getHeight() + 1)]
        self.__str__helper(self.root, str_arr, 0)
        str_arr = ["; ".join(elem) for elem in str_arr]
        return '\n'.join(str_arr)

    def __str__helper(self, tmp: RBTNode, str_arr: list[list[str]], level: int) -> None:
        '''
        Приватный метод помощник для строкового представления дерева
        :param tmp: текущий обратавыаемый узел
        :param str_arr: массив, содержащий строковое представление всех узлов дерева
        :param level: текущая глубина
        :return:
        '''
        if tmp is not None:
            str_arr[level].append(str(tmp))
            self.__str__helper(tmp.left, str_arr, level + 1)
            self.__str__helper(tmp.right, str_arr, level + 1)
        return


def main():
    rbt1 = RedBlackTree()
    for i in range(10):
        val = random.randint(1, 100)
        rbt1.insert(val)

    start = time.time()
    rbt1.insert(random.randint(1, 100))
    end = time.time()
    print(f"Вставка в дерево 10^1 {end - start}")

    rbt2 = RedBlackTree()
    for i in range(100):
        val = random.randint(1, 100)
        rbt2.insert(val)

    start = time.time()
    rbt2.insert(random.randint(1, 100))
    end = time.time()
    print(f"Вставка в дерево 10^2 {end - start}")

    rbt3 = RedBlackTree()
    for i in range(1000):
        val = random.randint(1, 100)
        rbt3.insert(val)

    start = time.time()
    rbt3.insert(random.randint(1, 100))
    end = time.time()
    print(f"Вставка в дерево 10^3 {end - start}")

    rbt4 = RedBlackTree()
    for i in range(10000):
        val = random.randint(1, 100)
        rbt4.insert(val)

    start = time.time()
    rbt4.insert(random.randint(1, 100))
    end = time.time()
    print(f"Вставка в дерево 10^4 {end - start}")

    rbt5 = RedBlackTree()
    for i in range(100000):
        val = random.randint(1, 100)
        rbt5.insert(val)

    start = time.time()
    rbt5.insert(random.randint(1, 100))
    end = time.time()
    print(f"Вставка в дерево 10^5 {end - start}")

if __name__ == "__main__":
    main()