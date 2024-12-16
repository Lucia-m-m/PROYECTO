'''
Created on 17 nov 2024

@author: belen
'''

from __future__ import annotations
from typing import TypeVar
from entrega3.Recorrido import Recorrido
from entrega3.Grafo import Grafo
from entrega2.tipos.Pila import Pila

V = TypeVar('V')
E = TypeVar('E')


class Recorrido_en_profundidad(Recorrido[V,E]):
    
    @staticmethod
    def of(grafo:Grafo[V,E])->Recorrido_en_profundidad[V,E]:
        return Recorrido_en_profundidad(grafo)
    
    def __init__(self,grafo:Grafo[V,E])->None:
        super().__init__(grafo)
    
    
    def traverse(self,source:V)->None:
        stack = Pila[V]()  
        visited = set()  
        stack.push(source)
        self._tree[source] = (None, 0.0)
        
        while not stack.is_empty():
            v = stack.pop()  
            if v not in visited:
                visited.add(v)
                self._path.append(v)
                self._tree[v] = (self.origin(v), 0)
                
                for neighbor in self._grafo.adjacent_vertices(v):
                    if neighbor not in visited:
                        stack.push(neighbor)   

if __name__ == '__main__':
    pass