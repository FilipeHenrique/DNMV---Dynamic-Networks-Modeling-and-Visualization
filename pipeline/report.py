import networkx as nx
from cdlib import algorithms, evaluation, NodeClustering, TemporalClustering

# communities number to be taken from louvain to be used in temporal clustering
communities_number = 5

# score to be taken in consideration, starting from the value set
score_lower_limit = 0.5

def get_communities(network):
    communities = algorithms.louvain(network, weight='weight', resolution=1.)
    return communities

def get_average_degree(network):
    average_degree = "{:.2f}".format(sum([d for (n, d) in nx.degree(network)]) / float(network.number_of_nodes()))
    print('Average Degree:',average_degree)
    return average_degree
    
def get_average_weight(network):
    get_average_weight = "{:.2f}".format(sum(nx.get_edge_attributes(network, 'weight').values()) / float(network.number_of_edges()))
    print('Average Weight:',get_average_weight)
    return get_average_weight

def get_average_clustering(network):
    average_clustering = "{:.2f}".format(nx.average_clustering(network))
    print('Average Clustering:',average_clustering)
    return average_clustering

def get_modularity(network,communities):
    modularity = evaluation.newman_girvan_modularity(network,communities)
    print('Modularidade:',modularity)
    return "{:.2f}".format(modularity[2])

def temporalClustering(network_timeline):
    communities_files = []
    for observation,network in enumerate(network_timeline):
        communities_files.append([]) #append da observação
        communities_list = list(get_communities(network).communities[0:communities_number])
        for community in communities_list:
            communities_files[observation].append(community) # append das comunidades na observação

    node_clustering = {}
    for observation in range(len(network_timeline)):
        communities_obs = []
        for community in range(len(communities_files[observation])):
            communities_obs.append(communities_files[observation][community])
            node_clustering[observation] = NodeClustering(communities_obs, graph=None, method_name="")
    
    tc = TemporalClustering()
    for observation in node_clustering:
        tc.add_clustering(node_clustering[observation],observation)

    jaccard = lambda x, y: len(set(x) & set(y)) / len(set(x) | set(y))
    matching = tc.community_matching(jaccard,two_sided=True)
    tc.add_matching(matching)

    return tc

def colorizeTemporalClustering(network_timeline,tc):
    colors_dict = {}
    timestamps_number = len(network_timeline)
    colors_list = ['red','orange','yellow','darkgreen','lime','cyan','lightblue','blue','darkblue','lightpink','pink','lightpurple','purple']
    color_count = 0
    explicit_match = tc.get_explicit_community_match()

    # color the dict    
    for tuple in explicit_match:
        t_c1 = tuple[0]
        t_c2 = tuple[1]
        score = tuple[2]

        if score >= score_lower_limit:
            if t_c1 in colors_dict.keys():
                colors_dict[t_c2] = (colors_dict[t_c1])
            else:
                colors_dict[t_c1] = (colors_list[color_count])
                colors_dict[t_c2] = (colors_list[color_count])
                color_count+=1

    print('Match: ',explicit_match)
    print('Cores: ',colors_dict)
    # color the nodes
    # start all nodes as grey
    for i in range(timestamps_number):
        nx.set_node_attributes(network_timeline[i],'grey',name="color")
    for t_c in colors_dict:
        color = colors_dict[t_c]
        t = int(t_c.split('_')[0])
        for node in tc.get_community(t_c):
            nx.set_node_attributes(network_timeline[t],{node: color},name="color")