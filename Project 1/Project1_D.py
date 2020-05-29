'''
This program utilizes the function 'borrow_value' to determine the optimal knapsack when capcity becomes dynamimc.
'''

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
    for i in V: #finds the first item to include in the knapsack based on the first '1' in the X matrix with max capacity
        if i[C]==1 and go=='yes':
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

#borrow_value function analyzes the various values at different capacities up to the max capcity to include all items in the knapsack    
def borrow_value(V,X,interest_rate,maxc,originalc):
    column=originalc #tracks capacity
    max_value=0 #tracks max value of knapsack
    max_column=0 #tracks the column associated wiht the max knapsack
    for i in V[0][originalc:]: #starts at original capacity without borrowing
        if column<=originalc: #calculates return of value without borrow(no interest)
            new_value=i-column
            if new_value>max_value:
                max_value=new_value
                max_column=column
        else:#calculates return of value when capacity is increased and interest must be accounted for
            new_value=i-column-(column-originalc)*interest_rate
            if new_value>max_value: #holds maximum
                max_value=new_value
                max_column=column 
        column+=1
    max_column+=1
    max_V=[] 
    max_X=[]
    for i in V:#creates new matrix to be solved where the highest column is the capacity from the max return value
        v_row=[]
        for j in i[0:max_column]:
            v_row.append(j)
        max_V.append(v_row)
    for i in X:#creates new matrix to be solved where the highest column is the capacity from the max return value
        x_row=[]
        for j in i[0:max_column]:
            x_row.append(j)
        max_X.append(x_row) 
    return max_value,max_column, max_V,max_X
            
            
    
       

value=[600,1000,600,300,500,300,800,500,900,700]
size=[400,600,400,200,300,200,400,200,600,400]
Capacity=2000

v=value
s=size
C=Capacity

interest_rate=.5

x=True
for i in value:
    if i%100!=0:
        x=False
for i in size:
    if i%100!=0:
        x=False
    

if C%100==0 and x==True:
    capacity_max=sum(size) #used to determine the greatest capacity to choose all items 
    base_capacity=C//100
    (v_divide,s_divide,c_divide)=divide_by_100(v,s,capacity_max)
    V,X=DPKP(v_divide,s_divide,c_divide)
    max_value,max_column, max_V,max_X=borrow_value(V,X,interest_rate,c_divide,base_capacity)
    items_in_knapsack, value_of_knapsack=in_knapsack(max_V,max_X,max_column-1,s_divide,v_divide)
    print("Interest Rate: {}".format(interest_rate))
    print("\tThe optimal knapsack includes items: {}".format(str(items_in_knapsack)[1:-1]))
    print("\tThe return of the optimal knapsack is {}".format(max_value)) 
    print("\t(return is printed as a multiple of 100)")    #return is printed as a multiple of 100 due to the divide_by_100 function. the return subtracts the money spent and interest
else:
    print("Items in v and s must be multipes of 100")
