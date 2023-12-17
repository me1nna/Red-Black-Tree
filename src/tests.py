from main import RedBlackTree, RBTNode
from modules import check
import random

def test_isNotRBT():
    root = RBTNode(val=120, black=False)
    assert check.isRBT(root) is False

def test_insert():
    rbt = RedBlackTree()
    for i in range(10):
        val = random.randint(1, 100)
        rbt.insert(val)
    assert check.isRBT(rbt.getRoot()) is True

def test_insertALot():
    rbt = RedBlackTree()
    for i in range(100):
        val = random.randint(1, 1000)
        rbt.insert(val)
    assert check.isRBT(rbt.getRoot()) is True

def test_find():
    rbt = RedBlackTree()
    rbt.insert(35)
    rbt.insert(28)
    rbt.insert(120)
    rbt.insert(44)
    rbt.insert(19)
    assert check.isRBT(rbt.getRoot()) is True and rbt.find(44).val == 44

def test_notFound():
    rbt = RedBlackTree()
    rbt.insert(35)
    rbt.insert(28)
    rbt.insert(120)
    rbt.insert(44)
    rbt.insert(19)
    assert check.isRBT(rbt.getRoot()) is True and rbt.find(999).val is None
