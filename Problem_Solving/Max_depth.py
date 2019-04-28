class TreeNode:

    def __init__(self,val,left=None, right=None):
        self.val=val,
        self.left=left
        self.right=right


def maxDepth(root: 'TreeNode') -> 'int':
    if root == None:
        return 0

    return 1 + max(maxDepth(root.left), maxDepth(root.right))


root=TreeNode(2)
root.left=TreeNode(3)
root.right=TreeNode(1)
root.left.left=TreeNode(4)
root.left.left.right=TreeNode(5)
root.right.right=TreeNode(7)


h=maxDepth(root)
print(h)