class Edge():
    """
    An Egde (with a start, an end and a weight)
    """
    start = None
    end = None
    weight = None

    def __init__(self, w, s, e):
        """
        Initialize an edge with a weight, a start and an end
        """
        self.weight = w
        self.start = s
        self.end = e

    def __str__(self):
        s= "start: "+str(self.start)+" end: "+str(self.end)+" weight: "+str(self.weight)
        return s


class Graph():
    """
    The class Graph represent ... a graph
    """
    matrix = None

    def __init__(self):
        """
        Initialize a matrix
        """
        self.matrix = dict()

    def insert_vertex(self, vertex):
        """
        Insert a vertex in the graph
        """
        # If the vertex doesn't exist in the graph
        if not(vertex in self.matrix):
            # We create a row for this vertex in the matrix
            self.matrix[vertex] = {key:-1 for key in self.matrix.keys()}
            # And the extend columns for the other vertex
            for key in self.matrix.keys():
                self.matrix[key][vertex] = -1
        
    def insert_edge(self, edge):
        """
        We insert an edge in the graph
        """
        self.insert_vertex(edge.start)
        self.insert_vertex(edge.end)
        self.matrix[edge.start][edge.end] = edge

    def delete_edge(self, edge):
        """
        We delete an edge in the graph
        """
        self.matrix[edge.start][edge.end] = -1

    def successor(self, vertice):
        """
        Compute the successors of a vertex 
        """
        succ = []
        for i in self.matrix[vertice].keys():
            if(self.matrix[vertice][i] != -1):
                succ.append(self.matrix[vertice][i])
        return succ

    def all_vertices(self):
        """
        Get the vertices
        """
        return self.matrix.keys()

    def __len__():
        return len(self.matrix.keys())

    def dijkstra(self, start, end):
        """
        Compute the shortest path in the graph
        """
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
        way_weight = list()
        vertex = end

        while(prev[vertex] != None):
            way.append(vertex)
            vertex = prev[vertex]
        way.append(vertex)
        way.reverse()
        for i in range(len(way)-1):
            weight = self.matrix[way[i]][way[i+1]].weight
            way_weight.append(weight)
        return way, way_weight
            
    
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

def argmin(l, s):
    """
    Compute the argmin for a dict which contains integers
    Note: the element in l must be in s
    """
    m = float("inf")
    arg = None
    for key in l.keys():
        if(l[key] <= m and key in s):
            m = l[key]
            arg = key
    return arg

