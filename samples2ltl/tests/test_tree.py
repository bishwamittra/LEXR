import pdb
import sys
sys.path.append("..")
try:
    from utils.SimpleTree import SimpleTree
except:
    from samples2ltl.utils.SimpleTree import SimpleTree

def test_basic():
    root = SimpleTree(label="|")
    root.addChildren("|", "x2")
    left = root.left
    left.addChildren("x0", "x1")
    
    
    
    print(root)
    print(root.getAllLabels())
    print(root.getAllNodes())

    

if __name__ == "__main__":
    test_basic()