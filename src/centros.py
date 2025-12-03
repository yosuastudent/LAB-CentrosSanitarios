from typing import NamedTuple, List

import csv
from coordenadas import Coordenadas, calcular_distancia, calcular_media_coordenadas
from mapas import crea_mapa, agrega_marcador, guarda_mapa

CentroSanitario = NamedTuple('CentroSanitario',
                             [('nombre',str),
                              ('localidad',str), 
                              ('ubicacion',Coordenadas),
                              ('estado',str),
                              ('num_camas', int), 
                              ('acceso_discapacitados', bool), 
                              ('tiene_uci',bool)
                              ])

def leer_centros(path:str) -> list[CentroSanitario]:
    centros = []
    with open(path , encoding='utf-8') as f:
        lector = csv.DictReader(f,delimiter=';')
        for fila in lector:
            nombre = fila['NOMBRE']
            localidad = fila['LOCALIDAD']
            latitud = float(fila['LATITUD'])
            longitud = float(fila['LONGITUD'])
            ubicacion = Coordenadas(latitud, longitud)
            estado = fila['ESTADO']
            num_camas = int(fila['NUM_CAMAS'])
            acceso_discapacitados = fila['TIENE_ACCESO_DISCAPACITADOS'].lower() == 'true'
            tiene_uci = fila['TIENE_UCI'].lower() == 'true'

            centro = CentroSanitario(
                nombre,
                localidad,
                ubicacion,
                estado,
                num_camas,
                acceso_discapacitados,
                tiene_uci
            )
            centros.append(centro)
    return centros

def calcular_total_camas_centros_accesibles(centros: List[CentroSanitario]) -> int:
    '''
    recibe una lista de tuplas de tipo ```CentroSanitario``` 
    y produce como salida un entero correspondiente al número 
    total de camas de los centros sanitarios accesibles para 
    discapacitados.
    '''
    total_camas = 0
    for centro in centros:
        if centro.acceso_discapacitados:
            total_camas += centro.num_camas
    return total_camas

def obtener_centros_con_uci_cercanos_a(centros:List[CentroSanitario], coord: Coordenadas, umbral: float) -> List[(str, str, Coordenadas)]:
    '''
    recibe una lista de tuplas de tipo ```CentroSanitario```; una tupla de tipo ```Coordenadas```, 
    que representa un punto; y un float, que representa un umbral de distancia. Produce como 
    salida una lista de tuplas ```(str, str, Coordenadas(float, float))``` con el nombre, 
    del centro, la localidad y la ubicacion de los centros **con uci** situados a una distancia 
    de las coordenadas dadas como parámetro menor o igual que el umbral dado.
    '''
    centros_uci_cercanos = []
    for centro in centros:
        coord_centro = centro.ubicacion
        distancia_al_centro = calcular_distancia(coord_centro,coord)
        if (centro.tiene_uci and distancia_al_centro <= umbral):
            centros_uci_cercanos.append((centro.nombre, centro.localidad, coord_centro))
    return centros_uci_cercanos

def generar_mapa(centros_cercanos: List[(str, str, Coordenadas)], url:str):
    '''
    recibe una lista de tuplas ```(str, str, Coordenadas(float, float))``` 
    con el nombre, del centro, la localidad y la ubicación del centro; 
    y una cadena, que representa la ruta de un fichero html, que se 
    generará con los centros geolocalizados. 

    Para implementar la función `generar_mapa` ayúdate de las funciones auxiliares 
    que se implementan en el módulo [mapas.py](./src/mapas.py). Además, ten en cuenta que:
1.	Primero debes crear un mapa. Usa la media de las coordenadas de las ubicaciones de los centros para centrar el mapa.
2.	Después ve agregando los marcadores al mapa que has creado mediante la función ```mapas.agrega_marcador```.
3.	Una vez añadidos todos los marcadores, guarda el mapa en el archivo html con `mapas.guarda_mapa`.
    '''
    corodenadas_centradas = calcular_media_coordenadas([centro[2] for centro in centros_cercanos])
    mapa = crea_mapa(corodenadas_centradas)

    for centro in centros_cercanos:
        agrega_marcador(mapa, centro[2], centro[1] ,'red')

    guarda_mapa(mapa, url)

if __name__ == '__main__':
    centros = leer_centros('./data/centrosSanitarios.csv')
    for centro in centros:
        print(centro)