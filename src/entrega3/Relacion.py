'''
Created on 17 nov 2024

@author: belen
'''
from __future__ import annotations
from dataclasses import dataclass



@dataclass(frozen=True)
class Relacion:
    id: int
    interacciones: int
    dias_activa: int
    __xx_num:int = 0
    
    @staticmethod
    def of(interacciones: int, dias_activa: int)->Relacion:
        Relacion.__xx_num+=1 # De esta manera creamos identificadores únicos
        return Relacion(interacciones, dias_activa,Relacion.__xx_num)
    
    
    def __str__(self):
        return f"ID: {self.id} - Días activa: {self.dias_activa} - Interacciones: {self.interacciones}"

if __name__ == '__main__':
    relacion1 = Relacion.of(15, 30)
    relacion2 = Relacion.of(10, 20)
    
    # Imprimimos las representaciones de las relaciones
    print(relacion1)
    print(relacion2)