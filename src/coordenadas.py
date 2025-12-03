from typing import NamedTuple, List
from math import sqrt

Coordenadas = NamedTuple('Coordenadas', [('latitud',float), ('longitud', float)])

def calcular_distancia(coord1: Coordenadas, coord2: Coordenadas)->float:
    '''
    recibe dos tuplas de tipo ```Coordenadas``` y produce como salida 
    un float correspondiente a la distancia euclídea entre ambas coordenadas.
    '''
    distancia = sqrt( (coord1.latitud - coord2.latitud) ** 2 + (coord1.longitud - coord2.longitud) ** 2 )

    return distancia

def calcular_media_coordenadas(coordenadas:List[Coordenadas]):
    
    sum_x = 0.0
    sum_y = 0.0

    for coordenada in coordenadas:
        sum_x += coordenada.latitud
        sum_y += coordenada.longitud
        
    return Coordenadas(sum_x/len(coordenadas), sum_y/len(coordenadas))
    
