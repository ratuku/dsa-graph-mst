import sys
from pathlib import Path

# Direct script execution needs the project root to resolve src imports.
if not __package__:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.mapper.GraphMapper import GraphMapper
from src.algorithms.shortest_path import *
from src.algorithms.minimum_spanning_tree import *
from src.algorithms.topological_sort import *

class UIRunner:

    def start(self):
        """Main chatbot execution"""

        while True:
            self.main_text()
            user_data_input_choice = input("").strip()
            if user_data_input_choice == "3":
                break

            try:
                if user_data_input_choice == "1":
                    graph = GraphMapper.mapp_to_graph()
                elif user_data_input_choice == "2":
                    user_graph_details = self._read_multiline("Enter Graph Details")
                    graph = GraphMapper.mapp_to_graph_from_console(user_graph_details)
                else:
                    print(f"Invalid choice: {user_data_input_choice}, try again")
                    continue
            except (OSError, ValueError) as e:
                print(f"Error: {e}")
                continue

            if self._analysis_menu(graph) == "Exit":
                break

        print("Goodbye!")

    def _analysis_menu(self, graph) -> str:
        """Now time to run the analysis"""
        while True:
            self.main_analysis_text()
            user_data_input_choice = input("").strip()
            try:
                if user_data_input_choice == "1":
                    source = graph.get_node(input("Enter Node Source Name\n").strip())
                    dijkstra(graph, source.get_name())
                elif user_data_input_choice == "2":
                    minimum_spanning_tree(graph)
                elif user_data_input_choice == "3":
                    topological_sort(graph)
                elif user_data_input_choice == "4":
                    return "Reload"
                    # only from inner loop
                elif user_data_input_choice == "5":
                    return "Exit"
                    # break fully from outer loop
                else:
                    print(f"Invalid choice: {user_data_input_choice}, try again")
                    continue
            except (ValueError, TypeError) as e:
                print(f"Error: {e},\n try again")

    def main_text(self):
        """Display welcome message"""
        print("\nWelcome DSA Project 2: Graph Analysis!")
        print("\nEnsure that your data is in graph-data.txt or you choose to enter data here")
        print("\nChose Options Below:")
        print("\n1. Use Data Under Resources")
        print("\n2. User Terminal to Enter Data")
        print("\n3. Exit")

    def main_analysis_text(self):
        print("\nWhich Analysis would you like to do?:")
        print("1. Single-source Shortest Path Algorithm - Using Dijkstra")
        print("2. Minimum Spanning Tree Algorithm (Kruskal)")
        print("3. DFS - Topological Sorting and Cycles")
        print("4. Re-enter Data")
        print("5. Exit")

    @staticmethod
    def _read_multiline(prompt: str) -> str:
        print(f"{prompt} (finish with an empty line):")
        lines = []
        while (line := input()).strip():
            lines.append(line)
        return "\n".join(lines)

if __name__ == "__main__":
    UIRunner().start()