# Union and intersection of two lists

#l1=[1,2,3,4]
l1=[]
#l2=[5,4,3,0]
l2=[]

def union(l1,l2):
    uni_list=[e for e in l1]
    inter_list=[]
    for e in l2:
        if e in uni_list:
            inter_list.append(e)
        else: uni_list.append(e)
    print (uni_list)
    print(inter_list)

union(l1,l2)