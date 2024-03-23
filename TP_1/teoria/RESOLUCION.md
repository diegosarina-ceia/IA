# Resolución TP Nº 1 - Torre de Hanoi

1. ¿Cuáles son los PEAS de este problema? (Performance, Environment, Actuators, Sensors)

    De acuerdo al problema que se trata de resolver, clasifico los PEAS como:

    - Performance (Rendimiento): Esta métrica, trata de medir cuál es la eficiencia en la resolución del problema. En este caso seria alcanzar el estado objetivo con el menor número de movimientos posibles y en el menor tiempo de ejecución.

    - Environment (Entorno): Este punto describe el entorno en el que el agente opera. En este caso, consiste en tres postes y cinco discos de tamaños diferentes apilados. Además el entorno es estático (no cambia mientras el agente está actuando), discreto (posiciones limitadas de los discos) y determinista (el próximo estado es predecible a partir del estado actual y la acción ejecutada).

    - Actuators (Actuadores): Son básicamente las acciones que el agente puede realizar. Nuevamente, en este caso son mover un disco de un poste a otro, siguiendo las reglas del juego.

    - Sensors (Sensores): Estos permiten al agente percibir el estado de su entorno y la información necesaria para tomar decisiones. Para nuestro problema estos pueden ser las representaciones internas del estado de los postes y la posición de cada disco.

2. ¿Cuáles son las propiedades del entorno de trabajo?
    
    Para nuestro trabajo práctico, tomando las características descritas en el punto N.º 1. Las propiedades del entorno de las Torres de Hanoi son:

    - Estático: no cambia mientras el agente está actuando, es decir, que no cambia con el tiempo por sí solo.
    - Discreto: hay un número finito de movimientos y estados posibles.
    - Determinista: cada acción tiene un resultado predecible (el próximo estado es predecible a partir del estado actual y la acción ejecutada).
    - Secuencial: las decisiones se toman secuencia a secuencia para resolver el problema.

3. En el contexto de este problema, establezca cuáles son los: estado, espacio de estados, árbol de búsqueda, nodo de búsqueda, objetivo, acción y frontera.

    De acuerdo al enunciado, definimos que:

    - Estado: representa una configuración específica de los discos en los tres postes. Por ejemplo, un estado inicial lo podemos representar como `[[5,4,3,2,1],[] ,[]]`, donde `[5,4,3,2,1]` representa los discos del más grande al más pequeño en el primer poste, y los otros postes están vacíos.

    - Espacio de Estados: El espacio de estados incluye todas las configuraciones posibles de los discos en los postes, desde el estado inicial hasta el estado objetivo. Para 5 discos, el número de estados posibles es 3^5^ = 243 posibles estados.
    
    - Árbol de Búsqueda: El árbol de búsqueda es una estructura que representa todas las secuencias posibles de movimientos desde el estado inicial hasta el estado objetivo. Cada nodo del árbol es un estado potencial en el espacio de estados, y cada conexión entre nodos representa un movimiento de un disco. La raíz del árbol es el estado inicial, y las hojas son los posibles estados finales (objetivos o no).

    - Nodo de Búsqueda: un nodo de búsqueda en el árbol representa un estado específico del problema junto con la información adicional necesaria para la búsqueda, como el camino (secuencia de acciones) tomado para llegar a ese estado desde el inicio, el costo de ese camino, y posiblemente, una estimación del costo restante para alcanzar el objetivo.

    - Objetivo: el objetivo es el estado o los estados que se quieren alcanzar, que satisfacen el problema. Para este problema en particular, el objetivo es tener todos los discos en el tercer poste, ordenados de mayor a menor.

    - Acción: una acción es un movimiento permitido dentro del juego, que cambia el estado de la configuración de los discos. Las acciones posibles de este problema, se limitan a mover el disco superior de un poste a otro poste, siempre y cuando el movimiento cumpla con la regla de que un disco más grande no puede estar sobre un disco más pequeño.

    - Frontera: la frontera es el conjunto de todos los nodos en el árbol de búsqueda que han sido generados pero aún no explorados. Es decir, son estados para los cuales hemos considerado las posibles acciones para llegar hasta ellos, pero aún no hemos explorado sus propios estados sucesores. La frontera es crucial en el proceso de búsqueda, ya que determina cuál será el próximo estado (nodo) a explorar en búsqueda de la solución.


4. Implemente algún método de búsqueda. Puedes elegir cualquiera menos búsqueda en anchura primero (el desarrollado en clase). Sos libre de elegir cualquiera de los vistos en clases, o inclusive buscar nuevos.

    Los métodos de búsqueda implementados, se encuentran en el archivo [search.py](/IA/TP_1/hanoi_tower/search.py) en el mismo he realizado la implementación de dos algoritmos diferentes, siendo estos:
    - Búsqueda primero en profundidad (DFS)
    - Búsqueda de profundidad limitada con profundidad iterativa (IDLDFS)
    
5. ¿Qué complejidad en tiempo y memoria tiene el algoritmo elegido?

    La complejidad de tiempo y memoria que tienen los algoritmos que he realizado son:

    |                         | DFS | IDLDFS |
    |-------------------------|--------- |----------|
    | Complejidad en Tiempo   | O($b^m$) | O($b^d$) |
    | Complejidad en Memoria  | O($bm$)  | O($bd$) |

    Donde:
    
    - b: factor de ramificación
    - m: profundidad máxima del árbol de búsqueda
    - d: profundidad de la solución más superficial

6. A nivel implementación, ¿qué tiempo y memoria ocupa el algoritmo?

    Con respecto a la implementación que ocupan, realizando el promedio a lo largo de **20 ejecuciones** de cada método, obteniendo:

    | Método de búsqueda | Tiempo promedio [s] | Memoria máxima promedio ocupada [MB] |
    |--------------------|---------------------|--------------------------------------|
    | BFS                | 0.04239820840302    | 0.23                                 |
    | DFS                | 0.01551018754835    | 0.14                                 |
    | IDDFS              | 4.74632246865076    | 1.92                                 |

7. Si la solución óptima es $2^k - 1$ movimientos con *k* igual al número de discos. Qué tan lejos está la solución del algoritmo implementado de esta solución óptima. Se tomaron 20 muestras

    | Método de búsqueda | Longitud del camino | Diferencia respecto a la solución óptima |
    |---------------------|---------------------|-----------------------------------------|
    | BFS                 | 31.0                | 0 movimientos                           |
    | DFS                 | 81.0                | 50 movimientos                          |
    | IDDFS               | 31.0                | 0 movimientos                          |

    Cabe destacar que BFS es la solución que se encontraba brindada y no fue implementada por mí, solo la ejecute para tomarla de referencia. Por ende los métodos de búsqueda que desarrolle consiguieron para el caso de IDDFS llegar a la solución óptima y para el caso de DFS quedo a 50 movimientos de la solución óptima.