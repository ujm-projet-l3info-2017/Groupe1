import math

class Edge:
    start = None
    end = None
    weight = None

    def __init__(self, w, s, e):
        self.weight = w
        self.start = s
        self.end = e

    def __str__(self):
        s= "start: "+str(self.start)+" end: "+str(self.end)+" weight: "+str(self.weight)
        return s


class Graph:
    matrix = None
    vertices = []

    def __init__(self):
        self.matrix = dict()

    def insert_vertex(self, vertex):
        if not(vertex in self.matrix):
            print("coucou")
            self.matrix[vertex] = {key:-1 for key in self.matrix.keys()}
            for key in self.matrix.keys():
                self.matrix[key][vertex] = -1
        else:
            print("connard")    
        
    def insert_edge(self, edge):
        print(self.matrix)
        self.insert_vertex(edge.start)
        self.insert_vertex(edge.end)
        self.matrix[edge.start][edge.end] = edge

    def delete_edge(self, edge):
        self.matrix[edge.start][edge.end] = -1

    def successor(self, vertice):
        succ = []
        for i in range(len(self.matrix[vertice])):
            if(self.matrix[vertice][i] != -1):
                succ.append(self.matrix[vertice][i])
        return succ

    def all_vertices(self):
        return self.matrix.keys()
    
    def __str__(self):
        s = ""
        for i in range (len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if(self.matrix[i][j] == -1):
                    # if no edge 
                    s+= ".   "
                else:
                    s+= str(self.matrix[i][j].weight)+"   "
            s+="\n"
        return s

    def __len__(self):
        # always square matrix
        return len(self.matrix)


#return the range of the min
def min_list(l):
    min = 0
    for i in range(len(l)):
        if(l[i] < min):
            min = i
    return min

def dijkstra(graph, start, end):
    # vertices we need to test
    v = [i for i in range(len(graph))]
    dist = [math.inf for i in range(len(graph))]
    prev = [None for i in range(len(graph))]

    dist[start] = 0

    while(v):
        vertex = v[min_list(dist)]
        v.remove(vertex)
        if(vertex == end):
            way = list()
            while(prev[vertex] != None):
                way.append(vertex)
                vertex = prev[vertex]
            way.append(vertex)
            way.reverse()
            return way
                
                
        for succ in graph.successor(vertex):
            old = dist[vertex] + succ.weight
            if old < dist[succ.end]:
                dist[succ.end] = old
                prev[succ.end] = vertex    
            
    
a = Edge(2,0,1)
b = Edge(6,0,2)
c = Edge(8,0,3)
d = Edge(1,1,4)
e = Edge(2,4,2)
f = Edge(4,2,5)
g = Edge(2,2,3)
h = Edge(8,4,5)
i = Edge(3,3,5)
j = Edge(9,4,6)
k = Edge(1,5,6)
l = Edge(7,3,7)
m = Edge(2,6,7)
gr = Graph()
gr.insert_edge(a)
gr.insert_edge(b)
gr.insert_edge(c)
gr.insert_edge(d)
gr.insert_edge(e)
gr.insert_edge(f)
gr.insert_edge(g)
gr.insert_edge(h)
gr.insert_edge(i)
gr.insert_edge(j)
gr.insert_edge(k)
gr.insert_edge(l)
gr.insert_edge(m)
#print(str(len(gr)))
print(gr)
#print(gr.successor(0))
l = list(gr.all_vertices())


chemin = dijkstra(gr, 0,7)
#print(len(chemin))
for v in chemin:
    print(v)
 
