import math
def sub_matrix(matrix,end):
    new=[]
    for i in range(0,end+1):
        new_line=[]
        for j in range(0,end+1):
            new_line.append(matrix[i][j])
        new.append(new_line)
    return new

def time_expanded_network_G(G,S,U,T):
    place_i=0 #keeps track of node in different time period to make it node in time=0
    place_j=0 #keeps track of node in different time period to make it node in time=0 
    node_count=len(G)
    GT=[]
        
    for i in range(0,node_count*(T+1)): #creating matrix for GT of size 0 to node_count
        add_list=[]
        for j in range(0,node_count*(T+1)):
            add_list.append(0)
        GT.append(add_list)

    #adds arcs to GU for capacity remaining at an arc over t    
    present_node=0
    for i in range(0,len(GT)):
        next_node=present_node+node_count
        if next_node<len(GT):
            GT[present_node][next_node]=1
        present_node+=1
        
    row_G=0  
    for i in range(0,len(GT)):
        column_G=0
        for j in G[row_G]:
            if j==1:
                difference=column_G-row_G
                next_column=i+S[row_G][column_G]*len(G)+difference
                if next_column<len(GT):
                    GT[i][next_column]=1
            column_G+=1
            if column_G==len(G):
                column_G=0
        row_G+=1
        if row_G==len(G):
            row_G=0
    return GT

def time_expanded_network_U(G,S,U,T):
    place_i=0 #keeps track of node in different time period to make it node in time=0
    place_j=0 #keeps track of node in different time period to make it node in time=0 
    node_count=len(U)
    UT=[]
        
    for i in range(0,node_count*(T+1)): #creating matrix for GT of size 0 to node_count
        add_list=[]
        for j in range(0,node_count*(T+1)):
            add_list.append(0)
        UT.append(add_list)

    #adds arcs to GU for capacity remaining at an arc over t    
    present_node=0
    for i in range(0,len(UT)):
        next_node=present_node+node_count
        if next_node<len(UT):
            UT[present_node][next_node]=math.inf
        present_node+=1
        
    row_G=0  
    for i in range(0,len(UT)):
        column_G=0
        for j in G[row_G]:
            if j==1:
                difference=column_G-row_G
                next_column=i+S[row_G][column_G]*len(G)+difference
                if next_column<len(UT):
                    UT[i][next_column]=U[row_G][column_G]
            column_G+=1
            if column_G==len(G):
                column_G=0
        row_G+=1
        if row_G==len(G):
            row_G=0
    return UT
            
def PathCreator(pred, s, j):
    #Determines the path from source node s to node j using the predecessor array.
    Path = [j]
    node = j
    while node != s:
        Path.insert(0, pred[node])
        node = pred[node]
        
    return Path

def BFSNodeNode(G, s):
    #Determines the set of reachable nodes from s given a node-node adjacency matrix representation of the network
    n = len(G)
    pred = [ -1 for i in range(n)]
    order = [ 0 for i in range(n)]
    mark = [0 for i in range(n)]  # mark(i) = 1 if we have found a directed path from s to i
    
    S = [s]
    pred[s] = s
    order[s] = 1
    mark[s] = 1
    k = 2 #keep track of the order of the next discovered node
    
    while len(S) > 0:
        i = S.pop(0)
        for j in range(n):
            if G[i][j] == 1:
                if mark[j] == 0:
                    pred[j] = i
                    order[j] = k
                    k+= 1
                    mark[j] = 1
                    S.append(j)
    
    return pred, order


def AugPath(G, U, s, t):
    #Applies the augmenting path algorithm to a network G, represented using a node-node adjancency matrix with arc capacities given by U and source node s and sink node t.  Throughout the algorithm, the residual network will be represented as a node-node adjancency matrix since it is easier to remove arcs from this representation.
    
    n = len(G)
    RG = [ [0 for i in range(n)] for i in range(n)]   #node-node adjancency matrix of the residual network
    RU = [ [0 for i in range(n)] for i in range(n)]  #residual capacities 
    
    for i in range(n):  #Initialization of residual network
        for j in range(n):
            if G[i][j] == 1:    #If arc (i, j) exists, then update its residual capacity
                RU[i][j] = U[i][j]
                if RU[i][j] > 0:
                    RG[i][j] = 1    #If arc (i, j) has positive residual capacity, put it in the residual network.
                    
    vstar = 0
    # from BFSNodeNode import BFSNodeNode
    #from PathCreator import PathCreator
    
    pred, order = BFSNodeNode(RG, s)  #if pred[t] >=0, then there is an s-t path.
    print(pred,order)
    
    while pred[t] > -1:
        P = PathCreator(pred, s, t)  #Get path
        print(P)
        delta = math.inf
        for i in range(len(P)-1):  #Finds the minimum residual capacatiy.  The arc (P[i], P[i+1]) is in the path for all i < len(P)-1
            if RU[P[i]][P[i+1]] < delta:
                delta = RU[P[i]][P[i+1]]
        vstar += delta  #Increase delta
        for i in range(len(P)-1):   #Scan all arcs in the path and update their residual capacities and their backward arcs' residual capacities
            RU[P[i+1]][P[i]] += delta   #Updating backwards arc's residual capacities
            RG[P[i+1]][P[i]] = 1
            RU[P[i]][P[i+1]] -= delta  #Forward arc's turn
            if RU[P[i]][P[i+1]] == 0:   #Remove arc's whose residual capacity drops to zero.
                RG[P[i]][P[i+1]] = 0
        pred, order = BFSNodeNode(RG, s)  #Run search on updated residual network.  
    
    return vstar

P=50
G=[[0,1,1,0],
   [0,0,0,1],
   [0,1,0,1],
   [0,0,0,0]]
S=[[0,5,4,0],
   [0,0,0,4],
   [0,3,0,2],
   [0,0,0,0]]

U=[[0,10,5,0],
   [0,0,0,6],
   [0,10,0,2],
   [0,0,0,0]]


T=15
P=50
GT=(time_expanded_network_G(G,S,U,T))
UT=(time_expanded_network_U(G,S,U,T))
evacuated =0
time_to_check=1
increment=len(G)
while evacuated<P:
    sink_node=len(G)+time_to_check*increment-1
    evacuated=(AugPath(GT,UT,0,sink_node))
    time_to_check+=1
print('{} people evacuated in T={}'.format(evacuated,time_to_check))
