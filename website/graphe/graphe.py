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
                succ.append(i)
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

def min_list(l):
    min = 0
    for i in range(len(l)):
        if(l[i] < min):
            min = i
    return min

def dijkstra(graph, start, end):
    # vertices we need to test
    v = list(graph.allVertices())
    dist = [math.inf for i in range(len(graph))]
    prev = [None for i in range(len(graph))]

    dist[start] = 0

    while(v):
        vertex = v[min_list(dist)]
        v.remove(vertex)

        for succ in 
        
    
            
    
a = Arc(50,0,1)
b = Arc(30,0,2)
c = Arc(20,1,3)
d = Arc(15,1,4)
e = Arc(10,1,6)
f = Arc(15,2,4)
g = Arc(10,2,5)
h = Arc(20,2,6)
i = Arc(15,3,7)
j = Arc(30,4,7)
k = Arc(10,5,7)
l = Arc(25,6,7)
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
print(str(len(gr)))
print(gr)
print(gr.successor(0))
l = list(gr.allVertices())
for v in l:
    print(v)
