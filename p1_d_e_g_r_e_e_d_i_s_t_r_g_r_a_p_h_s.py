"""
Project 1 - Degree distributions for graphs
"""

EX_GRAPH0 = {0: set([1, 2]),
             1: set([]),
             2: set([])}

EX_GRAPH1 = {0: set([1, 4, 5]),
             1: set([2, 6]),
             2: set([3]),
             3: set([0]),
             4: set([1]),
             5: set([2]),
             6: set([])}

EX_GRAPH2 = {0: set([1, 4, 5]),
             1: set([2, 6]),
             2: set([3, 7]),
             3: set([7]),
             4: set([1]),
             5: set([2]),
             6: set([]),
             7: set([3]),
             8: set([1, 2]),
             9: set([0, 3, 4, 5, 6, 7])}


def make_complete_graph(num_nodes):
    """
    Takes the number of nodes num_nodes and returns a dictionary corresponding
    to a complete directed graph with the specified number of nodes. 
    A complete graph contains all possible edges subject 
    to the restriction that self-loops are not allowed. 
    The nodes of the graph should be numbered 0 
    to num_nodes - 1 when num_nodes is positive. 
    Otherwise, the function returns a dictionary 
    corresponding to the empty graph.
    """
    complete_graph = {}
    if num_nodes == 0:
        return complete_graph
    for node_index in range(num_nodes):
        all_nodes = [i for i in range(num_nodes)]
        all_nodes.remove(node_index)
        complete_graph[node_index] = set(all_nodes)
    return complete_graph
#num_nodes = 0
#print make_complete_graph(num_nodes)


def compute_in_degrees(digraph):
    """
    Takes a directed graph digraph (represented as a dictionary) 
    and computes the in-degrees for the nodes in the graph. 
    The function should return a dictionary with the same 
    set of keys (nodes) as digraph whose corresponding values 
    are the number of edges whose head matches a particular node.
    
    code below returns indegree node (not edge number):
    num_nodes = len(digraph.keys())
    indegree_digraph = {}
    # initialize indegree_digraph
    for node_index in range(num_nodes):
        indegree_digraph[node_index] = set([])
    for node_index in range(num_nodes):
        for item in digraph[node_index]:
            indegree_digraph[item].add(node_index)
    return indegree_digraph
    """
    indegree_digraph_v = {}
    # initialize indegree_digraph
    for key in digraph.keys():
        indegree_digraph_v[key] = set([])
    for key in digraph.keys():
        for item in digraph[key]:
            indegree_digraph_v[item].add(key)
    indegree_digraph_e = {}
    for key in digraph.keys():
        if len(indegree_digraph_v[key]) == 0:
            indegree_digraph_e[key] = 0
        else:
            indegree_digraph_e[key] = len(indegree_digraph_v[key])
    return indegree_digraph_e
#print compute_in_degrees(GRAPH4)


def in_degree_distribution(digraph):
    """
    Takes a directed graph digraph (represented as a dictionary) and 
    computes the unnormalized distribution of the in-degrees of the graph. 
    The function should return a dictionary whose keys correspond to 
    in-degrees of nodes in the graph. 
    The value associated with each particular in-degree is 
    the number of nodes with that in-degree. 
    In-degrees with no corresponding nodes in the graph 
    are not included in the dictionary.
    """
    indegree_digraph_v = {}
    # initialize indegree_digraph
    for key in digraph.keys():
        indegree_digraph_v[key] = set([])
    for key in digraph.keys():
        for item in digraph[key]:
            indegree_digraph_v[item].add(key)
    indegree_digraph_e = {}
    for key in digraph.keys():
        indegree_digraph_e[key] = len(indegree_digraph_v[key])
    
    indegree_dist = {}
    for key in indegree_digraph_e.keys():
        if indegree_digraph_e[key] not in indegree_dist.keys():
            indegree_dist[indegree_digraph_e[key]] = 1
        else:
            indegree_dist[indegree_digraph_e[key]] += 1
    return indegree_dist

#print in_degree_distribution(GRAPH1)