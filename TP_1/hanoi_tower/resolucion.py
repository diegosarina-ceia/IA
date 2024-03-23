import tracemalloc
import time
from hanoi_states import StatesHanoi, ProblemHanoi
from tree_hanoi import NodeHanoi
from search import (
    breadth_first_graph_search,
    depth_first_search,
    iterative_deepening_depth_limited_search
)

search_algorithms = {
    "BFS": breadth_first_graph_search,
    "DFS": depth_first_search,
    "IDDFS": iterative_deepening_depth_limited_search,
}

def run_search_algorithm(algorithm, problem):
    start_time = time.perf_counter()
    tracemalloc.start()
    last_node = algorithm(problem)
    _, memory_peak = tracemalloc.get_traced_memory()
    memory_peak /= 1024 * 1024
    tracemalloc.stop()
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    return last_node, elapsed_time, memory_peak

def main():
    # Define el estado inicial y el estado objetivo del problema

    initial_state = StatesHanoi([5,4,3, 2, 1], [], [], max_disks=5)
    goal_state = StatesHanoi([], [], [5,4,3, 2, 1], max_disks=5)

    # Crea una instancia del problema de la Torre de Hanoi
    problem_hanoi = ProblemHanoi(initial=initial_state, goal=goal_state)

    metrics = {}

    # Ejecucion individual
    print("====== Realizando ejecucion individual ======")
    for search_method, search_function in search_algorithms.items():
        last_node, elapsed_time, memory_peak = run_search_algorithm(search_function, problem_hanoi)
        
        if isinstance(last_node, NodeHanoi):
            metrics[search_method] = {
                "elapsed_time": elapsed_time,
                "memory_peak": round(memory_peak, 2),
                "last_node": last_node
            }
        else:
            print(f"No se encuentra solución para el algoritmo: {search_method}")

    print("====== Resultados de la ejecucion individual ======")
    for search_method, metrics in metrics.items():
        print(f"====== Metodo de búsquda: {search_method} ======")
        print(f"Tiempo promedio: {metrics['elapsed_time']} [s]")
        print(f"Memoria máxima ocupada: {metrics['memory_peak']} [MB]")
        print(f"Longitud del camino de la solución: {metrics['last_node'].state.accumulated_cost}")
        print(f"==============================")
    
    # ========================================================================================
    #                                      Ejecucion multiples
    # ========================================================================================

    num_executions = 20
    print(f"====== Realizando ejecucion multiple para promediacion - numero de iteraciones: {num_executions} ======")
    metrics_multiple = {}
    for search_method, search_function in search_algorithms.items():
        elapsed_times = []
        memory_peaks = []
        cost = []
        for _ in range(num_executions):
            last_node, elapsed_time, memory_peak = run_search_algorithm(search_function, problem_hanoi)
            elapsed_times.append(elapsed_time)
            memory_peaks.append(memory_peak)
            cost.append(last_node.state.accumulated_cost)

        avg_elapsed_time = sum(elapsed_times) / len(elapsed_times)
        avg_memory_peak = sum(memory_peaks) / len(memory_peaks)
        avg_cost = sum(cost) / len(cost)

        metrics_multiple[search_method] = {
            "avg_elapsed_time": avg_elapsed_time,
            "avg_memory_peak": round(avg_memory_peak, 2),
            "last_node": avg_cost
        }

    print("====== Resultados de la ejecucion multiple ======")
    for search_method, metrics in metrics_multiple.items():
        print(f"Metodo de búsqueda: {search_method}")
        print(f"Tiempo promedio: {metrics['avg_elapsed_time']} [s]")
        print(f"Memoria máxima promedio ocupada: {metrics['avg_memory_peak']} [MB]")
        print(f"Longitud del camino de la solución: {metrics['last_node']}")
        print(f"==============================")
    
if __name__ == "__main__":
    main()