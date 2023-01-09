import networkx as nx
from graphToJson import generateTimelineJson,alphaCutJson,getNetworkTimelineFromJson
from generateNetwork import *


# initial network
G = nx.Graph()

# list of file indexes where a given timestamp finishes, considering index starting from 1

# test modeling first week

# timestamps_list = [
#     90875,  # quarta maio 27
#     195456, # quinta maio 28
#     235874, # sexta jun 05
#     251522, # sábado junho 06
#     267672, # domingo junho 07
#     277580, # segunda junho 08
#     289910, # terça junho 09
#     300328, # quarta junho 10
# ]


# # test modeling as 4 weeks
timestamps_list = [
    300328,
    475977, # Sat Jun 20
    557909, # Thu Jul 30
    718650 # EOF
]


# -------------- EM CASO DE NÃO TER FEITO A FILTRAGEM E SALVO EM JSON PREVIAMENTE ----------------------

# lê rede do arquivo e filtra com disparity filter e alphaCut
inputFileName = "stf_retweets_timestamp.txt"
network_timeline = generate_network_snapshots(G,timestamps_list,inputFileName)

# gera o JSON que contém a lista dos snapshots pós alpha cut (tal processo é útil pois a modelagem
# e filtragem podem demorar, e caso seja necessário testar diferentes divisões de comunidade repetir o 
# processo nessa etapa é desnecessário)
outputJsonName = 'snapshotsMonth01.json'
alphaCutJson(network_timeline,outputJsonName)

generateTimelineJson(network_timeline,"finalMonth01score05.json")
#---------------------------------------------------------------------------------------------------------


# -------------- EM CASO DE JÁ TER FEITO A FILTRAGEM E SALVO EM JSON PREVIAMENTE ----------------------
# # carrega a lista de snapshots de um JSON já pronto
# network_timeline = []
# inputJsonName = 'snapshotsMonth01.json'
# getNetworkTimelineFromJson(network_timeline,inputJsonName)

# # realiza divisão em comunidades e gera o JSON para consumo no front end 
# outputWithCommunitiesName = "finalMonth01score06.json"
# generateTimelineJson(network_timeline,outputWithCommunitiesName)
#---------------------------------------------------------------------------------------------------------
