class Edge():
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


class Graph():
    matrix = None

    def __init__(self):
        self.matrix = dict()

    def insert_vertex(self, vertex):
        if not(vertex in self.matrix):
            self.matrix[vertex] = {key:-1 for key in self.matrix.keys()}
            for key in self.matrix.keys():
                self.matrix[key][vertex] = -1
        
    def insert_edge(self, edge):
        self.insert_vertex(edge.start)
        self.insert_vertex(edge.end)
        self.matrix[edge.start][edge.end] = edge

    def delete_edge(self, edge):
        self.matrix[edge.start][edge.end] = -1

    def successor(self, vertice):
        succ = []
        for i in self.matrix[vertice].keys():
            if(self.matrix[vertice][i] != -1):
                succ.append(self.matrix[vertice][i])
        return succ

    def all_vertices(self):
        return self.matrix.keys()

    def __len__():
        return len(self.matrix.keys())

    def dijkstra(self, start, end):
        # vertices we need to test
        v = [key for key in self.matrix.keys()]
        dist = {key: float("inf") for key in self.matrix.keys()}
        prev = {key: None for key in self.matrix.keys()}
        dist[start] = 0

        while(v):
            vertex = argmin(dist, v)
            v.remove(vertex)
            
            for succ in self.successor(vertex):
                old = dist[vertex] + succ.weight
                if old < dist[succ.end]:
                    dist[succ.end] = old
                    prev[succ.end] = vertex

        way = list()
        vertex = end
        while(prev[vertex] != None):
            weight = self.matrix[vertex].weight
            way.append((vertex, weight))
            vertex = prev[vertex]
        weight = self.matrix[vertex].weight
        way.append((vertex, weight))
        way.reverse()
        return way
            
    
    def __str__(self):
        s = ""
        print(len(self.matrix))
        for i in self.matrix.keys():
            for j in self.matrix[i].keys():
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


# argmin for a dict which contains integers
# Note: the element in l must be in s
def argmin(l, s):
    m = float("inf")
    arg = None
    for key in l.keys():
        if(l[key] < m and key in s):
            m = l[key]
            arg = key
    return arg

a = Edge(2,"E", "B")
b = Edge(6,"E","A")
c = Edge(8,"E","C")
d = Edge(1,"B","D")
e = Edge(2,"D","A")
f = Edge(4,"A","F")
g = Edge(2,"A","C")
h = Edge(8,"D","F")
i = Edge(3,"F","C")
j = Edge(9,"D","G")
k = Edge(1,"F","G")
l = Edge(7,"C","H")
m = Edge(2,"G","H")
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


chemin = gr.dijkstra("E","H")
print(chemin)
#for v in chemin:
#    print(v)
 
