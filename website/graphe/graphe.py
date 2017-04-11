import math

class Arc:
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

    def __init__(self, nb_line_column):
        self.matrix = [[-1]*nb_line_column for i in range(nb_line_column)]

    def insert_arc(self, arc):
        self.matrix[arc.start][arc.end] = arc
        self.vertices.append(arc)

    def delete_arc(self, arc):
        self.matrix[arc.start][arc.end] = None

    def successor(self, vertice):
        succ = []
        for i in range(len(self.matrix[vertice])):
            if(self.matrix[vertice][i] != -1):
                succ.append(self.matrix[vertice][i])
        return succ

    def allVertices(self):
        return self.vertices
    
    def __str__(self):
        s = ""
        for i in range (len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if(self.matrix[i][j] == -1):
                    # if no arc 
                    s+= ".   "
                else:
                    s+= str(self.matrix[i][j].weight)+"  "
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
            
    
a = Arc(2,0,1)
b = Arc(6,0,2)
c = Arc(8,0,3)
d = Arc(1,1,4)
e = Arc(2,4,2)
f = Arc(4,2,5)
g = Arc(2,2,3)
h = Arc(8,4,5)
i = Arc(3,3,5)
j = Arc(9,4,6)
k = Arc(1,5,6)
l = Arc(7,3,7)
m = Arc(2,6,7)
gr = Graph(8)
gr.insert_arc(a)
gr.insert_arc(b)
gr.insert_arc(c)
gr.insert_arc(d)
gr.insert_arc(e)
gr.insert_arc(f)
gr.insert_arc(g)
gr.insert_arc(h)
gr.insert_arc(i)
gr.insert_arc(j)
gr.insert_arc(k)
gr.insert_arc(l)
gr.insert_arc(m)
#print(str(len(gr)))
print(gr)
#print(gr.successor(0))
l = list(gr.allVertices())


chemin = dijkstra(gr, 0,7)
#print(len(chemin))
for v in chemin:
    print(v)
 
