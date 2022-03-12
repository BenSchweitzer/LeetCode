from typing import Dict, List, Tuple



class Node:
    def __init__(self,color,i,j) -> None:          
        self.i = i
        self.j = j            
        self.color = color

    def getPos(self) -> Tuple[int,int]:
        return (self.i,self.j)

    def getColor(self) -> int:
        return self.color

    def updateColor(self,color) -> None:
        self.color = color



class imageGraph:

    def __init__(self,image) -> None:        
        self.nodes:List[Node] = []
        self.edges:Dict[Node,List[Node]] = {}
        self.posIndex:Dict[Tuple[int,int],Node] = {}
        
        # The graph is m rows by n columns
        self.m = len(image)
        self.n = len(image[0])
        
        self.buildGraph(image)

    def getNode(self,i:int,j:int) -> Node:
        p = (i,j)
        if p in self.posIndex.keys():
            return self.posIndex[p]
        else:
            raise ValueError(f"No node at pos i:{i} j:{j}")

    def getAttachedNodes(self,n:Node) -> list[Node]:
        return self.edges[n]

    def addNode(self,n:Node): 
        if n not in self.nodes: 
            self.nodes.append(n)
            self.posIndex[n.getPos()] = n
            self.edges[n] = []

    def addEdge(self,n1:Node,n2:Node):
        self.addNode(n1)
        self.addNode(n2)

        self.edges[n1].append(n2)
        self.edges[n2].append(n1)
    

    def buildGraph(self,image):  

        #For i rows
        for i in range(self.m):

            #For j columns
            for j in range(self.n):

                color = image[i][j]
                n = Node(color,i,j)

                #The first node of the row does not have a node to its left, so we just need to create the node
                if j == 0: self.addNode(n)

                # Every node after the first will form an edge with the node to its left
                else: 
                    n1 = self.getNode(i,j-1)
                    n2 = n
                    self.addEdge(n1,n2)
                
                # If this is not the first row then we should create edges to the node above the new node we created
                if i > 0:
                    n1 = self.getNode(i-1,j)
                    n2 = n
                    self.addEdge(n1,n2)
    
    def printGraph(self):
        hl = '-'
        vl = '|'

        pos = [[' ' for c in range(self.n*2-1)] for r in range(self.m*2-1)]

        for n in self.nodes:
            i,j = n.getPos()
            i *= 2
            j *= 2
            pos[i].insert(j,n.getColor())

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
    

    def buildImage(self) -> List[List[int]]:

        image:List[List[int]] = [[0 for c in range(self.n)] for r in range(self.m)]

        for n in self.nodes:
            i,j = n.getPos()
            image[i][j] = n.getColor()
        
        return image



def floodFill(image: List[List[int]], sr: int, sc: int, newColor: int) -> List[List[int]]:
    g = imageGraph(image)

    oc = image[sr][sc]

    searchNodes:List[Node] = [g.getNode(sr,sc)]
    visitedNodes:List[Node] = []

    while len(searchNodes) > 0:

        #Grab the first node from the list
        n = searchNodes[0]

        searchNodes.remove(n)
        visitedNodes.append(n)

        n.updateColor(newColor)

        for n in g.getAttachedNodes(n):
            if n in visitedNodes: 
                continue
            if n.color == oc: 
                searchNodes.append(n)

    return g.buildImage()

import unittest

#Testcases
class TestFloodFill(unittest.TestCase):
    
    def test1(self):
        image = [[1,1,1],[1,1,0],[1,0,1]]
        sr = 1
        sc = 0
        newColor = 2

        newImage = [[2,2,2],[2,2,0],[2,0,1]]
        self.assertEqual(floodFill(image,sr,sc,newColor),newImage)

    def test2(self):
        image = [[0,0,0],[0,0,0]]
        sr = 0
        sc = 0
        newColor = 2

        newImage = [[2,2,2],[2,2,2]]
        self.assertEqual(floodFill(image,sr,sc,newColor),newImage)

if __name__ == '__main__':
    unittest.main()
