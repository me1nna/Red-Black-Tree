def isRBT(root):
    def isOkay(node):
        # NIL-узел является допустимым красно-черным деревом
        if node.val is None:
            return True

        # Корень дерева всегда черный
        if node == root and node.black is not True:
            return False

        # Все листовые узлы черные
        if node.left is None and node.right is None and node.black is not True:
            return False

        # Если узел красный, то его потомки - черные
        if node.black is False and (node.left.black is not True and node.right.black is not True):
            return False

        # Корректная черная высота поддеревьев для всех нисходящих путей
        if checkBlackHeight(node) is False:
            return False

    def checkBlackHeight(node):
        # NIL-узел считается одним из узлов в пути
        if node.val is None:
            return 1

        leftBlackHeight = checkBlackHeight(node.left)
        rightBlackHeight = checkBlackHeight(node.right)

        # Некорректная черная глубина, если глубины правого и черного поддерева не равны, или если одна из них равна False
        if leftBlackHeight != rightBlackHeight or leftBlackHeight is False or rightBlackHeight is False:
            return False

        return rightBlackHeight + (1 if node.black is True else 0)

    return isOkay(root) is not False