'''
Created on 17 nov 2024

@author: belen
'''
from __future__ import annotations
from typing import TypeVar, Callable
from enum import Enum
from entrega3.Grafo import Grafo
import networkx as nx
import matplotlib.pyplot as plt

V = TypeVar('V')
E = TypeVar('E')

class Graph_type(Enum):
    UNDIRECTED = 1
    DIRECTED = 2
    

#===============================================================================
# Traverse_type -> Tipo de recorrido del grafo
#===============================================================================
class Traverse_type(Enum):
    FORWARD = 1
    BACK = 2

class E_grafo(Grafo[V,E]):
    
    def __init__(self,graph_type:Graph_type,weight:Callable[[E],float],traverse_type:Traverse_type=Traverse_type.FORWARD)->None:
        self._vertex_set:set[V] = set() # Conjunto de vértices del grafo (nodos)
        self._edge_set:set[E] = set() # Conjunto de aristas (relaciones entre nodos)
        self._edges_dict:dict[tuple[V,V],E] = {}  # Diccionario que mapea las parejas de vértices a las aristas
        self._neighbors:dict[V,set[V]] = {} # Diccionario que guarda los vecinos de cada vértice
        self._predecessors:dict[V,set[V]] = {} # Diccionario que guarda los predecesores (vértices anteriores) de cada vértice
        self._sources:dict[E,V] = {} # Diccionario que mapea las aristas a sus vértices de origen
        self._targets:dict[E,V] = {} # Diccionario que mapea las aristas a sus vértices de origen
        self._graph_type = graph_type # Tipo de grafo (dirigido o no dirigido)
        self._weight = weight  # Función que calcula el peso de una arista
        self._traverse_type = traverse_type # Tipo de recorrido: hacia adelante (FORWARD) o hacia atrás (BACK)
     
    def __add_neighbors(self, source:V, target:V)->None:
        if source not in self._neighbors:
            self._neighbors[source] = set()
        self._neighbors[source].add(target)
            
    def __add_predecessors(self, source:V, target:V)->None:
        if self._graph_type == Graph_type.DIRECTED:
            if target not in self._predecessors:
                self._predecessors[target] = set()
        self._predecessors[target].add(source)

    def add_edge(self,source:V,target:V,e:E)->None:
        if source == target:
            raise ValueError("Los vértices no pueden ser iguales")
    
        if source not in self._vertex_set or target not in self._vertex_set:
            raise ValueError("Los vértices no pertenecen al grafo") 
        if(source, target) in self._edges_dict:
                raise ValueError("La arista ya existe")
        if self._graph_type == Graph_type.UNDIRECTED:   
            self._edges_dict[(source, target)] = e
            self._edges_dict[(target, source)] = e
            self._sources[e] = source
            self._targets[e] = target
            
            self.__add_neighbors(source, target)
            self.__add_neighbors(target, source)
        else:
            self._edges_dict[(source, target)] = e
            self._sources[e] = source
            self._targets[e] = target
            self.__add_neighbors(source, target)
            self.__add_predecessors(source, target)
            
        self._edge_set.add(e)    
        
        
        
            
                
    def edge_weight(self,sourceVertex:V, targetVertex:V) -> float:
        edge = self._edges_dict.get((sourceVertex, targetVertex))
        if edge is None:
            raise ValueError("No existe una arista entre los vértices dados")
        return self._weight(edge)
    
    def add_vertex(self,vertex:V)->bool:
        if vertex in self._vertex_set:
            return False 
        self._vertex_set.add(vertex)
        self._neighbors[vertex] = set()
        
        self._predecessors[vertex] = set()
        return True
            
    def edge_source(self,e:E)->V:
        if e not in self._edge_set:
            raise ValueError("La arista no existe en el grafo")
        return self._sources[e]
    
    def edge_target(self,e:E)->V:
        if e not in self._edge_set:       
            raise ValueError("La arista no existe en el grafo")
        return self._targets[e]
    
    def vertex_set(self)->set[V]:
        return self._vertex_set
     
    def edge_set(self)->set[E]:
        return self._edge_set
    
    def contains_edge(self,sourceVertex:V, targetVertex:V)->bool:
        if (sourceVertex, targetVertex) not in self._edges_dict:
            return False
        return True
     
    def neighbors(self,vertex:V)->set[V]:
        return self._neighbors.get(vertex,set())
    
    def predecessors(self,vertex:V)->set[V]:
        if vertex not in self._vertex_set:
            raise ValueError("El vértice no pertenece al grafo")
        if self._graph_type == Graph_type.DIRECTED:
            return self._predecessors[vertex]
        return self._neighbors
        
    def successors(self,vertex:V)->set[V]:
        if vertex not in self._vertex_set:
            raise ValueError("El vértice no pertenece al grafo")
        
        if self._traverse_type == Traverse_type.FORWARD:
            return self._neighbors[vertex]
        elif self._traverse_type == Traverse_type.BACK:
            return self._predecessors[vertex]
        else:
            raise ValueError("Tipo de recorrido no válido")
    
    def edge(self,sourceVertex:V, targetVertex:V) -> E:
        return self._edge_dict[(sourceVertex,targetVertex)]
            
    def vertex_list(self)->list[V]:
        return list(self._vertex_set)
    
    def graph_type(self)->Graph_type:
        return self._graph_type
    
    def traverse_type(self)->Traverse_type:
        return self._traverse_type
    
    def weight(self)->Callable[[E],float]:
        return self._weight
    
    def inverse_graph(self)->E_grafo[V,E]:
        if self._graph_type == Graph_type.UNDIRECTED:
            return self
        
        inverted_graph = E_grafo(self.graph_type(), self._weight, self._traverse_type)
        
        for vertex in self._vertex_set:
            inverted_graph.add_vertex(vertex)
            
        for e in self._edge_set:
            source= self._edge_source(e)
            target= self._edge_target(e)
            inverted_graph.add_edge(target, source, e)
            
        
        return inverted_graph
    
    def subgraph(self,vertices:set[V]) -> Grafo[V,E]:
        #g= E_grafo[V,E]
        g: E_grafo[V,E]= E_grafo(self.graph_type(),self.weight(),self.traverse_type())
        for v in vertices:
            g.add_vertex(v)
        for e in self.edge_set():
            s = self.edge_source(e)
            t = self.edge_target(e)
            if s in vertices and t in vertices:
                g.add_edge(s,t,e)
        return g
    
    def plot_graph(self):
        # Create an empty networkx graph
        G = nx.DiGraph() if self._graph_type == Graph_type.DIRECTED else nx.Graph()
    
        # Add vertices to the graph
        for vertex in self._vertex_set:
            G.add_node(vertex)
    
        # Add edges to the graph
        edge_labels: dict = {}
        for edge in self._edge_set:
            source = self.edge_source(edge)
            target = self.edge_target(edge)
            G.add_edge(source, target)
            edge_labels[(source, target)] = self._weight(edge)
    
        # Plot the graph using matplotlib
        plt.figure(figsize=(8, 8))  # You can adjust the size
        pos = nx.spring_layout(G)  # Layout for node positioning
        nx.draw(G, pos, with_labels=True, node_size=3000, node_color="lightblue", font_size=12, font_weight="bold", edge_color="gray")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, font_color="red")
        # Show the plot
        plt.title("Graph Visualization")
        plt.show()
            
    def __str__(self):
        sep = '\n'
        return f'Vertices: \n{sep.join(str(x) for x in self._vertex_set)} \nAristas: \n{sep.join(str(x) for x in self._edge_set)}'
    
    

if __name__ == '__main__':
    pass
