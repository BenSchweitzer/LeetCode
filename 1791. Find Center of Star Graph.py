from typing import List, Set

class Solution:
    def findCenter(self, edges: List[List[int]]) -> int:
        edge:Set[int] = set()
        
        for e in edges:
            for n in e:
                if n in edge:
                    return n
                else:
                    edge.add(n)
        