from typing import Dict, List, Set, Tuple


class Node:
    def __init__(self,i,j) -> None:          
        self.i = i
        self.j = j            

    def getPos(self) -> Tuple[int,int]:
        return (self.i,self.j)


class Graph:

    def __init__(self,grid) -> None:        
        self.nodes:Set[Node] = set()
        self.edges:Dict[Node,List[Node]] = {}
        self.posIndex:Dict[Tuple[int,int],Node] = {}
        
        # The graph is m rows by n columns
        self.m = len(grid)
        self.n = len(grid[0])
        
        self.buildGraph(grid)

    def checkPos(self,i:int,j:int) -> bool:
        if (i,j) in self.posIndex.keys(): return True
        else: return False

    def getNode(self,i:int,j:int) -> Node:
        if self.checkPos(i,j):
            return self.posIndex[(i,j)]
        else:
            raise ValueError(f"No node at pos i:{i} j:{j}")

    def getAttachedNodes(self,n:Node) -> list[Node]:
        return self.edges[n]

    def getDegree(self,n:Node) -> int:
        return len(self.edges[n])

    def addNode(self,n:Node): 
        if n not in self.nodes: 
            self.nodes.add(n)
            self.posIndex[n.getPos()] = n
            self.edges[n] = []

    def addEdge(self,n1:Node,n2:Node):
        if n1 not in self.edges[n2]:
            self.addNode(n1)
            self.addNode(n2)

            self.edges[n1].append(n2)
            self.edges[n2].append(n1)

    def buildGraph(self,grid):  

        #For i rows
        for i in range(self.m):

            #For j columns
            for j in range(self.n):

                if grid[i][j] == 0: continue

                n = Node(i,j)
                self.addNode(n)

        for n in self.nodes:
            i,j = n.getPos()

            for h in -1,1:
                self.checkConnectivity(i+h, j, n)

            for v in -1,1:
                self.checkConnectivity(i, j+v, n)

    def checkConnectivity(self, i, j, n1:Node) -> None:
        if self.checkPos(i,j):
            n2 = self.getNode(i,j)
            self.addEdge(n1,n2)
    
    def printGraph(self) -> None:
        hl = '-'
        vl = '|'

        pos = [[' ' for c in range(self.n*2-1)] for r in range(self.m*2-1)]

        for n in self.nodes:
            i,j = n.getPos()
            i *= 2
            j *= 2
            pos[i][j] = 1

            for edge in self.getAttachedNodes(n):
                di,dj = edge.getPos()
                
                di *= 2
                dj *= 2

                ai = int((i + di)/2)
                aj = int((j + dj)/2)

                #If the edge is horizontal
                if i == di:
                    pos[ai][aj] = hl

                #If the edge is vertical
                elif j == dj:
                    pos[ai][aj] = vl

            #print(n.getPos(),':',[e.getPos() for e in self.getEdges(n)])
            #print(i,':',pos[i])
            #if i + 1 <= self.m: print(i+1,':',pos[i+1])

        print("\n".join(map(lambda l: "".join(map(str, l)), pos)))
    

    def getPerimeter(self) -> int:
        self.printGraph()
        p = 0 
        for n in self.nodes:
            p += 4 - self.getDegree(n)

        return p


def islandPerimeter(grid: List[List[int]]) -> int:
    G = Graph(grid)
    return G.getPerimeter()



import unittest

#Testcases
class TestFloodFill(unittest.TestCase):
    
    def test1(self):
        grid = [[0,1,0,0],[1,1,1,0],[0,1,0,0],[1,1,0,0]]
        perimiter = 16
        self.assertEqual(islandPerimeter(grid),perimiter)

    def test2(self):
        grid = [[1]]
        perimiter = 4
        self.assertEqual(islandPerimeter(grid),perimiter)

    def test3(self):
        grid = [[1,0]]
        perimiter = 4
        self.assertEqual(islandPerimeter(grid),perimiter)

if __name__ == '__main__':
    #unittest.main()

    import cProfile
    grid = [[1,1,1,1,1,1,1,1,0,0,1,1,1,0,0,1,1,1,0,0,1,1,1,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,0,0,1,1,1,0,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,0,0,1,0,1,1,1,1,0,1,1,1,0,0],[1,0,0,0,1,0,0,1,1,0,1,0,1,1,1,1,0,1,1,0,0,0,0,0,1,1,1,0,0,1,0,0,0,1,0,1,1,1,0,1,0,0,1,0,0,1,0,1,1,1,0,1,1,0,0,0,1,1,1,1,0,1,0,0,0,1,0,1,1,1,0,0,0,1,1,1,0,1,0,0,0,0,0,0,0,1,1,0,1,0,1,0,0,1,1,1,0,1,1,0],[1,1,1,0,1,1,0,0,0,0,1,0,0,0,1,0,0,0,1,1,1,1,1,1,1,0,1,1,0,1,0,1,0,1,0,0,1,0,0,1,0,1,1,1,0,0,0,0,1,0,0,0,1,1,1,0,0,0,0,0,0,1,0,1,1,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,1,1,1,0,0,0,1,0,1,1,1,1,0,1,0,1,0,0,1,1],[0,0,1,0,0,1,1,1,0,1,1,1,0,0,1,1,0,0,0,1,0,0,0,0,0,0,0,1,1,1,0,1,1,1,0,1,1,0,0,1,0,0,0,1,1,0,0,0,1,0,1,1,1,0,1,0,0,1,1,1,0,0,0,1,0,0,0,0,1,0,1,1,1,0,0,1,0,1,0,1,1,0,1,1,1,0,1,1,1,0,0,0,0,0,0,1,0,0,1,0],[0,1,1,1,0,0,0,1,1,1,0,1,1,0,0,1,1,1,0,1,0,1,1,1,1,0,0,0,0,0,0,1,0,0,0,1,0,0,1,1,1,1,0,0,1,1,0,1,1,0,0,0,0,0,1,0,1,1,0,1,1,0,1,1,0,1,1,1,1,0,1,0,1,1,0,1,0,1,0,1,0,0,0,0,1,0,0,0,1,0,0,1,1,1,1,1,0,1,1,1],[1,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,1,1,1,1,0,1,0,1,0,1,1,1,1,0,0,0,1,0,0,0,0,1,0,1,0,0,1,1,1,0,1,0,1,0,0,0,1,1,1,0,0,1,0,1,0,0,1,0,0,1,1,1,0,1,0,1,1,1,0,1,1,1,0,1,1,0,1,1,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,1,1,1,1,0,1,1,1,1,0,1,1,0,0,1,1,1,0,1,0,0,1,0,1,0,1,0,0,1,0,1,1,0,1,1,1,0,1,0,1,0,1,0,1,1,0,1,0,1,1,1,1,1,0,0,1,0,0,0,0,0,1,0,1,1,1,0,0,0,1,1,1,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0,1,1,1,1,1,1,1],[1,1,0,0,1,1,1,0,0,1,1,1,0,0,1,0,0,1,0,1,1,0,1,0,0,0,0,1,0,1,0,1,1,0,0,0,0,1,0,0,0,1,0,1,1,1,0,1,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0,1,1,1,0,1,1,1,0,0,0,1,0,1,0,0,0,1,1,1,0,1,1,1,1,0,0,1,1,0,1,1,0,0,0,0,0,1],[0,0,0,1,1,0,0,0,0,0,0,0,0,1,1,0,0,1,1,1,0,0,0,0,1,1,1,1,0,1,0,0,1,1,0,0,0,1,0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,0,0,1,1,1,0,1,0,1,1,1,0,1,0,0,0,1,0,1,1,1,0,0,0,1,0,1,0,0,0,0,0,0,1,1,0,1,0,0,0,1,0,1,1,1,0,0],[1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,0,1,1,0,0,0,0,0,1,1,0,0,0,0,1,1,0,0,1,1,0,1,1,0,1,0,0,0,0,1,1,1,0,0,1,1,1,0,0,1,1,0,1,1,1,1,1,0,1,0,1,1,1,0,1,0,1,0,1,1,0,1,1,1,1,0,1,1,0,1,0,0,1,0,1,1,1,0,0,0,1,0,1,1,1],[0,1,0,1,0,1,1,1,1,1,1,1,0,1,0,0,0,1,0,1,1,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,1,0,0,1,1,1,1,1,1,0,1,1,1,1,0,1,1,0,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,0,1,0,0,1,1,1,0,0,0,0,0,1,1,1,0,0,1,0,1,0,1,1,1,1,1,0,0,1,0],[1,1,0,0,0,0,0,0,1,0,0,1,0,1,1,1,0,1,1,1,0,0,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,0,1,0,1,0,1,1,1,1,0,0,0,0,1,1,0,1,1,1,1,0,0,0,0,0,1,1,1,0,0,1,0,0,1,1,0,1,0,0,1,0,1,0,0,0,1,1],[0,1,1,1,1,1,0,0,1,1,0,0,0,0,0,1,0,0,0,1,1,0,1,0,1,0,0,1,0,0,1,0,1,1,1,1,0,0,1,1,1,1,0,0,1,1,0,1,0,0,0,0,0,1,1,0,1,0,1,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,0,1,0,1,0,1,1,0,1,1,0,0,1,1,0,0,0,1,1,0,1,1,0],[0,0,0,0,0,1,1,0,0,1,1,1,1,0,0,1,1,1,0,1,0,0,1,0,1,1,0,1,1,0,1,1,1,0,0,1,1,1,1,0,0,1,1,0,0,1,1,1,0,1,1,1,1,1,0,0,1,0,1,1,0,0,0,0,0,0,0,0,1,1,1,1,0,1,1,0,1,1,1,0,1,0,1,0,0,1,0,0,0,0,1,1,0,0,0,0,0,1,0,0],[1,1,1,1,0,0,1,1,0,0,1,0,1,1,0,0,0,1,0,0,0,1,1,0,0,1,0,1,0,0,0,0,0,0,0,0,0,1,0,0,1,1,0,0,1,1,0,0,0,1,0,0,0,0,0,1,1,0,1,0,0,1,1,0,1,1,1,1,1,0,0,1,0,1,0,0,0,1,0,0,1,1,1,0,0,1,0,1,0,0,0,1,1,0,0,1,1,1,1,1],[0,1,0,0,0,0,0,1,1,0,1,0,0,1,0,1,1,1,0,0,1,1,0,0,1,1,0,1,0,1,1,1,1,0,0,1,0,1,1,0,0,0,0,1,1,0,0,1,1,1,0,1,1,1,1,1,0,0,1,1,0,0,1,1,1,0,0,0,0,0,1,1,0,1,1,1,0,1,1,0,0,0,1,1,0,1,0,1,1,1,0,0,1,0,1,1,0,1,0,1],[0,1,1,1,1,1,0,0,1,0,1,1,0,1,1,1,0,0,0,1,1,0,0,1,1,0,0,1,0,1,0,0,1,1,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,0,0,0,0,0,1,1,0,0,1,1,0,0,0,1,1,0,0,1,1,1,0,0,0,0,1,0,0,1,1,1,0,1,0,0,1,0,1,0,1,1,0,1,0,1,0,0,0,0,1],[1,1,0,0,1,0,0,1,1,0,1,0,0,0,0,0,0,0,1,1,0,0,1,1,0,0,0,1,0,1,1,0,0,1,0,1,1,0,0,1,1,1,1,0,0,1,1,0,0,1,1,1,1,1,0,0,1,1,0,0,1,1,1,0,0,1,1,0,0,0,0,0,0,0,1,1,1,0,1,0,1,0,0,0,1,1,0,1,0,0,1,0,1,0,1,0,1,0,1,1],[0,1,0,0,1,1,0,1,0,0,1,1,0,1,0,1,0,1,1,0,0,1,1,0,0,1,0,1,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,1,0,1,1,0,0,1,1,0,0,0,1,0,0,0,1,1,1,1,1,1,0,1,1,0,0,0,1,0,1,0,1,1,1,0,0,1,1,0,1,1,1,0,1,1,1,0,0,1],[1,1,1,0,1,0,0,1,0,0,0,1,1,1,1,1,0,1,0,0,0,0,1,0,1,1,0,1,1,1,0,0,0,1,0,0,0,1,1,0,1,1,1,0,0,1,0,0,0,0,1,1,0,0,1,1,1,1,0,0,1,0,1,1,0,0,1,0,1,0,0,1,0,1,0,0,1,0,0,0,1,1,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,1,0,1],[1,0,0,0,1,1,0,1,1,1,0,0,0,0,0,1,1,1,1,0,0,1,1,1,1,0,0,0,0,1,1,0,1,1,0,1,1,1,0,0,1,0,1,0,1,1,1,0,0,1,1,0,0,0,0,0,0,1,1,0,1,0,0,1,1,0,0,0,1,0,0,1,0,1,1,0,1,1,0,0,0,0,0,0,1,1,1,0,1,1,1,0,1,0,1,0,0,1,0,0],[1,1,0,1,1,0,0,0,0,1,1,0,0,1,0,0,0,0,0,0,1,1,0,1,0,0,1,1,0,0,1,0,1,0,0,0,0,0,0,1,1,0,1,1,1,0,0,0,1,1,0,0,0,1,1,0,0,0,1,1,1,1,0,0,1,1,0,0,0,0,1,1,0,0,1,0,0,1,0,1,1,1,1,0,0,1,0,0,0,0,1,0,1,1,1,1,0,1,1,1],[0,1,0,1,0,0,0,1,0,0,1,1,0,1,1,1,1,1,1,1,1,0,0,1,1,0,1,0,0,1,1,1,1,0,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,0,0,1,0,0,1,1,1,0,0,1,0,1,1,0,0,1,1,1,0,1,1,0,0,1,1,0,0,1,1,1,0,1,0,0,1,1,1,1,1,0,1,0,0,0,1,0,0,0,1,0],[1,1,0,1,1,1,1,1,1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,1,1,1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,1,1,0,1,1,1,0,0,1,1,1,0,0,1,0,0,0,1,0,0,0,0,0,0,0,1,0,1,0,0,1,1,0,0,1,1,0,0,0,1,1,0,0,0,1,0,1,0,1,0,1,1,1,1,1,0,1,1],[0,1,0,0,1,0,0,0,1,1,0,1,1,0,0,1,1,1,0,0,0,1,1,0,1,0,1,1,0,0,1,1,1,0,1,0,0,1,0,1,0,1,0,1,1,1,0,0,0,0,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,0,0,1,1,0,0,1,0,0,1,0,0,1,1,0,0,0,1,0,1,0,0,0,1,0,0,1],[1,1,1,0,1,1,0,0,0,0,0,0,1,1,0,1,0,1,1,0,0,0,1,1,1,0,0,1,0,1,1,0,0,0,1,1,0,1,1,1,0,1,0,0,0,1,1,0,0,1,1,0,0,1,1,1,0,0,1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,1,1,0,1,0,1,1,0,0,1,1,1,0,1,1,0,1,1,0,0,1],[1,0,0,0,0,1,1,1,1,1,1,0,0,1,1,1,0,0,1,1,1,0,0,0,1,1,0,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,0,1,0,0,1,1,0,0,1,0,0,0,0,0,0,1,1,1,0,1,1,0,1,0,0,1,1,1,0,1,1,0,1,1,1,1,0,0,1,1,1,1,1,0,0,1,1,0,0,0,0,1,0,0,0,0,1,1],[1,0,1,1,0,1,0,0,1,0,1,0,0,0,0,0,0,1,1,0,1,1,1,0,0,1,0,0,1,0,0,1,1,1,0,1,0,1,0,1,0,1,1,1,1,0,0,1,1,0,1,0,1,1,1,1,0,0,0,1,0,0,1,0,1,1,0,1,0,0,0,0,1,1,1,0,0,1,1,0,0,0,0,1,0,0,0,1,0,0,0,1,1,1,1,0,1,1,1,0],[1,1,1,0,0,1,1,0,1,0,0,0,1,1,1,1,0,0,0,0,1,0,1,1,0,1,1,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0,0,1,0,1,0,1,0,0,1,1,1,0,1,1,0,1,0,0,1,1,1,1,0,1,0,1,0,0,0,0,0,1,1,0,1,1,1,0,1,1,1,0,1,0,1,0,0,1,0,1,0,0,0],[1,0,1,0,0,0,0,0,1,1,1,0,1,0,0,1,1,1,0,0,1,0,0,1,0,0,1,1,0,0,1,1,0,1,1,1,0,1,1,1,1,1,0,0,1,1,0,1,1,0,1,0,1,1,0,0,0,1,0,0,0,0,1,1,0,1,0,0,1,1,1,0,1,1,0,1,1,0,0,1,0,0,1,0,0,1,0,0,0,1,1,1,1,0,1,0,1,1,1,1],[0,0,0,0,1,1,1,0,0,0,1,0,1,1,0,0,0,1,1,0,0,0,1,1,1,0,0,1,1,0,1,0,0,1,0,0,0,0,1,0,0,1,1,0,0,1,0,1,0,0,0,0,0,1,1,1,0,1,1,1,0,0,0,1,0,1,0,0,0,0,1,0,0,1,1,1,0,0,1,1,1,0,0,0,0,1,1,1,0,0,0,0,0,0,1,0,0,1,0,0],[1,1,1,1,1,0,1,1,0,1,1,0,0,1,1,1,0,0,1,1,1,0,0,0,1,0,0,0,1,1,1,0,0,1,1,1,0,1,1,1,0,0,1,0,0,1,0,1,1,1,0,1,0,1,0,1,0,0,0,1,0,1,1,1,0,0,0,1,1,0,1,1,0,0,0,0,0,1,1,0,1,1,0,1,0,0,0,1,1,0,0,1,1,1,1,1,0,1,1,1],[0,1,0,0,1,0,0,1,0,0,1,0,0,0,0,1,1,0,0,0,1,1,1,0,1,1,0,0,0,0,1,1,0,0,0,1,0,1,0,1,0,0,1,0,1,1,0,0,0,1,1,1,0,0,0,1,1,0,0,1,1,1,0,0,0,0,1,1,0,0,0,1,0,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,1,1,0,1,0,1,0,1,0,0,1,0],[1,1,1,0,0,0,1,1,0,1,1,1,1,1,0,0,1,1,0,0,0,0,1,0,0,1,1,1,0,0,0,0,0,0,1,1,0,1,0,1,0,1,1,0,1,0,0,1,0,0,0,1,1,0,0,0,1,1,0,0,0,0,0,1,1,1,1,0,0,1,1,1,1,1,0,1,1,1,0,0,0,0,1,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,1],[0,0,1,0,0,1,1,0,0,0,0,0,1,0,0,0,0,1,0,1,0,1,1,0,0,1,0,1,1,1,1,0,1,0,1,0,0,1,0,1,0,0,0,0,1,1,1,1,0,1,0,0,1,1,1,0,0,1,1,1,1,1,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,1,1,1,0,1,1,0,1,0,1,0,1,1,1,1,0,0,1],[1,1,1,0,1,1,0,0,1,0,0,1,1,0,1,1,1,1,0,1,1,1,0,0,1,1,0,1,0,0,1,1,1,0,1,0,0,0,0,1,1,1,0,0,0,0,0,1,1,1,0,0,0,0,1,0,0,0,0,0,1,0,0,1,1,0,0,1,1,0,0,1,1,0,1,0,0,0,1,1,0,1,1,0,1,1,1,0,0,1,0,1,0,1,0,0,1,1,0,1],[0,1,0,0,1,0,0,1,1,1,0,1,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,1,1,1,1,0,1,0,1,0,1,1,1,0,0,1,0,0,1,1,1,1,0,1,1,0,0,1,0,1,1,0,0,0,0,1,1,0,0,1,1,1,1,1,0,0,1,0,0,0,0,1,0,1,0,1,1,1,1,0,1,1,0,0,1,0,1],[1,1,0,1,1,0,1,1,0,1,1,1,0,0,1,1,1,1,1,0,1,0,1,1,1,0,1,1,1,1,0,1,1,1,1,0,0,1,0,0,0,1,1,1,0,1,1,1,1,0,1,1,0,0,1,1,1,0,0,1,1,0,1,0,0,1,1,0,0,1,0,1,1,0,0,0,1,1,0,1,1,1,1,0,1,0,1,1,1,0,0,1,0,0,1,0,1,1,1,1],[1,0,0,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,1,0,1,1,1,0,1,0,0,1,0,1,0,0,0,0,0,0,1,1,1,1,0,0,0,1,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,1,0,0,1,1,0,0,1,0,0,1,0,0,0,0,0,1,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,1,0,1,0,0,1],[1,0,0,1,1,1,0,1,1,1,0,0,1,1,1,1,0,1,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,1,1,0,0,1,0,1,1,1,0,0,0,0,0,1,1,1,1,0,1,1,1,1,1,1,1,0,0,0,0,1,1,0,1,0,1,1,1,0,0,1,1,1,0,0,1,1,0,1,1,0,0,1,1,0,1,1,0,1,1,1,1,0,1,1,0,0],[1,1,0,0,0,1,1,1,0,1,1,1,1,0,0,0,0,1,0,0,1,1,1,0,1,1,1,0,0,0,0,0,0,0,1,1,0,0,0,1,0,1,1,0,1,0,1,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,1,0,1,0,1,1,1,1,0,1,1,0,1,0,0,1,0,0,1,1,0,0,0,1,0,1,0,0,0,0,0,1,1,0],[0,1,1,1,0,0,1,0,0,0,0,0,1,1,0,1,1,1,0,1,1,0,1,0,0,0,0,0,1,1,1,0,1,0,0,1,0,0,1,1,0,0,1,1,1,1,1,0,0,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,0,0,0,0,0,0,0,1,1,1,0,1,1,1,0,0,1,0,1,1,1,0,1,0,1,1,1,0,0,1,1],[1,1,0,1,1,0,0,0,1,1,1,0,0,1,0,1,0,0,0,0,1,0,1,1,1,1,1,0,1,0,0,0,1,1,1,1,0,1,1,0,0,0,0,1,0,1,0,0,1,1,0,0,0,0,1,0,1,1,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,1,1,1,1,0,1,0,1,0,0,0,1,1,1,1,0,0,0,1,1,1,0,1,0,0,0,1],[1,0,0,0,1,1,1,1,1,0,1,0,0,1,0,1,1,0,1,1,1,0,1,0,0,0,1,1,1,0,1,1,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,1,0,0,1,0,0,1,0,0,0,0,0,1,1,1,0,1,0,1,1,1,0,1,1,1,1,0,0,0,0,0,0,1,1,1,0,0,0,0,1,1,0,0,0,0,0,0,1,0,1,0,1],[1,1,1,0,0,0,0,0,0,0,1,1,0,1,0,0,1,0,0,1,0,0,0,0,0,1,1,0,1,0,1,0,0,0,0,1,1,1,0,1,1,1,0,0,1,1,0,1,0,0,1,1,0,1,1,0,1,1,1,0,0,0,1,0,1,1,1,0,1,0,0,0,0,1,0,1,1,1,1,0,0,0,1,0,1,1,0,0,1,1,1,1,0,1,1,1,0,1,1,1],[1,0,1,1,0,0,1,1,1,0,0,1,0,1,1,0,1,1,0,1,0,1,1,1,0,0,1,0,1,0,1,1,1,1,1,1,0,1,0,1,0,1,1,0,0,0,0,1,0,1,1,0,0,1,0,0,1,0,1,1,0,1,1,0,0,0,0,0,1,1,1,1,0,1,0,1,0,1,0,0,1,0,1,0,0,1,1,0,0,0,1,0,0,1,0,0,0,0,0,1],[1,0,0,1,0,1,1,0,1,1,0,1,0,1,0,0,0,1,0,0,0,1,0,1,1,0,1,0,1,0,0,0,0,0,0,0,0,1,0,1,0,0,1,0,1,1,1,1,0,0,1,1,1,1,1,1,1,0,0,1,0,0,1,1,1,0,1,0,0,0,0,1,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,1,0,1,1,1,0,1,1,0,1,0,1,1],[1,1,0,0,0,1,0,0,0,1,0,1,0,1,1,1,0,1,1,1,0,1,0,0,1,0,1,0,1,1,1,1,1,1,1,0,1,1,0,1,1,0,1,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,1,1,1,1,1,1,0,1,1,0,0,1,0,1,0,0,1,0,0,0,0,0,0,1,1,1,0,0,0,0,1,0,1,1,1,0],[0,1,0,0,1,1,0,0,1,1,0,1,0,0,0,0,0,0,0,1,0,1,0,0,1,0,1,0,0,1,0,0,0,0,1,0,1,0,0,0,1,0,0,0,0,0,1,0,1,1,1,0,0,1,1,1,1,1,0,0,1,1,1,0,0,1,0,1,0,0,0,0,1,1,1,1,0,1,0,0,1,1,0,1,0,0,1,1,0,0,0,1,1,1,1,0,1,0,0,0],[0,1,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,1,0,1,1,1,0,1,1,0,1,0,0,1,1,0,0,1,1,0,1,0,0,1,1,1,1,1,0,1,1,0,1,0,1,0,1,1,0,0,0,1,0,0,0,0,1,1,0,0,0,1,1,1,1,0,0,0,0,0,0,1,1,0,0,1,0,1,1,1,1,0,0,1,1,1,0,0,0,0,1,1,0,1],[1,1,0,1,0,0,0,1,0,0,0,0,1,1,1,1,0,1,0,0,0,0,0,1,0,0,1,1,0,0,1,1,0,1,0,0,1,1,0,0,0,0,0,1,0,1,0,0,1,0,1,0,1,0,0,0,1,1,1,1,1,0,0,1,1,1,0,0,0,1,0,0,1,1,1,1,0,0,1,1,0,1,0,1,0,0,0,0,0,1,0,0,0,1,1,0,0,1,0,1],[0,1,0,1,0,1,0,1,1,1,0,0,0,0,1,0,0,1,1,1,1,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,1,1,1,1,0,0,1,0,0,0,0,1,0,0,0,1,1,1,0,1,0,0,0,0,0,0,0,0,1,0,1,1,1,0,1,1,0,1,0,0,1,1,0,0,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,0,1,0,1],[1,1,0,1,0,1,0,0,0,1,1,0,0,1,1,0,0,0,1,0,1,0,1,1,0,1,0,1,1,1,0,1,1,1,1,1,0,0,0,0,1,1,0,1,0,1,1,1,1,0,1,1,1,0,1,0,0,0,1,1,1,1,1,0,0,1,0,1,0,1,1,1,0,0,0,0,1,1,0,0,1,1,0,1,0,0,0,1,1,0,0,1,0,1,0,1,0,1,0,1],[0,0,0,1,0,1,1,1,0,0,1,0,1,1,0,0,1,1,1,0,0,0,1,0,0,1,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,1,0,1,0,1,0,0,0,0,0,0,0,0,1,0,1,1,1,0,0,0,1,0,1,1,0,1,0,1,0,1,0,1,1,1,1,0,0,0,1,0,0,1,1,0,1,1,0,0,1,1,0,1,1,1,0,1,1,1],[1,1,1,1,0,1,0,0,0,0,1,0,0,1,0,0,1,0,0,0,1,1,1,0,1,1,1,1,1,1,1,0,1,1,0,1,0,1,1,1,0,1,1,1,0,1,1,0,0,1,1,1,1,1,1,0,1,0,0,0,1,0,1,1,1,0,0,1,0,1,0,0,0,1,0,0,1,0,0,1,1,0,1,1,0,0,1,0,0,0,1,0,0,0,0,1,0,0,0,1],[1,0,0,1,0,1,1,0,1,1,1,1,0,1,0,1,1,0,1,1,1,0,0,0,0,0,1,0,0,0,1,0,1,0,0,1,1,1,0,1,1,1,0,0,0,1,0,0,1,1,0,1,0,0,1,0,1,1,1,0,1,0,1,0,1,1,1,1,0,1,0,0,1,1,1,0,0,0,1,1,0,0,0,0,0,1,1,0,1,0,1,0,0,1,1,1,1,0,1,1],[1,1,0,0,0,0,1,1,1,0,0,1,0,0,0,1,0,0,1,0,0,0,1,1,1,0,0,0,1,0,1,0,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,1,1,0,0,1,1,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,0,0,0,1,1,0,1,1,0,1,1,0,0,1,1,1,1,1,0,0,1,1,1,1,0,1,0,0,0,0,1,0],[0,1,1,1,1,0,0,0,0,0,0,1,1,1,0,1,1,0,1,1,1,0,1,0,1,1,1,0,1,0,1,0,0,1,1,1,1,1,1,0,0,1,0,1,0,0,0,0,1,0,0,0,1,1,0,1,0,0,1,0,0,0,1,1,1,0,0,0,0,1,1,1,0,0,0,0,0,1,0,0,1,1,0,1,0,1,0,0,1,0,0,1,0,1,1,1,0,0,1,0],[0,0,1,0,0,0,1,1,1,1,0,0,0,1,0,0,1,0,0,0,1,1,1,0,0,0,1,0,1,1,1,1,0,0,0,1,0,1,0,0,1,1,0,1,1,0,1,1,1,0,1,0,0,1,1,1,1,0,1,1,0,0,1,0,1,1,1,0,0,0,1,0,0,0,1,1,1,1,0,1,1,0,0,1,0,0,0,1,1,1,0,0,0,0,0,1,1,0,1,1],[1,1,1,0,1,1,1,0,0,1,0,0,1,1,1,0,1,1,1,0,0,0,0,0,1,0,1,0,0,0,1,0,0,1,1,1,0,0,0,1,1,0,0,0,1,0,1,0,0,0,1,1,0,0,0,0,1,0,0,1,0,1,1,0,0,0,1,1,1,1,1,0,1,1,1,0,1,0,0,1,0,0,1,1,1,1,0,0,0,0,0,1,1,1,0,0,1,0,1,0],[1,0,1,0,1,0,0,0,0,1,1,0,0,0,1,0,0,1,0,0,0,1,1,1,1,0,1,1,0,1,1,0,1,1,0,1,0,0,1,1,0,0,0,1,1,0,1,1,0,1,1,0,0,0,1,0,1,1,0,1,0,1,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,1,1,0,0,0,0,0,1,1,0,0,1,1,1,0,1,1,0,1,1,1,1],[1,0,0,0,1,0,1,1,0,0,1,0,1,1,1,1,0,1,1,1,1,1,0,0,1,0,0,1,0,1,0,0,1,0,0,1,0,1,1,0,0,0,1,1,0,0,0,1,0,0,1,0,0,1,1,0,0,1,0,1,0,1,1,0,1,1,1,1,1,0,0,1,1,0,1,1,0,1,1,0,0,1,1,1,0,0,1,1,1,1,0,1,0,0,1,0,0,0,0,1],[1,1,0,0,1,0,1,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,1,0,1,1,0,1,1,0,1,0,1,1,1,1,0,0,0,1,1,0,0,1,0,1,1,0,1,1,0,1,0,0,0,1,0,1,0,0,1,0,1,0,0,0,0,0,1,1,0,0,1,0,0,1,0,0,1,1,0,1,0,1,1,0,0,0,0,0,0,1,1,1,0,1,0,1],[0,1,1,1,1,1,1,0,1,0,1,0,0,1,0,1,1,1,1,1,0,1,1,1,0,0,1,0,0,0,1,1,1,0,0,0,0,0,0,1,1,1,0,0,0,1,0,0,1,0,0,1,1,1,1,1,0,1,1,1,0,0,1,0,1,0,1,1,1,0,1,0,0,0,1,1,1,1,0,1,1,0,0,1,0,1,0,0,1,1,1,0,0,0,0,1,0,1,0,1],[1,1,0,1,0,0,1,1,1,0,1,1,0,1,0,0,0,0,0,1,0,1,0,1,0,1,1,0,1,0,0,0,1,1,0,1,1,1,0,0,1,0,0,1,1,1,0,0,1,1,0,0,1,0,1,0,0,0,0,0,0,1,1,0,0,0,1,0,1,1,1,0,0,1,1,0,0,0,0,1,0,0,0,1,0,0,0,1,1,0,1,0,1,1,1,1,0,1,1,1],[1,0,0,0,0,0,0,0,1,0,0,1,0,1,1,1,1,1,0,1,0,1,0,0,0,1,0,0,1,0,0,1,1,0,0,1,0,1,1,1,1,0,0,1,0,1,1,0,0,1,1,1,1,0,1,1,0,1,1,1,0,1,0,0,1,1,1,0,0,0,0,0,1,1,0,0,1,1,1,1,0,1,1,1,1,0,1,1,0,0,1,0,0,0,1,0,0,1,0,0],[1,0,1,0,1,1,1,0,1,0,0,1,0,0,1,0,0,1,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0,0,1,1,0,0,0,0,0,0,1,1,0,0,1,1,0,1,0,0,0,0,0,1,1,1,0,0,0,1,0,0,1,0,0,0,1,1,1,0,1,0,0,0,1,0,0,0,0,0,1,0,1,1,1,0,0,1,1,1,1,1,1,0,1,1,1,1],[0,0,1,1,1,0,1,0,1,1,0,1,1,0,0,0,1,1,0,0,0,0,1,0,1,0,0,0,1,1,1,0,0,1,1,0,0,1,1,1,0,1,1,0,0,1,1,0,0,1,0,1,1,1,0,0,0,0,0,1,1,1,0,1,1,0,1,0,1,0,1,0,0,0,1,1,1,0,1,1,1,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],[1,1,1,0,1,0,1,0,0,1,0,0,1,1,1,0,1,0,0,1,1,1,1,0,1,1,1,0,1,0,1,0,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,0,1,1,0,1,0,1,1,0,1,1,1,1,0,1,0,1,0,0,1,1,1,0,1,1,0,0,0,1,0,0,1,0,1,0,0,0,1,1,1,1,0,0,0,1,1,1,1,1,1,1,0,1],[0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,1,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,1,1,0,0,1,0,0,0,0,0,0,0,1,1,0,0,1,0,0,1,1,1,0,0,0,0,0,0,1,0,1,1,0,1,0,0,1,1,1,0,1,1,1,1,0,1,1,0,0,1,0,0,1,1,1,0,0,0,0,1,0,0,0,0,1],[1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,0,1,1,1,1,0,1,1,1,0,0,1,1,0,1,1,0,0,0,0,0,1,1,1,1,0,1,1,0,0,1,1,0,0,0,0,1,0,1,1,1,0,1,1,0,1,0,0,1,1,0,0,0,1,0,0,0,0,1,0,0,1,1,0,1,0,0,0,0,1,1,1,0,0,1,1,1,1,1,1],[1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1,1,0,0,1,0,0,1,0,0,1,1,0,0,1,0,0,1,0,0,1,1,0,1,0,0,1,0,0,0,0,1,1,1,1,0,0,0,1,0,1,1,1,0,0,1,1,0,0,1,1,1,0,1,1,1,1,0,0,0,0,0,1,1,1,0,1,1,0,0,0,1,1,0,1,0,0,0,0,0],[1,0,0,1,1,1,0,0,1,1,1,0,1,1,1,1,0,1,0,1,0,1,1,0,1,1,0,1,1,0,1,0,0,0,1,1,1,1,1,1,1,0,0,1,0,1,1,0,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,1,1,0,0,0,1,0,0,0,0,1,1,0,0,1,0,0,1,0,0,0,1,1,0,0,0,1,0,1,1,1,1,0,1],[1,1,0,0,0,1,0,1,1,0,1,1,1,0,0,1,0,1,0,0,0,0,0,0,1,0,0,0,1,0,1,1,0,1,1,0,1,0,1,0,0,0,1,1,0,1,0,0,1,1,1,1,0,0,0,0,0,0,0,0,1,1,0,1,1,0,0,1,0,1,1,1,0,1,0,0,0,1,1,1,1,1,0,1,1,1,1,1,0,0,1,0,1,0,0,0,0,1,0,1],[0,1,1,1,0,1,1,1,0,0,0,0,0,0,1,1,0,1,1,1,1,1,1,1,1,0,0,0,1,0,0,1,0,1,0,0,1,0,0,0,1,1,1,0,0,1,0,0,1,0,0,1,1,0,0,1,1,1,1,0,0,1,1,1,0,0,0,0,0,1,0,0,0,1,1,1,0,0,0,0,0,1,0,0,0,0,0,1,1,0,1,0,1,1,0,1,0,1,1,1],[0,0,0,1,0,0,0,0,0,1,1,0,1,1,1,0,0,0,0,0,0,0,1,0,1,1,0,1,1,0,1,1,0,1,0,0,1,1,0,1,1,0,1,0,1,1,0,1,1,1,0,0,1,1,1,1,0,0,1,1,1,1,0,1,0,0,1,1,1,1,0,1,0,1,0,1,1,1,1,1,0,1,1,0,1,1,0,0,1,0,1,0,0,1,0,1,0,0,0,1],[1,1,0,1,1,0,1,1,0,0,1,0,1,0,0,0,1,0,0,1,1,1,1,0,0,1,0,1,0,0,1,0,0,1,1,0,0,1,0,1,0,0,1,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,1,0,1,0,0,1,1,1,0,1,0,0,0,1,0,0,1,0,0,1,1,1,1,0,1,0,0,1,0,1,1,0,1,1],[0,1,0,0,1,0,0,1,0,1,1,0,1,1,0,0,1,1,1,1,0,0,0,0,0,1,0,1,1,1,1,1,0,0,1,1,0,0,0,1,0,0,0,0,1,1,1,0,1,1,0,1,0,1,1,1,1,0,0,1,0,1,0,0,0,1,0,0,1,1,0,0,0,1,0,1,1,0,0,0,0,1,1,0,1,1,0,0,0,0,1,0,1,1,0,1,0,0,1,0],[1,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,1,0,0,0,0,1,1,1,0,1,0,1,0,0,0,0,0,0,0,1,1,0,0,1,1,1,0,0,0,0,1,0,0,1,1,1,0,0,0,0,1,1,1,1,0,1,1,0,1,1,1,0,1,0,0,0,1,1,0,0,1,1,0,1,1,1,0,0,1,0,0,0,1,0,1,0,1,0,0,1,0,1,1,1],[1,0,1,0,0,0,0,1,0,1,1,1,0,1,0,1,0,0,0,1,1,1,0,1,0,0,0,0,0,1,1,1,0,1,0,0,1,1,0,0,0,1,1,0,0,1,1,0,0,0,0,1,1,1,1,0,0,0,1,0,0,0,1,1,1,0,1,0,1,1,1,0,0,1,1,0,0,1,0,1,0,0,0,0,1,1,1,1,1,1,1,0,1,0,1,1,0,1,0,0],[1,0,0,0,1,0,1,1,1,1,0,0,0,1,0,1,1,1,0,1,0,0,0,1,1,1,0,0,1,1,0,1,0,1,1,0,1,0,0,1,0,0,1,1,0,0,1,0,1,1,0,0,0,0,1,1,1,0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,1,1,0,1,1,1,1,0,0,0,1,0,0,0,0,0,1,0,0,1,1,1,1,1],[1,1,1,1,1,1,1,0,0,0,0,0,1,1,0,1,0,0,0,1,1,1,0,0,0,1,1,1,1,0,0,1,0,0,1,1,1,1,0,1,1,0,0,1,0,1,1,0,0,1,1,1,0,0,0,0,1,0,0,0,1,1,1,1,1,0,0,1,1,0,0,1,1,1,1,0,1,0,0,0,0,0,1,1,0,0,0,0,1,1,1,0,1,1,0,0,0,0,0,0],[1,0,0,1,0,1,0,0,0,1,1,1,1,0,0,1,0,1,1,1,0,1,1,0,0,0,1,0,0,0,0,1,0,0,1,0,0,1,1,1,0,0,0,1,0,1,0,0,1,1,0,1,1,0,0,1,1,1,1,1,1,0,0,0,1,1,1,1,0,0,1,1,0,0,1,0,1,0,1,0,1,0,0,1,1,1,0,0,1,0,1,0,0,1,1,1,0,1,1,1],[1,1,0,0,0,0,0,0,1,1,0,0,1,1,0,0,0,1,0,0,0,0,1,1,1,0,1,1,1,1,0,1,1,0,0,0,0,0,0,0,0,1,1,1,0,1,0,0,0,1,0,0,1,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1,1,0,1,1,1,1,1,1,0,0,0,1,1,1,1,0,1,0,1,1,0,1,1,1,0,1],[0,1,1,0,0,1,1,1,1,0,0,1,1,0,0,0,1,1,1,0,1,0,0,0,0,0,0,0,0,1,0,0,1,1,0,0,1,1,1,1,1,1,0,1,0,1,1,1,0,1,1,0,0,1,1,0,0,1,0,1,0,0,1,1,0,0,1,1,1,1,1,1,0,1,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1],[0,0,0,0,1,1,0,0,0,0,1,1,0,0,1,1,1,0,0,0,1,1,1,1,1,1,0,0,1,1,1,0,0,1,1,1,1,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,1,1,0,1,1,1,1,1,1,0,0,1,1,0,0,1,0,1,1,1,0,1,0,0,1,1,1,1,0,1,1,0,1,0,1,1,1,0,0,0,1,0,1,1,1,1],[1,1,1,1,1,0,0,1,1,1,1,0,0,1,1,0,0,0,0,1,1,0,0,1,0,1,1,0,1,0,0,0,0,0,1,0,1,0,1,1,1,1,1,1,0,1,1,1,0,0,1,1,1,0,0,1,1,1,0,0,0,0,0,0,0,0,1,1,0,1,0,0,0,0,0,1,1,0,1,0,0,1,0,1,0,0,1,1,1,0,0,0,1,1,1,1,1,0,0,1],[1,0,1,0,0,0,1,1,0,0,0,0,0,1,0,0,1,0,1,1,0,0,0,1,0,0,1,1,1,0,1,0,1,1,1,0,0,0,0,0,0,1,0,0,0,1,0,0,0,1,1,0,1,0,1,1,0,0,0,1,1,0,1,1,1,0,0,1,0,0,0,0,1,1,0,0,1,1,1,1,0,0,0,1,0,1,1,0,0,0,1,1,1,0,0,0,0,0,0,1],[1,0,1,1,1,0,0,0,0,1,1,1,0,1,0,0,1,0,1,0,0,0,1,1,1,0,0,1,0,0,1,1,1,0,0,0,0,1,1,1,0,0,0,1,1,1,1,0,0,1,0,0,1,0,0,1,0,0,1,1,0,0,1,0,1,1,0,1,1,1,0,1,1,0,0,0,1,0,0,1,1,1,0,0,0,1,0,0,1,1,1,0,0,0,1,1,1,0,1,1],[1,0,0,1,0,0,1,1,1,1,0,1,0,1,1,0,1,0,1,1,0,1,1,0,0,0,0,0,0,1,1,0,1,1,0,1,1,1,0,1,0,0,1,1,0,0,0,0,1,1,0,1,1,0,1,1,1,0,1,0,0,1,1,0,0,1,0,0,0,1,0,1,0,0,1,1,1,1,0,0,0,1,0,0,1,1,0,0,0,0,1,0,1,0,0,1,0,0,1,0],[1,0,0,1,0,1,1,0,0,0,0,1,0,0,1,0,1,0,0,1,0,1,0,0,0,1,1,1,0,1,0,0,0,0,0,1,0,0,0,1,1,0,1,0,0,0,1,1,1,0,0,1,0,0,0,0,1,1,1,1,0,0,1,0,1,1,1,0,1,1,0,1,0,1,1,0,0,1,1,1,0,1,1,1,1,0,0,1,0,1,1,0,1,0,0,1,1,0,1,1],[1,1,0,1,1,1,0,0,1,1,0,1,1,1,1,0,1,1,0,1,0,0,0,1,1,1,0,1,0,1,0,0,1,1,1,1,0,1,0,0,1,0,1,0,0,1,1,0,0,0,0,1,0,1,1,0,0,0,0,1,1,0,1,0,1,0,1,0,1,0,0,1,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1,1,0,0,1,1,1,1,0,0,0,1],[1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,0,0,1,1,0,1,1,0,0,0,1,0,0,0,1,1,0,0,0,0,1,1,0,1,0,1,0,1,1,0,0,1,1,1,1,0,0,1,1,1,0,0,0,1,0,1,0,0,0,1,0,1,1,0,0,0,0,0,1,0,1,1,1,1,0,1,1,1,1,1,1,0,0,0,0,0,0,1,0,0,1,1,1],[1,1,1,0,0,1,1,1,0,0,0,1,0,1,1,0,1,1,0,1,0,0,1,0,0,1,0,1,1,1,0,1,0,0,1,0,1,1,0,0,1,0,1,0,1,0,0,1,1,0,0,0,0,1,1,0,1,1,0,0,1,0,1,1,0,0,1,0,0,1,1,1,1,1,0,1,1,1,0,0,1,0,0,0,0,0,0,0,0,1,1,1,1,0,1,0,1,1,0,1],[0,0,1,1,0,1,0,1,1,1,1,1,0,0,1,1,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,1,1,1,1,0,0,1,1,0,1,1,1,0,1,1,0,0,1,0,1,1,0,0,0,1,1,1,1,0,0,1,1,0,1,1,0,0,0,0,0,1,1,1,0,0,0,1,1,0,1,1,1,0,0,1,1,1,0,0,1,1,1,0,1,0,0,0],[1,0,0,1,0,0,0,0,1,0,0,1,1,0,1,0,1,1,0,1,1,0,1,1,1,1,0,0,1,1,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,1,0,0,1,1,1,1,0,0,1,1,1,0,0,0,0,0,0,1,0,0,1,0,1,1,1,0,1,0,0,0,1,1,1,0,0,1,0,1,1,1,1,0,1,0,0,0,0,0,0,1,1,1,0],[1,1,0,1,1,0,1,0,1,0,0,0,1,0,1,0,0,1,0,0,1,0,0,0,0,1,1,0,0,1,0,1,1,1,0,1,1,1,0,1,1,1,1,1,1,0,1,1,0,0,1,0,0,0,0,0,1,0,0,1,1,1,1,0,1,1,0,1,0,1,0,1,0,1,0,0,1,1,0,0,0,1,1,0,1,0,0,1,0,1,0,1,1,1,1,0,0,0,1,1],[1,0,0,0,1,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,0,0,1,0,0,0,1,0,0,1,0,0,0,1,0,0,1,1,0,0,0,1,1,1,0,1,0,1,1,0,0,1,0,0,1,0,1,0,1,0,1,0,0,0,1,1,0,0,1,0,1,0,0,1,1,0,0,0,0,0,1,0,0,1,1,0,0,0,1],[1,1,1,0,0,0,1,0,0,1,0,1,0,0,0,1,0,1,0,0,0,0,0,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,0,1,1,1,0,0,0,0,0,1,0,0,1,1,0,1,0,0,0,1,0,0,1,1,1,0,1,0,1,0,1,0,1,1,0,1,1,0,0,1,1,1,1,0,0,0,0,0,1,1,1,0,1,0,0,0,1,1,0,1,1],[1,0,1,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,0,1,0,1,0,1,1,1,0,1,1,1,0,0,1,0,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,0,1,1,0,1,1,1,0,1,1,1,0,0,1,1,1,0,0,1,1,0,0,1,1,1,1,1,1,1,0,1,1,1,1,1,0,0,1,1,1,0]]
    cProfile.run('islandPerimeter(grid)')