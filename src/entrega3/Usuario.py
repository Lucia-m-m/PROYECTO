'''
Created on 17 nov 2024

@author: belen
'''

from __future__ import annotations
from dataclasses import dataclass
from datetime import date, datetime





@dataclass(frozen=True)
class Usuario:
    dni: str
    nombre: str 
    apellidos:str 
    fecha_nacimiento: date
    
    @staticmethod
    def of(dni:str, nombre:str, apellidos:str, fecha_nacimiento:date) -> Usuario:
        return Usuario(dni, nombre, apellidos, fecha_nacimiento)
    
    @staticmethod
    def parse(linea:str) -> Usuario:
        campos = linea.split(",")
        dni = campos[0]
        nombre = campos[1]
        apellidos = campos[2]
        fecha_nacimiento = datetime.strptime(campos[3], '%Y-%m-%d').date()
        return Usuario.of(dni, nombre, apellidos, fecha_nacimiento)
        
       
    
            
    def __str__(self):
        return f"Usuario: {self.nombre}  {self.apellidos}, DNI: {self.dni}"

if __name__ == '__main__':
    linea:str = "45718832U,Carlos,Lopez,1984-01-14"
    usuario: Usuario = Usuario.parse(linea)
    print(usuario)