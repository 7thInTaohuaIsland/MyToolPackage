def Sort_A_taking_B_bubble(A:list,B:list):
    '''
    :param A: 待排序数组
    :param B: 随着A排序进行同步变化
    :return: A_re:排序后的A
             B_re:排序后的B
    '''
    if len(A)!=len(B):
        raise ValueError
    num=len(A)
    A_tmp=A.copy()
    B_tmp=B.copy()
    B_re=[0]*num
    A_re=[0]*num
    i=0
    while len(A_tmp)>0:
        min_tmp=min(A_tmp)
        index=A_tmp.index(min_tmp)
        A_tmp.pop(index)
        B_tmp.pop(index)
        index1=A.index(min_tmp)
        A_re[i]=A[index1]
        B_re[i]=B[index1]
        i+=1
    return A_re,B_re
