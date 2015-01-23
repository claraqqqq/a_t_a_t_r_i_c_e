"""
Project 2 - Connected components and graph resilience
"""

import alg_module2_graphs

def bfs_visited(ugraph, start_node): 
    
    """
    Takes the undirected graph ugraph and the node start_node 
    and returns the set consisting of all nodes 
    that are visited by a breadth-first search 
    that starts at start_node.
    """
    queue = []
    visited = set([])
    visited.add(start_node)
    queue.append(start_node) 
    while len(queue) != 0:        
        node = queue.pop(0)
        #print 'node',node
        if len(ugraph[node]) != 0:
            #print 'true'
            for neighbor in ugraph[node]:
                #print 'node', node
                if neighbor not in visited:                    
                    visited.add(neighbor)
                    queue.append(neighbor) 
                    #print 'visited', visited
    return visited
                      
#print bfs_visited(alg_module2_graphs.GRAPH3, 0)
#expected set([0, 1, 2, 3]) 
#print alg_module2_graphs.GRAPH3


def cc_visited(ugraph):
    """
    Takes the undirected graph ugraph and returns a list of sets, 
    where each set consists of all the nodes (and nothing else) 
    in a connected component, and there is exactly one set in 
    the list for each connected component in ugraph and 
    nothing else.
    """
    remain_nodes = []
    for key in ugraph.keys():
        remain_nodes.append(key)
    #print 'remain_nodes', remain_nodes
    connect_components = []
    while len(remain_nodes) != 0:
        node = remain_nodes[0]
        ww_bfs = bfs_visited(ugraph, node)
        #print ww_bfs
        connect_components.append(ww_bfs)
        for element in ww_bfs:
            remain_nodes.remove(element) 
    return connect_components


#print cc_visited(alg_module2_graphs.GRAPH0) 
#expected [set([0, 1, 2, 3])] 

def largest_cc_size(ugraph):
    """
    Takes the undirected graph ugraph and returns the size 
    (an integer) of the largest connected component in ugraph.
    """
    connect_components = cc_visited(ugraph)
    cc_size = []
    for cc_element in connect_components:
        cc_size.append(len(cc_element))
    return max(cc_size) if len(cc_size) != 0 else 0

#print largest_cc_size(alg_module2_graphs.GRAPH0)
#expected 4 

def compute_resilience(ugraph, attack_order):
    """
    Takes the undirected graph ugraph, a list of nodes attack_order 
    and iterates through the nodes in attack_order. 
    For each node in the list, the function removes the given node 
    and its edges from the graph and then computes the size of the 
    largest connected component for the resulting graph.
    The function should return a list whose k+1th entry is the size 
    of the largest connected component in the graph after the 
    removal of the first k nodes in attack_order. 
    The first entry (indexed by zero) is the size of the largest 
    connected component in the original graph.
    """
    cc_largest = [largest_cc_size(ugraph)]
    ugraph_copy = ugraph
    for attack_node in attack_order:
        del ugraph_copy[attack_node]
        #print ugraph_copy
        for key in ugraph_copy.keys():
            if attack_node in ugraph_copy[key]:
                ugraph_copy[key].remove(attack_node)        
        cc_largest.append(largest_cc_size(ugraph_copy))
    
    return cc_largest

#print alg_module2_graphs.GRAPH0    
#print compute_resilience(alg_module2_graphs.GRAPH0, [1, 2]) 
#expected [4, 2, 1] 
#print compute_resilience(alg_module2_graphs.GRAPH2, [1, 3, 5, 7, 2, 4, 6, 8]) 