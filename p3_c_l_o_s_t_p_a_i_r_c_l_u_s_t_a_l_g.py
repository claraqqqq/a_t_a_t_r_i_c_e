"""
Template for Project 3
Student will implement four functions:

slow_closest_pairs(cluster_list)
fast_closest_pair(cluster_list) - implement fast_helper()
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

where cluster_list is a list of clusters in the plane
"""

import math
import alg_cluster



def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function to compute Euclidean distance between two clusters
    in cluster_list with indices idx1 and idx2
    
    Returns tuple (dist, idx1, idx2) with idx1 < idx2 where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), idx1, idx2)


def slow_closest_pairs(cluster_list):
    """
    Compute the set of closest pairs of cluster in list of clusters
    using O(n^2) all pairs algorithm
    
    Returns the set of all tuples of the form (dist, idx1, idx2) 
    where the cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.   
    
    """
    length = len(cluster_list)
    dist_dict = {}
    for index1 in range(length):
        for index2 in range(index1+1, length):
            dist = cluster_list[index1].distance(cluster_list[index2])
            if dist not in dist_dict.keys():
                dist_dict[dist]=[(index1, index2)]
            else:
                dist_dict[dist].append((index1, index2))
    #print dist_dict
    min_dist = min(dist_dict)
    dist_pairs = dist_dict[min_dist]
    #print min_dist
    #print dist_pairs[0][1]
    result = set([])
    for index in range(len(dist_pairs)):
        result.add((min_dist, dist_pairs[index][0], dist_pairs[index][1]))
    return result

#print slow_closest_pairs([alg_cluster.Cluster(set([]), 0, 0, 1, 0), alg_cluster.Cluster(set([]), 1, 0, 1, 0)]) 
#expected set([(1.0, 0, 1)]) 

#print slow_closest_pairs([alg_cluster.Cluster(set([]), 0, 0, 1, 0), alg_cluster.Cluster(set([]), 0, 1, 1, 0), alg_cluster.Cluster(set([]), 0, 2, 1, 0)]) 
#expected set([(1.0, 0, 1), (1.0, 1, 2)]) 

def fast_closest_pair(cluster_list):
    """
    Compute a closest pair of clusters in cluster_list
    using O(n log(n)) divide and conquer algorithm
    
    Returns a tuple (distance, idx1, idx2) with idx1 < idx 2 where
    cluster_list[idx1] and cluster_list[idx2]
    have the smallest distance dist of any pair of clusters
    """
        
    def fast_helper(cluster_list, horiz_order, vert_order):
        """
        Divide and conquer method for computing distance between closest pair of points
        Running time is O(n * log(n))
        
        horiz_order and vert_order are lists of indices for clusters
        ordered horizontally and vertically
        
        Returns a tuple (distance, idx1, idx2) with idx1 < idx 2 where
        cluster_list[idx1] and cluster_list[idx2]
        have the smallest distance dist of any pair of clusters
    
        """
        
        # base case
        if len(horiz_order) <= 3:
            #cluster_q = [cluster_list[index] for index in horiz_order]
            result_bc = slow_closest_pairs([cluster_list[index] for index in horiz_order])
            return (list(result_bc)[0][0], horiz_order[list(result_bc)[0][1]], horiz_order[list(result_bc)[0][2]])
        
        # divide
        half = len(horiz_order)/2 
        mid = 1.0 / 2 * (cluster_list[horiz_order[half-1]].horiz_center() + cluster_list[horiz_order[half]].horiz_center())

        horiz_order_left = horiz_order[0:half]
        horiz_order_right = horiz_order[half:len(horiz_order)]
        vert_order_left = []
        vert_order_right = []
        
        for index in vert_order:
            if index in horiz_order_left:
                vert_order_left.append(index)
            else:
                vert_order_right.append(index)        
        
        result_l = fast_helper(cluster_list, horiz_order_left, vert_order_left)        
        result_r = fast_helper(cluster_list, horiz_order_right, vert_order_right)
        
        if result_l[0] < result_r[0]:
            result_min = result_l
        else:
            result_min = result_r
        
        # conquer
        ss_index = []
        for index in vert_order:
            if abs(cluster_list[index].horiz_center()- mid) < result_min[0]:
                ss_index.append(index) 

        for dummy_u in range(len(ss_index)-1):
            for dummy_v in range(dummy_u+1, min(dummy_u+4, len(ss_index))):
                dummy_dd_t = cluster_list[ss_index[dummy_u]].distance(cluster_list[ss_index[dummy_v]])
                if dummy_dd_t < result_min[0]:
                    result_min = (dummy_dd_t, ss_index[dummy_u], ss_index[dummy_v])
        return result_min
            
    # compute list of indices for the clusters ordered in the horizontal direction
    hcoord_and_index = [(cluster_list[idx].horiz_center(), idx) 
                        for idx in range(len(cluster_list))]    
    hcoord_and_index.sort()
    horiz_order = [hcoord_and_index[idx][1] for idx in range(len(hcoord_and_index))]
     
    # compute list of indices for the clusters ordered in vertical direction
    vcoord_and_index = [(cluster_list[idx].vert_center(), idx) 
                        for idx in range(len(cluster_list))]    
    vcoord_and_index.sort()
    vert_order = [vcoord_and_index[idx][1] for idx in range(len(vcoord_and_index))]

    # compute answer recursively
    answer = fast_helper(cluster_list, horiz_order, vert_order) 
    return (answer[0], min(answer[1:]), max(answer[1:]))

                
def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function mutates cluster_list
    
    Input: List of clusters, number of clusters
    Output: List of clusters whose length is num_clusters
    """
    
    while len(cluster_list) > num_clusters:
        result = fast_closest_pair(cluster_list)
        #print 'result',result
        cluster1 = result[1]
        cluster2 = result[2]
        cluster_list[cluster1].merge_clusters(cluster_list[cluster2])
        del cluster_list[cluster2] 
        #print 'cluster_list',cluster_list
    return cluster_list


def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function mutates cluster_list
    
    Input: List of clusters, number of clusters, number of iterations
    Output: List of clusters whose length is num_clusters
    """
    
    # initialize k-means clusters to be initial clusters with largest populations
    
    population_and_index = [(cluster_list[idx].total_population(), idx)
                             for idx in range(len(cluster_list))]
    population_and_index.sort()
    population_and_index.reverse()
    
    mean_cluster = [(cluster_list[population_and_index[idx][1]].horiz_center(),
                     cluster_list[population_and_index[idx][1]].vert_center()) 
                    for idx in range(num_clusters)]

    for dummy_idx in range(num_iterations):
        
        cluster_mean_list = []
        cluster_new_list = []
        
        for idx in range(num_clusters):
            cluster_mean_list.append(alg_cluster.Cluster(set([]), mean_cluster[idx][0], mean_cluster[idx][1], 0, 0))
            cluster_new_list.append(alg_cluster.Cluster(set([]), mean_cluster[idx][0], mean_cluster[idx][1], 0, 0))
        
        for idx1 in range(len(cluster_list)):           
            rcrd = []
            for idx2 in range(num_clusters):
                rcrd.append((cluster_list[idx1].distance(cluster_mean_list[idx2]), idx2))
            cluster_new_list[min(rcrd)[1]].merge_clusters(cluster_list[idx1])
        
        mean_cluster = [(cluster_new_list[idx].horiz_center(), cluster_new_list[idx].vert_center()) 
                        for idx in range(num_clusters)]   
    return cluster_new_list
    

    