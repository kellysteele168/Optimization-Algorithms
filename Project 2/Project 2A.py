import math


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
            
            


G=[[0,1,1,0],
   [0,0,0,1],
   [0,1,0,1],
   [0,0,1,0]]

S=[[0,2,3,0],
   [0,0,0,4],
   [0,4,0,3],
   [0,0,1,0]]

U=[[0,7,10,0],
   [0,0,0,5],
   [0,7,0,4],
   [0,0,8,0]]
T=4
GT=(time_expanded_network_G(G,S,U,T))
for i in GT:
    print(i)
    
print(' ')

UT=time_expanded_network_U(G,S,U,T)
for i in UT:
    print(i)

