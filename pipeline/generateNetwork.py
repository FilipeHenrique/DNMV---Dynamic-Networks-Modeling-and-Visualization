import backbone

# p value for disparity filter
alpha_t = 0.1


def print_nodes_and_edges(G):
    nodes = G.number_of_nodes()
    edges = G.number_of_edges()
    print('-----',nodes,'\t nós.')
    print('-----',edges,'\t arestas.')

def clean_neighborhood(network):
    # limpa nós com grau 1 isolados na periferia
    nodes_to_remove = []
    for node,degree in dict(network.degree()).items():
        if degree == 0:
            nodes_to_remove.append(node)
        if degree == 1:
            node2 = list(network.edges(node, data=True))[0][1]
            if network.degree[node2] == 1:
                nodes_to_remove.append(node)
                nodes_to_remove.append(node2)
    network.remove_nodes_from(nodes_to_remove)
    return network

def get_alpha_cut_network(network,alpha_t):
    print('\nRede de Entrada')
    print_nodes_and_edges(network)

    print('Alpha T:',alpha_t)
    X = backbone.disparity_filter(network)

    X = backbone.disparity_filter_alpha_cut(X,alpha_t)

    print('Pós Alpha Cut')
    print_nodes_and_edges(X)

    return X

def generate_network_snapshots(G,timestamps_list,inputFileName):
    # list to store each network in the timeline
    network_list = []

    file = open(inputFileName,"r")

    # variables for loop control
    # get last element of timestamps_list to be the limit in the file loopover
    limit = timestamps_list[-1]

    # taking in consideration file index starting from 1 (line 1)
    count = 1

    while count <= limit:
        line = file.readline()
        words = line.split("\t")
        words[2] = words[2].rstrip("\n")

        # separate nodes and timestamps
        node1 = words[0]
        node2 = words[1]

        if node1 not in list(G.nodes):
            G.add_node(node1)
        if node2 not in list(G.nodes):
            G.add_node(node2)
        
        if (node1,node2) not in G.edges():
            G.add_edge(node1,node2,weight= 1)
        else: 
            G[node1][node2]['weight'] += 1

        count += 1
        
        # if reachedd one of the timestamps
        if count in timestamps_list:
            # apply alhpa cut and clean neighborhood
            new_network = G.copy()

            
            filtred_network = clean_neighborhood(get_alpha_cut_network(new_network,alpha_t))

            print('Rodou Limpeza de periferia de nós:')
            print_nodes_and_edges(filtred_network)
            print('\n')

            network_list.append(filtred_network)
    
    return network_list