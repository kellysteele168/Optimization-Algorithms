"""
This program runs the dynamic programming model dividing the input by zero for portfolio optimization applications
"""


#Applies the dynamic programming method to the knapsack problem where v are the values of the n items, s are the sizes of the n items, and C is the capacity, and values are stored initially
def DPKP(v, s, C):
    n = len(v)
    V = [ [0 for cp in range(int(C)+1)] for j in range (n)  ]
    X = [ [0 for cp in range(int(C)+1)] for j in range (n)  ]
    
    for cp in range(int(C)+1):
        if s[n-1] <= cp:
            V[n-1][cp] = v[n-1]
            X[n-1][cp] = 1
    
    for i in reversed(range(n-1)):
        for cp in range(int(C)+1):
            if s[i] <= cp:
                if v[i] + V[i+1][cp-s[i]] > V[i+1][cp]:
                    V[i][cp] = v[i] + V[i+1][cp-s[i]]
                    X[i][cp] = 1
                else:
                    V[i][cp] = V[i+1][cp]
            else:
                V[i][cp] = V[i+1][cp]
    
    return V, X

#function returns value of optimal knapsack and items in it
def in_knapsack(V,X,C,s,v):
    items_in_knapsack=[]
    value_of_knapsack=max(V[0]) #highest value of knapsack appears in the first row of the matrix
    go='yes'
    time=0
    for i in X: #finds the first item to include in the knapsack based on the first '1' in the X matrix with max capacity
        if X[X.index(i)][C]==1 and go=='yes':
            go='no'
            items_in_knapsack.append(X.index(i)+1)
            C-=s[time]
            time+=1
            
    while C>=0 and time<=len(s)-1: #determines the other items to include while the capacity is positive and items still need to be examined
        for i in X[time:]:
            if i[C]==1:
                items_in_knapsack.append(time+1)
                C-=s[time]
                time+=1
            else:
                time+=1
    
    return items_in_knapsack, value_of_knapsack

def divide_by_100(v,s,c): #divides values, sizes, and capacity by 100 
    v_divide=[]
    s_divide=[]
    c_divide=int(c/100)
    #appends values and sizes divided by 100 to new lists
    for i in v:
        v_divide.append(int(i/100))
    for i in s:
        s_divide.append(int(i/100))
    return v_divide,s_divide,c_divide
        

v=[600,1000,200]
s=[400,600,300]
C=1000

#ensuring values are multiples of 100
x=True
for i in v:
    if i%100!=0:
        x=False
for i in s:
    if i%100!=0:
        x=False

if C%100==0 and x==True:
    v_divide,s_divide,c_divide=divide_by_100(v,s,C) #divides values by 100
    V,X=DPKP(v_divide,s_divide,c_divide)
    items_in_knapsack, value_of_knapsack=in_knapsack(V,X,c_divide,s_divide,v_divide)#determines knapsack for new values
    
    print("Solving through division:")
    print("\tThe optimal knapsack includes items: {}".format(str(items_in_knapsack)[1:-1]))
    print("\tThe value of the optimal knapsack is {}".format(value_of_knapsack)) 
    print("\t(value is printed as a multiple of 100)")
    
    V,X=DPKP(v,s,C)
    items_no_divide,value_no_divide=in_knapsack(V,X,C,s,v)
    
    print("Solving with standard method:")  
    print("\tThe optimal knapsack includes items: {}".format(str(items_no_divide)[1:-1]))
    print("\tThe value of the optimal knapsack is {}".format(value_no_divide)) 
else:
    print("Items in v and s must be multipes of 100")
