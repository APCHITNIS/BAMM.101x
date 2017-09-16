import matplotlib.pyplot as plt
import networkx as nx


# % matplotlib inline

def get_connection(graph, node, relationship):
    l = []
    for n, nbrs in graph.adjacency_iter():
        #         print(n)
        if n != node:
            continue
        l.append(node)
        for nbr, eattr in nbrs.items():
            data = eattr['source']
            if data == relationship:
                #                 print((n,nbr,data))
                l.append(nbr)
        for li in l:
            if li == node:
                continue
            # print("getting neighbours of " + li)
            l = get_edge_relation(graph, li, 'family', l)

    # print(str(l))
    return l


def get_edge_relation(graph, node, relationship, l):
    for n, nbrs in graph.adjacency_iter():
        if n != node:
            continue
        for nbr, eattr in nbrs.items():
            data = eattr['source']
            if data == relationship:
                #                 print(nbr)
                if nbr in l:
                    continue
                # print("appended: " + nbr)
                l.append(nbr)
    return l


def run():
    G = nx.Graph()
    nodes = ["Gur", "Qing", "Samantha", "Jorge", "Lakshmi", "Jack", "John", "Jill"]
    edges = [("Gur", "Qing", {"source": "work"}),
             ("Gur", "Jorge", {"source": "family"}),
             ("Samantha", "Qing", {"source": "family"}),
             ("Jack", "Qing", {"source": "work"}),
             ("Jorge", "Lakshmi", {"source": "work"}),
             ("Jorge", "Samantha", {"source": "family"}),
             ("Samantha", "John", {"source": "family"}),
             ("Lakshmi", "Jack", {"source": "family"}),
             ("Jack", "Jill", {"source": "charity"}),
             ("Jill", "John", {"source": "family"})]
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    pos = nx.circular_layout(G)  # positions for all nodes
    fig = plt.figure(1, figsize=(12, 12))  # Let's draw a big graph so that it is clearer
    node_name = {}
    for node in G.nodes():
        node_name[node] = str(node)
    nx.draw_networkx_labels(G, pos, node_name, font_size=16)
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), width=8, alpha=0.5, edge_color='b')
    nx.draw_networkx_edge_labels(G, pos, font_size=10)

    fig.show()

    for n in nx.nodes_iter(G):
        if n == "John":
            #         print('yey!')
            get_connection(G, n, 'family')
            break


run()