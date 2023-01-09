import networkx as nx
from graphToJson import getNetworkTimelineFromJson

# ler network timeline do arquivo do mês
network_timeline = []
inputJsonName = "finalMonth01score05.json"
getNetworkTimelineFromJson(network_timeline,inputJsonName)


colors_list = ['red','orange','yellow','darkgreen','lime','cyan','lightblue','blue','darkblue','lightpink','pink','lightpurple','purple']
communities_number = 5

f = open("pageRank.txt", "a")


for t,timestamp in enumerate(network_timeline):
    
    f.write("\nTimestamp "+str(t+1))
    f.write("\n----------------------------------------------------------")

    # get the communities by node color for each timestamp
    communities = []
    for i in range(communities_number):
        community = [node for node,value in timestamp.nodes(data=True) if value['color']==colors_list[i]]
        communities.append(community)

    # create a subgraph containing only the community nodes and the edges containing them
    for i,community in enumerate(communities):
        f.write("\nComunidade #"+str(i+1)+": \n\n")
        subgraph = timestamp.subgraph(community)
        pr = nx.pagerank(subgraph)

        # sort dictionary reversed by value
        pr = dict(sorted(pr.items(), key=lambda item: item[1], reverse= True))

        # get 10 best rankings
        for key in list(pr.keys())[0:10]:
            f.write(key+': '+str(pr[key])+' \n')

    f.write("----------------------------------------------------------")

f.close()
