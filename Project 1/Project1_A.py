"""
This program uses the timeit module to calculate the runtime for two dynamic programming models to determine the optimal model. DPKP utilizes a matrix filled with zeros to begin, while DPKP1 does not.
"""

def DynamicProgrammingtest(n, Vmax, Smax, alpha, x):
    from random import randint
    import timeit
    rtdpstore = 0  #keep track of the cumulative running time so far of running the greedy algorithm (normal version) on the create instances
    rtdp = 0 #keep track of the cumulative running time so far of running the greedy algorithm (sorted version) on the create instance
    C = (n)*(Smax/2)*alpha
    for i in range(x):
        v = [randint(1, Vmax) for j in range(n)]
        s = [randint(1, Smax) for j in range(n)]
        #runtime when zeros are stored initially
        start = timeit.time.clock()
        [Sg, vg] = DPKP(v, s, C)
        end = timeit.time.clock()
        rtdpstore = rtdpstore+ (end - start)
        #runtime when no zeros are stored initially
        start = timeit.time.clock()
        [Sg, vg] = DPKP1(v, s, C)
        end = timeit.time.clock()
        rtdp = rtdp + (end - start)        
    return rtdpstore/x, rtdp/x

#Applies the dynamic programming method to the knapsack problem where v are the values of the n items, s are the sizes of the n items, C is the capacity, and values are not stored. 
def DPKP1(v, s, C):
    n = len(v)
    V = [ [] for j in range (n)  ]
    X = [ [] for j in range (n)  ]
    
    for cp in range(int(C)+1):
        if s[n-1] <= cp:
            V[n-1].append(v[n-1])
            X[n-1].append(1)
        else:
            V[n-1].append(0)
            X[n-1].append(0)  
            
    for i in reversed(range(n-1)):
        for cp in range(int(C)+1):
            if s[i] <= cp:
                if v[i] + V[i+1][cp-s[i]] > V[i+1][cp]:
                    V[i].append(v[i] + V[i+1][cp-s[i]])
                    X[i].append(1)
                else:
                    V[i].append(V[i+1][cp])
                    X[i].append(0)
            else:
                V[i].append(V[i+1][cp])
                X[i].append(0)
    
    return V, X

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
                
n=3
Vmax=5
Smax=6
alpha=.13
x=4

stored_time,not_stored_time=(DynamicProgrammingtest(n,Vmax,Smax,alpha,x))
print('n:{}\nVmax:{}\nSmax:{}\nalpha:{}\nx:{}\n'.format(n,Vmax,Smax,alpha,x))
print("The run time for the dynamic programming model with the stored values is {:.8f}. \nThe run time for the dynamic programming model without the stored values is {:.8f}.".format(stored_time,not_stored_time))
if stored_time>not_stored_time:
    print("The run time for the dynamic programming model without storing values initially is faster than the run time for the dynamic programming model that initally stores values.")
elif stored_time<not_stored_time:
    print("The run time for the dynamic programming model storing values initially is faster than the run time for the dynamic programming model that does not initialy store values.")