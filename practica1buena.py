# AIA
# Problemas de Satisfacción de Restricciones
# Dpto. de C. de la Computación e I.A. (Univ. de Sevilla)
# ===================================================================

# En esta práctica vamos a programar el algoritmo de backtracking
# combinado con consistencia de arcos AC3 y la heurística MRV. 

import random, copy

# ===================================================================
# Representación de problemas de satisfacción de restricciones
# ===================================================================

#   Definimos la clase PSR que servirá para representar problemas de
# satisfacción de restricciones.

# La clase tiene cuatro atributos:
# - variables: una lista con las variables del problema.
# - dominios: un diccionario que asocia a cada variable su dominio,
#      una lista con los valores posibles.
# - restricciones: un diccionario que asigna a cada tupla de
#      variables la restricción que relaciona a esas variables.
# - vecinos: un diccionario que asigna a cada variables una lista con
#      las variables con las que tiene una restricción asociada.

# El constructor de la clase recibe los valores de los atributos
# "dominios" y "restricciones". Los otros dos atributos se definen a
# partir de éstos valores.

# NOTA IMPORTANTE: Supondremos en adelante que todas las
# restricciones son binarias y que existe a lo sumo una restricción
# por cada par de variables.

class PSR:
    """Clase que describe un problema de satisfacción de
    restricciones, con los siguientes atributos:
       variables     Lista de las variables del problema
       dominios      Diccionario que asigna a cada variable su dominio
                     (una lista con los valores posibles)
       restricciones Diccionario que asocia a cada tupla de variables
                     involucrada en una restricción, una función que,
                     dados valores de los dominios de esas variables,
                     determina si cumplen o no la restricción.
                     IMPORTANTE: Supondremos que para cada combinación
                     de variables hay a lo sumo una restricción (por
                     ejemplo, si hubiera dos restricciones binarias
                     sobre el mismo par de variables, consideraríamos
                     la conjunción de ambas). 
                     También supondremos que todas las restricciones
                     son binarias
        vecinos      Diccionario que representa el grafo del PSR,
                     asociando a cada variable, una lista de las
                     variables con las que comparte restricción.

    El constructor recibe los valores de los atributos dominios y
    restricciones; los otros dos atributos serán calculados al
    construir la instancia."""

    def __init__(self, dominios, restricciones):
        """Constructor de PSRs."""

        self.dominios = dominios
        self.restricciones = restricciones
        self.variables = list(dominios.keys())

        vecinos = {v: [] for v in self.variables}
        for v1, v2 in restricciones:
            vecinos[v1].append(v2)
            vecinos[v2].append(v1)
        self.vecinos = vecinos

# ===================================================================
# Ejercicio 1
# ===================================================================

#   Definir una función n_reinas(n), que recibiendo como entrada un
# número natural n, devuelva una instancia de la clase PSR,
# correspondiente al problema de las n-reinas.
def n_reinas_restriccion(x,y):
    return (lambda vx, vy: vx!= vy #restriccion para que no esten en la misma fila
                and abs(x-y)!=abs(vx-vy)) #restriccion para que no esten en la misma columna

def n_reinas(n):
    doms = {i:[j for j in range(1,n+1)] for i in range(1,n+1)}
    restr = dict()
    for x in range(1,n):
        for y in range(x+1,n+1):
            restr[(x,y)] = n_reinas_restriccion(x,y) 
    return PSR(doms, restr)
# Ejemplos:
print(n_reinas(4))
# >>> psr_n4 = n_reinas(4)
# >>> psr_n4.variables
# [1, 2, 3, 4]
# >>> psr_n4.dominios
# {1: [1, 2, 3, 4], 2: [1, 2, 3, 4], 3: [1, 2, 3, 4], 4: [1, 2, 3, 4]}
# >>> psr_n4.restricciones
# {(1, 2): <function <lambda> at ...>,
#  (1, 3): <function <lambda> at ...>,
#  (1, 4): <function <lambda> at ...>,
#  (2, 3): <function <lambda> at ...>,
#  (3, 4): <function <lambda> at ...>,
#  (2, 4): <function <lambda> at ...>}
# >>> psr_n4.vecinos
# {1: [2, 3, 4], 2: [1, 3, 4], 3: [1, 2, 4], 4: [1, 2, 3]}
# >>> psr_n4.restricciones[(1,4)](2,3)
# True
# >>> psr_n4.restricciones[(1,4)](4,1)
# False


# Definir una funcion coloreado_mapas(mapa, colores) que devuelva un PSR correspondiente a colorear ese mapa con esos colores
mapa_andalucia = {  "Huelva":["Cadiz","Sevilla"],
                    "Sevilla":["Cadiz","Cordoba","Huelva","Malaga"],
                    "Cadiz":["Malaga","Sevilla","Huelva"],
                    "Cordoba": ["Jaen","Granada","Malaga","Sevilla"],
                    "Malaga":["Cadiz","Sevilla","Cordoba","Granada"],
                    "Jaen":["Cordoba","Granada"],
                    "Granada":["Cordoba","Jaen","Almeria","Malaga"],
                    "Almeria":["Granada"]}

def coloreado_restricciones(x,y,mapa):

    return (lambda vx, vy:  vy!=vx if x in mapa[y] else True)   #si las ciudades son vecinas miramos si los colores son iguales
                                                                #si no son vecinas entonces True

def coloreado_mapas(mapa, colores):

    doms = {i:colores for i in mapa} #cada ciudad puede tomar el valor de cualquier color

    restr = {(i,k):lambda x,y: True for i in mapa for k in mapa} #inicializamos las restricciones con todo a True

    restantes = list(mapa) #lista para no repetir dos veces la misma tupla. Por ejemplo (Sevilla, Granada) (Granada, Sevilla)

    for x in mapa:
        restantes.remove(x) #Ya hemos pasado por x asi que la quitamos

        for y in restantes: 
            restr[(x,y)] = coloreado_restricciones(x,y,mapa) #para dar valor a cada tupla miramos si cumple o no la restriccion
            
    return PSR(doms,restr)

print("VARIABLES:")
print(coloreado_mapas(mapa_andalucia,["R","V","A"]).variables)
print("-------------------------------------------------------")
print("DOMINIOS:")
print(coloreado_mapas(mapa_andalucia,["R","V","A"]).dominios)
print("-------------------------------------------------------")
print("RESTRICCION:")
print(coloreado_mapas(mapa_andalucia,["R","V","A"]).restricciones[("Cordoba","Cordoba")]("R","R"))







# ===================================================================
# Parte II: Algoritmo de consistencia de arcos AC3
# ===================================================================

#   En esta parte vamos a definir el algoritmo de consistencia de arcos
# AC3 que, dado un problema de satisfacción de restricciones,
# devuelve una representación equivalente que cumple la propiedad de
# ser arco consistente (y que usualmente tiene dominios más
# reducidos.)

#   Dado un PSR, un arco es una restricción cualquiera del problema,
# asociada con una de las variables implicadas en la misma, a la que
# llamaremos variable distinguida.





# ===================================================================
# Ejercicio 2
# ===================================================================

#   Definir una función restriccion_arco que, dado un PSR, la
# variable distinguida de un arco y la variable asociada; devuelva
# una función que, dado un elemento del dominio de la variable
# distinguida y otro de la variable asociada, determine si verifican
# la restricción asociada al arco.

# Ejemplos:

# >>> restriccion_arco(psr_n4, 1, 2)
# <function n_reinas.<locals>.n_reinas_restriccion.<locals>.<lambda>
# at 0x7fdfa13d30d0>
# >>> restriccion_arco(psr_n4, 1, 2)(1, 4)
# True
# >>> restriccion_arco(psr_n4, 1, 2)(3, 2)
# False






       
# ===================================================================
# Ejercicio 3
# ===================================================================

#   Definir un método arcos para la clase PSR que construya un
# conjunto con todos los arcos asociados al conjunto de restricciones
# del problema. Utilizaremos las tuplas para representar a los
# arcos. El primer elemento será la variable distinguida y el segundo
# la variable asociada.

# Ejemplo:

# >>> psr_n4 = n_reinas(4)
# >>> arcos_n4 = psr_n4.arcos()
# >>> arcos_n4
# [(1, 2), (2, 1), (1, 3), (3, 1), (2, 3), (3, 2), (3, 4), (4, 3),
#  (2, 4), (4, 2), (1, 4), (4, 1)]
# >>> psr_n4.restriccion_arco(1, 2)(4, 1)
# True
# >>> psr_n4.restriccion_arco(1, 2)(2, 3)
# False









# ===================================================================
# Ejercicio 4
# ===================================================================

#   Definir la función AC3(psr,doms) que, recibiendo como entrada una
# instancia de la clase PSR y diccionario doms que a cada variable
# del problema le asigna un dominio, aplica el algoritmo de
# consistencia de arcos AC3 a los dominios recibidos (ver tema 1).

# NOTA: La función AC3 debe actualizar los dominios de forma
# destructiva (es decir, después de ejecutar la llamada "AC3(psr,
# doms)", en el diccionario doms debe quedar actualizados.

# Ejemplos:

# >>> psr_n4=n_reinas(4)
# >>> dominios = {1:[2,4],2:[1,2,3,4],3:[1,2,3,4],4:[1,2,3,4]}
# >>> AC3(psr_n4, dominios)
# >>> dominios
# {1: [2, 4], 2: [1, 4], 3: [1, 3], 4: [1, 3, 4]}

# >>> dominios = {1:[1],2:[1,2,3,4],3:[1,2,3,4],4:[1,2,3,4]}
# >>> AC3(psr_n4,dominios)
# >>> dominios
# {1: [], 2: [], 3: [], 4: []}

# >>> dominios = {1:[1,2,3,4],2:[3,4],3:[1,4],4:[1,2,3,4]}
# >>> AC3(psr_n4,dominios)
# >>> dominios
# {1: [2], 2: [4], 3: [1], 4: [3]}







# ===================================================================
# Parte III: Algoritmo de búsqueda AC3
# ===================================================================


# ===================================================================
# Ejercicio 5
# ===================================================================


# Definir una función parte_dominio(doms), que a partir de un diccionario doms
# en el que cada variable del problema tiene asignado un dominio de posibles
# valores (como los que obtiene el algoritmo AC-3 anterior), devuelve dos
# diccionarios obtenidos partiendo en dos el primero de los dominios que no
# sea unitario.   

# Nota: Supondremos que el diccionario doms que se recibe no tiene dominios
# vacíos y que al menos uno de los dominios no es unitario. El método para
# partir en dos el dominio se deja a libre elección (basta con que sea una
# partición en dos). 

# Ejemplo:

# >>> doms4_1={1: [2, 4], 2: [1, 4], 3: [1, 3], 4: [1, 3, 4]}
# >>> parte_dominios(doms4_1)
# ({1: [2], 2: [1, 4], 3: [1, 3], 4: [1, 3, 4]}, {1: [4], 2: [1, 4], 3: [1, 3], 4: [1, 3, 4]})







# ===================================================================
# Ejercicio 6
# ===================================================================

# Definir la función búsqueda_AC3(psr), que recibiendo como entrada un psr
# (tal y como se define en el ejercicio 1), aplica el algoritmo de búsqueda
# AC-3 tal y como se define en el tema 2

# Ejemplos:

# >>> psr_nreinas4=n_reinas(4)
# >>> busqueda_AC3(psr_nreinas4)
# {1: 3, 2: 1, 3: 4, 4: 2}
# >>> psr_nreinas3=n_reinas(3)
# >>> busqueda_AC3(psr_nreinas3)
# No hay solución






# ===================================================================
# Ejercicio 7
# ===================================================================



#   En este ejercicio no se pide ninguna función. Tan sólo comprobar el
# algoritmo resolviendo diversas instancias del problema de las 
# n_reinas. Para visualizar las soluciones, puede ser útil la siguiente
# función:

def dibuja_tablero_n_reinas(asig):

    def cadena_fila(i,asig):
        cadena="|"
        for j in range (1,n+1):
            if asig[i]==j:
                cadena += "X|"
            else:
                cadena += " |"
        return cadena

    n=len(asig)
    print("+"+"-"*(2*n-1)+"+")
    for i in range(1,n):
        print(cadena_fila(i,asig))
        print("|"+"-"*(2*n-1)+"|")
    print(cadena_fila(n,asig))
    print("+"+"-"*(2*n-1)+"+")

# Ejemplos:


# >>> dibuja_tablero_n_reinas(busqueda_AC3(n_reinas(4)))
# +-------+
# | | |X| |
# |-------|
# |X| | | |
# |-------|
# | | | |X|
# |-------|
# | |X| | |
# +-------+

# >>> dibuja_tablero_n_reinas(busqueda_AC3(n_reinas(6)))
# +-----------+
# | | | | |X| |
# |-----------|
# | | |X| | | |
# |-----------|
# |X| | | | | |
# |-----------|
# | | | | | |X|
# |-----------|
# | | | |X| | |
# |-----------|
# | |X| | | | |
# +-----------+

# >>> dibuja_tablero_n_reinas(busqueda_AC3(n_reinas(8)))
# +---------------+
# | | | | | | | |X|
# |---------------|
# | | | |X| | | | |
# |---------------|
# |X| | | | | | | |
# |---------------|
# | | |X| | | | | |
# |---------------|
# | | | | | |X| | |
# |---------------|
# | |X| | | | | | |
# |---------------|
# | | | | | | |X| |
# |---------------|
# | | | | |X| | | |
# +---------------+

# >>> dibuja_tablero_n_reinas(busqueda_AC3(n_reinas(14)))
# +---------------------------+
# | | | | | | | | | | | | | |X|
# |---------------------------|
# | | | | | | | | | | | |X| | |
# |---------------------------|
# | | | | | | | | | |X| | | | |
# |---------------------------|
# | | | | | | | |X| | | | | | |
# |---------------------------|
# | | |X| | | | | | | | | | | |
# |---------------------------|
# | | | | |X| | | | | | | | | |
# |---------------------------|
# | |X| | | | | | | | | | | | |
# |---------------------------|
# | | | | | | | | | | |X| | | |
# |---------------------------|
# |X| | | | | | | | | | | | | |
# |---------------------------|
# | | | | | |X| | | | | | | | |
# |---------------------------|
# | | | | | | | | | | | | |X| |
# |---------------------------|
# | | | | | | | | |X| | | | | |
# |---------------------------|
# | | | | | | |X| | | | | | | |
# |---------------------------|
# | | | |X| | | | | | | | | | |
# +---------------------------+



