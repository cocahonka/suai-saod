import os
from dataclasses import dataclass
from typing import Any, Callable, List

from lab6.algs.adjacency_matrix.dijkstra import dijkstra
from lab6.algs.adjacency_matrix.topological_sort import topological_sort
from lab6.graph.adjacency_matrix_graph import AdjacencyMatrixGraph
from lab6.graph.graph import GraphTraversalType, IGraph
from lab6.serializers.graph_serializer import GraphSerializer


@dataclass
class City:
    name: str
    population: int
    area: float

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name


def prefix(length: int = 20) -> Callable[..., Any]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args: Any, **kwargs: Any) -> object:
            print(f"{'=' * length} {func.__name__} {'=' * length}")
            return func(*args, **kwargs)

        return wrapper

    return decorator


def main() -> None:
    end: str = "\n\n"

    directed_graph_str: IGraph[str, int] = AdjacencyMatrixGraph(is_directed=True)
    undirected_graph_city: IGraph[City, float] = AdjacencyMatrixGraph(is_directed=False)

    saint_petersburg = City("Saint Petersburg", 5398064, 1403)
    sosnovy_bor = City("Sosnovy Bor", 65931, 10)
    syktyvkar = City("Syktyvkar", 235006, 144)
    bryansk = City("Bryansk", 411151, 124)
    pushkin = City("Pushkin", 84743, 7)
    magic_city = City("Magic City", 0, 0)
    gravity_falls = City("Gravity Falls", 0, 0)
    cities = [saint_petersburg, sosnovy_bor, syktyvkar, bryansk, pushkin, magic_city, gravity_falls]

    undirected_graph_city.add_all(cities)
    undirected_graph_city.connect_all(
        [
            (saint_petersburg, sosnovy_bor, 100.1),
            (saint_petersburg, syktyvkar, 1495.7),
            (saint_petersburg, bryansk, 1081.4),
            (saint_petersburg, pushkin, 26.7),
            (sosnovy_bor, syktyvkar, 1485.3),
            (pushkin, bryansk, 1088.1),
            (magic_city, pushkin, 50),
            (magic_city, syktyvkar, 150),
        ]
    )

    directed_graph_str.add_all(["X1", "X2", "X3", "X4", "X5", "X6", "X7"])
    directed_graph_str.connect_all(
        [
            ("X1", "X3", 11),
            ("X1", "X4", 15),
            ("X1", "X5", 7),
            ("X2", "X5", 14),
            ("X2", "X6", 18),
            ("X3", "X2", 9),
            ("X3", "X4", 13),
            ("X3", "X5", 7),
            ("X3", "X6", 11),
            ("X3", "X7", 22),
            ("X4", "X6", 11),
            ("X4", "X7", 16),
            ("X5", "X6", 8),
            ("X5", "X7", 23),
            ("X6", "X7", 19),
        ]
    )

    @prefix()
    def present_graphs() -> None:
        print(f"Cities graph:\n{undirected_graph_city}", end=end)
        print(f"Directed graph:\n{directed_graph_str}", end=end)

        print(
            f"Edges of directed graph:\n{'\n'.join(str(x) for x in directed_graph_str.get_edges())}\n"
        )
        print(
            f"Edges of cities graph:\n{'\n'.join(str(x) for x in undirected_graph_city.get_edges())}",
            end=end,
        )

    @prefix()
    def basic_methods() -> None:
        print(f"Is directed graph cyclic: {directed_graph_str.is_cyclic}")
        print(f"Is cities graph cyclic: {undirected_graph_city.is_cyclic}", end=end)

        print(f"Is directed graph connected: {directed_graph_str.is_connected}")
        print(f"Is cities graph connected: {undirected_graph_city.is_connected}", end=end)

        print(f"Directed graph edge count: {directed_graph_str.edge_count}")
        print(f"Cities graph edge count: {undirected_graph_city.edge_count}", end=end)

        print(f"Directed graph vertex count: {directed_graph_str.vertex_count}")
        print(f"Cities graph vertex count: {undirected_graph_city.vertex_count}", end=end)

        print(f"Directed graph contains 'X8': {'X8' in directed_graph_str}")
        print(
            f"Cities graph contains 'Pushkin': {undirected_graph_city.contains(pushkin)}", end=end
        )

        print(f"Is 'X1' connected to 'X7': {directed_graph_str.is_connected_to('X1', 'X5')}")
        print(
            f"Is 'Magic City' connected to 'Gravity Falls': {undirected_graph_city.is_connected_to(magic_city, gravity_falls)}",
            end=end,
        )

        print(f"Weight between 'X1' and 'X5': {directed_graph_str.get_weight('X1', 'X5')}")
        print(
            f"Weight between 'Saint Petersburg' and 'Sosnovy Bor': {undirected_graph_city.get_weight(saint_petersburg, sosnovy_bor)}",
            end=end,
        )

        print(f"Successors of 'X1': {directed_graph_str.get_successors('X1')}")
        print(
            f"Successors of 'Saint Petersburg': {undirected_graph_city.get_successors(saint_petersburg)}",
            end=end,
        )

        print(f"Predecessors of 'X3': {directed_graph_str.get_predecessors('X3')}")
        print(
            f"Predecessors of 'Pushkin': {undirected_graph_city.get_predecessors(pushkin)}",
            end=end,
        )

        print(f"Neighbors of 'X3': {directed_graph_str.get_neighbors('X3')}")
        print(
            f"Neighbors of 'Pushkin': {undirected_graph_city.get_neighbors(pushkin)}",
            end=end,
        )

    @prefix()
    def path_finder_and_traverse() -> None:
        print(f"Path from 'X1' to 'X7': {directed_graph_str.get_path('X1', 'X7')}")
        print(
            f"Path from 'Pushkin' to 'Sosnovy Bor': {undirected_graph_city.get_path(pushkin, sosnovy_bor)}",
            end=end,
        )

        print(
            f"All paths from 'X1' to 'X7':\n{'\n'.join(str(x) for x in directed_graph_str.get_all_paths('X1', 'X7'))}\n"
        )
        print(
            f"All paths from 'Pushkin' to 'Sosnovy Bor':\n{'\n'.join(str(x) for x in undirected_graph_city.get_all_paths(pushkin, sosnovy_bor))}",
            end=end,
        )

        traverse: List[object] = []

        directed_graph_str.traverse(traverse.append, GraphTraversalType.DEPTH_FIRST)
        print(f"Depth first traverse of directed graph vertices: {traverse}")
        traverse.clear()

        directed_graph_str.traverse(traverse.append, GraphTraversalType.BREADTH_FIRST)
        print(f"Breadth first traverse of directed graph vertices: {traverse}")
        traverse.clear()

        undirected_graph_city.traverse(traverse.append, GraphTraversalType.DEPTH_FIRST)
        print(f"Depth first traverse of cities graph vertices: {traverse}")
        traverse.clear()

        undirected_graph_city.traverse(traverse.append, GraphTraversalType.BREADTH_FIRST)
        print(f"Breadth first traverse of cities graph vertices: {traverse}", end=end)
        traverse.clear()

        print(
            f"Depth first generator of directed graph vertices: {list(directed_graph_str.generator(GraphTraversalType.DEPTH_FIRST))}"
        )
        print(
            f"Breadth first generator of directed graph vertices: {list(directed_graph_str.generator(GraphTraversalType.BREADTH_FIRST))}"
        )
        print(
            f"Depth first generator of cities graph vertices: {list(undirected_graph_city.generator(GraphTraversalType.DEPTH_FIRST))}"
        )
        print(
            f"Breadth first generator of cities graph vertices: {list(undirected_graph_city.generator(GraphTraversalType.BREADTH_FIRST))}",
            end=end,
        )

    @prefix()
    def algorithms() -> None:
        assert isinstance(directed_graph_str, AdjacencyMatrixGraph)
        assert isinstance(undirected_graph_city, AdjacencyMatrixGraph)
        print(f"Dijkstra for directed graph (X1-X7): {dijkstra(directed_graph_str, 'X1', 'X7')}")
        print(f"Dijkstra for directed graph (X3-X6): {dijkstra(directed_graph_str, 'X3', 'X6')}")
        print(
            f"Dijkstra for directed graph (X7-X1): {dijkstra(directed_graph_str, 'X7', 'X1')}",
            end=end,
        )

        print(
            f"Dijkstra for cities graph (Sosnovy Bor - Syktyvkar): {dijkstra(undirected_graph_city, sosnovy_bor, syktyvkar)}",
        )
        print(
            f"Dijkstra for cities graph (Sosnovy Bor - Magic City): {dijkstra(undirected_graph_city, sosnovy_bor, magic_city)}",
        )
        print(
            f"Dijkstra for cities graph (Saint Petersburg - Gravity Falls): {dijkstra(undirected_graph_city, saint_petersburg, gravity_falls)}",
        )
        graph_city_copy: AdjacencyMatrixGraph[City, float] = undirected_graph_city.copy()
        graph_city_copy.remove(magic_city)
        print(
            f"Dijkstra for cities graph (without Magic City) (Sosnovy Bor - Syktyvkar): {dijkstra(graph_city_copy, sosnovy_bor, syktyvkar)}",
            end=end,
        )

        print(
            f"Topological sort for directed graph: {topological_sort(directed_graph_str)}", end=end
        )

    @prefix()
    def serialization() -> None:
        small_copy: IGraph[str, int] = directed_graph_str.copy()
        small_copy.remove_all(["X4", "X5"])

        print(f"Directed graph small copy:\n{small_copy}", end=end)

        GraphSerializer.save_graph_to_file(small_copy, "directed.json")

        with open("directed.json") as file:
            print(f"Directed graph from file:\n{file.read()}", end=end)

        os.remove("directed.json")

    present_graphs()
    basic_methods()
    path_finder_and_traverse()
    algorithms()
    serialization()


if __name__ == "__main__":
    main()
