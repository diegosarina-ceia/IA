from collections import deque
from queue import LifoQueue
import tree_hanoi
from tree_hanoi import *
import hanoi_states


def breadth_first_tree_search(problem: hanoi_states.ProblemHanoi):
    """
    Realiza una búsqueda en anchura para encontrar una solución a un problema de Hanoi.
    Esta función no chequea si un estado se visito, por lo que puede entrar en Loop infinitos muy fácilmente. No
    usarla con más de 3 discos.

    Parameters:
        problem (hanoi_states.ProblemHanoi): El problema de la Torre de Hanoi a resolver.

    Returns:
        tree_hanoi.NodeHanoi: El nodo que contiene la solución encontrada.
    """
    frontier = deque([tree_hanoi.NodeHanoi(problem.initial)])  # Creamos una cola FIFO con el nodo inicial
    while frontier:
        node = frontier.popleft()  # Extraemos el primer nodo de la cola
        if problem.goal_test(node.state):  # Comprobamos si hemos alcanzado el estado objetivo
            return node
        frontier.extend(node.expand(problem))  # type: ignore # Agregamos a la cola todos los nodos sucesores del nodo actual

    return None


def breadth_first_graph_search(problem: hanoi_states.ProblemHanoi, display: bool = False):
    """
    Realiza una búsqueda en anchura para encontrar una solución a un problema de Hanoi. Pero ahora si recuerda si ya
    paso por un estado e ignora seguir buscando en ese nodo para evitar recursividad.

    Parameters:
        problem (hanoi_states.ProblemHanoi): El problema de la Torre de Hanoi a resolver.
        display (bool, optional): Muestra un mensaje de cuantos caminos se expandieron y cuantos quedaron sin expandir.
                                  Por defecto es False.

    Returns:
        tree_hanoi.NodeHanoi: El nodo que contiene la solución encontrada.
    """

    frontier = deque([tree_hanoi.NodeHanoi(problem.initial)])  # Creamos una cola FIFO con el nodo inicial

    explored = set()  # Este set nos permite ver si ya exploramos un estado para evitar repetir indefinidamente
    while frontier:
        node = frontier.popleft()  # Extraemos el primer nodo de la cola

        # Agregamos nodo al set. Esto evita guardar duplicados, porque set nunca tiene elementos repetidos, esto sirve
        # porque heredamos el método __eq__ en tree_hanoi.NodeHanoi de aima.Node
        explored.add(node.state)

        if problem.goal_test(node.state):  # Comprobamos si hemos alcanzado el estado objetivo
            if display:
                print(len(explored), "caminos se expandieron y", len(frontier), "caminos quedaron en la frontera")
            return node
        # Agregamos a la cola todos los nodos sucesores del nodo actual que no haya visitados
        frontier.extend(child for child in node.expand(problem)
                        if child.state not in explored and child not in frontier) # type: ignore

    return None


# ======================================================================================================================
#                                       Implementacion metodos de busqueda
# ======================================================================================================================

def depth_first_search(problem: hanoi_states.ProblemHanoi, display: bool = False):
    """
    Realiza una búsqueda primero en profundidad para encontrar una solución a un problema de Hanoi. Recordando si ya
    paso por un estado e ignora seguir buscando en ese nodo para evitar recursividad.

    Parameters:
        problem (hanoi_states.ProblemHanoi): El problema de la Torre de Hanoi a resolver.
        display (bool, optional): Muestra un mensaje de cuantos caminos se expandieron y cuantos quedaron sin expandir.
                                  Por defecto es False.

    Returns:
        tree_hanoi.NodeHanoi: El nodo que contiene la solución encontrada.
    """
    frontier = LifoQueue()  # Creamos una cola LIFO con el nodo inicial
    frontier.put(tree_hanoi.NodeHanoi(problem.initial))  # Agregamos el nodo inicial a la cola

    explored = set()  # Este set nos permite ver si ya exploramos un estado para evitar repetir indefinidamente
    while frontier:
        node = frontier.get()  # Extraemos el último nodo de la cola LIFO

        explored.add(node.state)

        if problem.goal_test(node.state):  # Comprobamos si hemos alcanzado el estado objetivo
            if display:
                print(len(explored), "caminos se expandieron y", frontier.qsize(), "caminos quedaron en la frontera")
            return node

        # Agregamos a la cola LIFO todos los nodos sucesores del nodo actual que no hayan sido visitados
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier.queue:
                frontier.put(child)

    return None


def depth_limited(problem: hanoi_states.ProblemHanoi, limit: int, display: bool = False):
    """
    Realiza una búsqueda en profundidad pero limitada, retornando asi al nodo padre cuando el limite se alcanza. 
    Recuerda ademas si ya paso por un estado e ignora seguir buscando en ese nodo para evitar recursividad.

    Parameters:
        problem (hanoi_states.ProblemHanoi): El problema de la Torre de Hanoi a resolver.
        limit (int): El limite de profundidad a llegar
        display (bool, optional): Muestra un mensaje de cuantos caminos se expandieron y cuantos quedaron sin expandir.
                                  Por defecto es False.

    Returns:
        tree_hanoi.NodeHanoi: El nodo que contiene la solución encontrada.
    """
    frontier = LifoQueue() # Creamos una cola LIFO con el nodo inicial
    frontier.put((NodeHanoi(problem.initial), 0))  # Tupla inicial y profundidad
    explored = set()

    result = "failure"
    while frontier.qsize() > 0:
        node_tuple = frontier.get()
        node = node_tuple[0]  # Obtener el nodo de la tupla
        node_depth = node_tuple[1]  # Obtener la profundidad de la tupla
        
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "caminos se expandieron y", frontier.qsize(), "caminos quedaron en la frontera")
            return node
        
        if node_depth > limit:
            result = "cutoff"
        elif (node.state, node_depth) not in explored:  # Almacenar el estado y su profundidad en explored
            explored.add((node.state, node_depth))
            for child in node.expand(problem):
                child_tuple = (child, node_depth + 1)  # Crear la tupla para el hijo con la profundidad incrementada
                frontier.put(child_tuple)  # Insertar la tupla del hijo en la cola
    
    return result

def iterative_deepening_depth_limited_search(problem: hanoi_states.ProblemHanoi, display: bool = False):
    """
    Realiza una búsqueda en profundidad pero iterando el limite de esta, retornando asi al nodo padre cuando el limite se alcanza. 

    Parameters:
        problem (hanoi_states.ProblemHanoi): El problema de la Torre de Hanoi a resolver.
        display (bool, optional): Muestra un mensaje de cuantos caminos se expandieron y cuantos quedaron sin expandir.
                                  Por defecto es False.

    Returns:
        tree_hanoi.NodeHanoi: El nodo que contiene la solución encontrada.
    """
    depth = 0
    while True:
        result = depth_limited(problem, depth, display)
        if result != "cutoff":
            return result
        depth += 1



