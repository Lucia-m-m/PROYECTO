'''
Created on 17 nov 2024

@author: belen
'''

from __future__ import annotations
from entrega3.E_grafo import E_grafo, Graph_type, Traverse_type
from entrega3.Usuario import Usuario
from entrega3.Relacion import Relacion
from us.lsi.tools.File import lineas_de_fichero, absolute_path



class Red_social(E_grafo[Usuario, Relacion]):
    
    def __init__(self,graph_type:Graph_type,traverse_type:Traverse_type)->None:
        super().__init__(graph_type, lambda r: r.interacciones, traverse_type)
        self.__usuarios_dni:dict[str,Usuario] = {}
        
    
    @staticmethod
    def of(usuarios:list[Usuario], relaciones: list[Relacion], graph_type: Graph_type = Graph_type.UNDIRECTED, traverse_type: Traverse_type= Traverse_type.BACK) -> Red_social: # TODO: Hay que añadir los parámetros de entrada
        #rrss = Red_social(graph_type, traverse_type)
        #return rrss
        rrss = Red_social(graph_type, traverse_type)
        for usuario in usuarios:
            rrss.add_vertex(usuario)
            rrss.__usuarios_dni.update({usuario.dni: usuario})
        for relacion in relaciones:
            rrss.add_edge(relacion.u1, relacion.u2, relacion)
        return rrss
    
    @staticmethod
    def parse(f1:str, f2:str, graph_type:Graph_type = Graph_type.UNDIRECTED, traverse_type: Traverse_type = Traverse_type.BACK) -> Red_social:
        red_social:Red_social = Red_social(graph_type, traverse_type)
        
        usuarios= []
        for linea in lineas_de_fichero(f1):
            u:Usuario = Usuario.parse(linea)
            red_social.add_vertex(u)
            usuarios.append(u)
            red_social.__usuarios_dni.update({u.dni:u})
            
        
     
        relaciones=[]
        for linea in lineas_de_fichero(f2):
            trozos = linea.split(',')
            #u1:Usuario = red_social.__usuarios_dni.get(trozos[0])
            #u2:Usuario = red_social.__usuarios_dni.get(trozos[1])
            u1:Usuario = red_social.__usuarios_dni.get(trozos[0])
            u2:Usuario = red_social.__usuarios_dni.get(trozos[1])
            r:Relacion = Relacion.of(int(trozos[2]),int(trozos[3]))
            red_social.add_edge(u1, u2, r)
            relaciones.append(r)
            
    
                
        return red_social
    
    @property
    def usuarios_dni(self)->dict[str,Usuario]:
        return self.__usuarios_dni

    


if __name__ == '__main__':
    #rrss = Red_social.parse(('C:\\Users\\lucia\\git\\proyecto-laboratorio-python-entrega3-Lucia-m-m\\src\\entrega3\\resources\\usuarios.py'),('C:\\Users\\lucia\\git\\proyecto-laboratorio-python-entrega3-Lucia-m-m\\src\\entrega3\\resources\\relaciones.txt'))
    #rrss = Red_social.parse(('resources/usuarios.txt'), ('resources/relaciones.txt'))
    rrss = Red_social.parse(('../resources/usuarios.txt'), ('../resources/relaciones.txt'))
    # Imprime una representación textual del grafo para verificar datos
    print(rrss.plot_graph())
    
    # Visualiza el grafo
    