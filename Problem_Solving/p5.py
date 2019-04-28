# Sorting

def bubble(items):
    for i in range(len(items)):
        for j in range(len(items)-i-1):

            if items[j] > items[j+1]: items[j],items[j+1]=items[j+1],items[j]

def sort(items,):

    mid=len(items)/2
    left=items[:mid]
    right=items[mid:]
    sort(left)
    sort(right)
    join(left,right)



def join(left,right):
    left=[2,6]
    right=[1,7]
    joined=[]
    k=0
    for l,r in zip(left,right):
        if l<r: joined[k]=l
        else: joined[k]=r
        k+=1
    if len(left)<len(right):
        while(k!=len(right)):
            joined[k]=right[k]
            k+=1
    if len(left) > len(right):
        while (k != len(left)):
            joined[k] = left[k]
            k += 1


items=[6,2,1,7,0,-10]
bubble(items)
print(items)

