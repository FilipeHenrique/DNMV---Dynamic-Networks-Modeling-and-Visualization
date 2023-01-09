import networkx as nx
from networkx.readwrite import json_graph
import json
from report import *

def generateTimelineJson(network_timeline,json_name):

    json_file = open(json_name, "a")

    # starts writing the json
    json_file.write('{"graphTimeline": [')

    # divide comunidades em temporal clustering
    tc = temporalClustering(network_timeline)
    colorizeTemporalClustering(network_timeline,tc)

    # add each snapshot as a json object
    for i,network in enumerate(network_timeline):

        nodes = network.number_of_nodes()
        edges = network.number_of_edges()

        # report (relatório)
        # get communities with louvain (need undirected graph)
        communities_list = get_communities(network)

        #generate directed network to get report
        directed_network = nx.DiGraph(network)
        modularity = get_modularity(directed_network,communities_list)
        average_degree = get_average_degree(directed_network)
        average_weight = get_average_weight(directed_network)
        average_clustering = get_average_clustering(directed_network)

        # generate network JSON according to networkx docs via dictionary model
        dictionary = dict(source='source', target='target', name='id',key='key', link='links')
        graph_data_toJSON = json_graph.node_link_data(directed_network,dictionary)

        graph_data_toJSON["nodesNumber"] = nodes
        graph_data_toJSON["edgesNumber"] = edges
        graph_data_toJSON["averageDegree"] = average_degree
        graph_data_toJSON["averageWeight"] = average_weight
        graph_data_toJSON["averageClustering"] = average_clustering

        json_object = json.dumps(graph_data_toJSON)
        json_file.write(json_object)

        if i < len(network_timeline)-1:
            json_file.write(',')
    
    json_file.write(']}')
    json_file.close()

# generate json with filtered snapshots (first step of the pipeline), save processing time for later tests
def alphaCutJson(network_timeline,json_name):
        json_file = open(json_name, "a")
        json_file.write('{"graphTimeline": [')
        for i,network in enumerate(network_timeline):
            graph_data_toJSON = json_graph.node_link_data(network)
            json_object = json.dumps(graph_data_toJSON)
            json_file.write(json_object)
            if i < len(network_timeline)-1:
                json_file.write(',')
        json_file.write(']}')

# load snapshots from a previously generated JSON
def getNetworkTimelineFromJson(network_timeline,json_name):
    f = open(json_name)
    data = json.load(f)
    for network in data['graphTimeline']:
        new_network = json_graph.node_link_graph(network)
        network_timeline.append(new_network)