
def get_connections(graph, node, relationship):
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
    #Here's the grph to look at-
    import networkx as nx
    G = nx.Graph()
    nodes = ["Gur","Qing","Samantha","Jorge","Lakshmi","Jack","John","Jill"]
    edges = [("Gur","Qing",{"source":"work"}),
             ("Gur","Jorge", {"source":"family"}),
             ("Samantha","Qing", {"source":"family"}),
             ("Jack","Qing", {"source":"work"}),
             ("Jorge","Lakshmi", {"source":"work"}),
             ("Jorge","Samantha",{"source":"family"}),
             ("Samantha","John", {"source":"family"}),
             ("Lakshmi","Jack", {"source":"family"}),
             ("Jack","Jill", {"source":"charity"}),
             ("Jill","John",{"source":"family"})]
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    for n in nx.nodes_iter(G):
        if n == "John":
            #         print('yey!')
            l = get_connections(G, n, 'family')
            print(l)
            break


run()