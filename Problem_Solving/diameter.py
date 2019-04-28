class TreeNode:
    def __init__(self,val,left=None,right=None):
        self.val=val
        self.left=left
        self.right=right

maxdim=0
def dim(n):
    global maxdim
    if n.left==None and n.right==None:
        return 0
    lh=dim(n.left)
    rh=dim(n.right)
    ht=max(lh,rh)+1
    dia=lh+rh+1
    if dia > maxdim:
        maxdim=dia
    return ht

root=TreeNode(2)
root.left=TreeNode(3)
root.right=TreeNode(4)
root.right.right=TreeNode(5)

dim(root)