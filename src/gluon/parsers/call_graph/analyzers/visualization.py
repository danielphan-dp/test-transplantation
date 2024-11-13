import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import pandas as pd
import numpy as np
from pathlib import Path
from collections import Counter, defaultdict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .repo_analyzer import RepoAnalyzer


class VisualizationGenerator:
    """Handles generation of visualizations for the call graph analysis"""

    def __init__(self, analyzer: "RepoAnalyzer"):
        self.analyzer = analyzer
        self.viz_dir = self.analyzer.output_dir / "visualizations"

    def generate_visualizations(self):
        """Generate all visualizations"""
        try:
            self.viz_dir.mkdir(exist_ok=True)

            if len(self.analyzer.module_graph) > 0:
                self._generate_module_visualization()
            if len(self.analyzer.call_graph) > 0:
                self._generate_call_graph_visualization()

            self._generate_statistics_visualizations()
            self._generate_test_visualizations()

        except ImportError as e:
            self.analyzer.logger.warning(f"Visualization packages not available: {str(e)}")
        except Exception as e:
            self.analyzer.logger.error(f"Error generating visualizations: {str(e)}")

    def _generate_module_visualization(self):
        """Generate module dependency visualization"""
        plt.figure(figsize=(15, 10))
        pos = nx.spring_layout(self.analyzer.module_graph)
        nx.draw(
            self.analyzer.module_graph,
            pos,
            with_labels=True,
            node_color="lightblue",
            node_size=2000,
            font_size=8,
            arrows=True,
        )
        plt.title("Module Dependencies")
        plt.savefig(self.viz_dir / "module_dependencies.png", bbox_inches="tight")
        plt.close()

    def _generate_call_graph_visualization(self):
        """Generate call graph visualization"""
        graph = (
            self._get_simplified_call_graph()
            if self.analyzer.call_graph.number_of_nodes() > 100
            else self.analyzer.call_graph
        )

        plt.figure(figsize=(20, 15))
        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, with_labels=True, node_color="lightgreen", node_size=1500, font_size=6, arrows=True)
        plt.title("Function Call Graph")
        plt.savefig(self.viz_dir / "call_graph.png", bbox_inches="tight")
        plt.close()

    def _generate_statistics_visualizations(self):
        """Generate statistical visualizations"""
        self._generate_degree_distribution()
        self._generate_module_complexity()
        self._generate_function_types()
        self._generate_module_dependencies_heatmap()
        self._generate_parameter_distribution()
        self._generate_decorator_usage()
        self._generate_module_centrality()

    def _generate_degree_distribution(self):
        """Generate degree distribution visualization"""
        plt.figure(figsize=(10, 6))
        degrees = [d for _, d in self.analyzer.call_graph.degree()]
        if degrees:
            plt.hist(degrees, bins=min(50, len(set(degrees))), alpha=0.75)
            plt.xlabel("Number of Connections")
            plt.ylabel("Frequency")
            plt.title("Function Connection Distribution")
            plt.savefig(self.viz_dir / "degree_distribution.png")
        plt.close()

    def _generate_module_complexity(self):
        """Generate module complexity visualization"""
        module_complexity = defaultdict(int)
        for node in self.analyzer.nodes.values():
            module_complexity[node.module] += 1

        if module_complexity:
            plt.figure(figsize=(12, 6))
            modules = list(module_complexity.keys())
            counts = list(module_complexity.values())
            plt.bar(range(len(modules)), counts)
            plt.xticks(range(len(modules)), modules, rotation=45, ha="right")
            plt.xlabel("Module")
            plt.ylabel("Number of Functions")
            plt.title("Module Complexity")
            plt.tight_layout()
            plt.savefig(self.viz_dir / "module_complexity.png")
        plt.close()

    def _generate_function_types(self):
        """Generate function types distribution visualization"""
        plt.figure(figsize=(10, 8))
        type_counts = Counter(node.type for node in self.analyzer.nodes.values())
        plt.pie(type_counts.values(), labels=type_counts.keys(), autopct="%1.1f%%")
        plt.title("Distribution of Function Types")
        plt.savefig(self.viz_dir / "function_types.png")
        plt.close()

    def _generate_module_dependencies_heatmap(self):
        """Generate module dependencies heatmap"""
        if len(self.analyzer.module_graph) > 0:
            plt.figure(figsize=(12, 10))
            modules = sorted(self.analyzer.module_graph.nodes())
            adj_matrix = nx.adjacency_matrix(self.analyzer.module_graph, nodelist=modules).todense()
            sns.heatmap(adj_matrix, xticklabels=modules, yticklabels=modules, cmap="YlOrRd", square=True)
            plt.title("Module Dependencies Heatmap")
            plt.xticks(rotation=45, ha="right")
            plt.yticks(rotation=0)
            plt.tight_layout()
            plt.savefig(self.viz_dir / "module_dependencies_heatmap.png")
            plt.close()

    def _generate_parameter_distribution(self):
        """Generate parameter distribution visualization"""
        plt.figure(figsize=(12, 6))
        param_counts = [len(node.parameters) for node in self.analyzer.nodes.values()]
        sns.boxplot(x=param_counts)
        sns.stripplot(x=param_counts, color="red", alpha=0.3)
        plt.title("Distribution of Function Parameters")
        plt.xlabel("Number of Parameters")
        plt.savefig(self.viz_dir / "parameter_distribution.png")
        plt.close()

    def _generate_decorator_usage(self):
        """Generate decorator usage visualization"""
        decorator_counts = Counter(
            [decorator for node in self.analyzer.nodes.values() for decorator in node.decorators]
        )
        if decorator_counts:
            plt.figure(figsize=(12, 6))
            decorators, counts = zip(*decorator_counts.most_common())
            sns.barplot(x=list(counts), y=list(decorators))
            plt.title("Most Common Decorators")
            plt.xlabel("Count")
            plt.tight_layout()
            plt.savefig(self.viz_dir / "decorator_usage.png")
            plt.close()

    def _generate_module_centrality(self):
        """Generate module centrality visualization"""
        if len(self.analyzer.module_graph) > 0:
            centrality_measures = {
                "In-Degree": nx.in_degree_centrality(self.analyzer.module_graph),
                "Out-Degree": nx.out_degree_centrality(self.analyzer.module_graph),
                "Betweenness": nx.betweenness_centrality(self.analyzer.module_graph),
            }

            data = []
            for measure, values in centrality_measures.items():
                for module, score in values.items():
                    data.append({"Module": module, "Measure": measure, "Score": score})

            df = pd.DataFrame(data)
            plt.figure(figsize=(15, 6))
            sns.barplot(data=df, x="Module", y="Score", hue="Measure")
            plt.xticks(rotation=45, ha="right")
            plt.title("Module Centrality Measures")
            plt.tight_layout()
            plt.savefig(self.viz_dir / "module_centrality.png")
            plt.close()

    def _generate_test_visualizations(self):
        """Generate test-related visualizations"""
        self._generate_test_coverage_matrix()
        self._generate_test_dependency_network()
        self._generate_test_complexity_distribution()
        self._generate_test_evolution()
        self._generate_test_similarity_network()

    def _generate_test_coverage_matrix(self):
        """Generate test coverage matrix visualization"""
        test_coverage = defaultdict(lambda: defaultdict(int))
        for node in self.analyzer.nodes.values():
            if "test" in node.name.lower():
                for edge in self.analyzer.call_graph.out_edges(node.full_name):
                    target = self.analyzer.nodes.get(edge[1])
                    if target and not "test" in target.name.lower():
                        test_coverage[node.module][target.module] += 1

        if test_coverage:
            coverage_df = pd.DataFrame(test_coverage).fillna(0)
            plt.figure(figsize=(15, 10))
            sns.heatmap(coverage_df, annot=True, fmt="g", cmap="YlOrRd")
            plt.title("Test Coverage Matrix: Test Modules vs Tested Modules")
            plt.xlabel("Test Modules")
            plt.ylabel("Tested Modules")
            plt.xticks(rotation=45, ha="right")
            plt.yticks(rotation=0)
            plt.tight_layout()
            plt.savefig(self.viz_dir / "test_coverage_matrix.png")
            plt.close()

    def _generate_test_dependency_network(self):
        """Generate test dependency network visualization"""
        test_dependencies = defaultdict(set)
        for node in self.analyzer.nodes.values():
            if "test" in node.name.lower():
                for edge in self.analyzer.call_graph.out_edges(node.full_name):
                    target = self.analyzer.nodes.get(edge[1])
                    if target and "test" in target.name.lower():
                        test_dependencies[node.name].add(target.name)

        if test_dependencies:
            G = nx.DiGraph(test_dependencies)
            plt.figure(figsize=(15, 10))
            pos = nx.spring_layout(G)
            nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=2000, font_size=8, arrows=True)
            plt.title("Test Dependency Network")
            plt.savefig(self.viz_dir / "test_dependencies.png", bbox_inches="tight")
            plt.close()

    def _generate_test_complexity_distribution(self):
        """Generate test complexity distribution visualization"""
        test_metrics = []
        for node in self.analyzer.nodes.values():
            if "test" in node.name.lower():
                metrics = {
                    "name": node.name,
                    "parameters": len(node.parameters),
                    "out_degree": self.analyzer.call_graph.out_degree(node.full_name),
                    "docstring_length": len(node.docstring or ""),
                    "decorators": len(node.decorators),
                }
                test_metrics.append(metrics)

        if test_metrics:
            df = pd.DataFrame(test_metrics)
            plt.figure(figsize=(15, 8))
            df_melted = df.melt(
                id_vars=["name"], value_vars=["parameters", "out_degree", "docstring_length", "decorators"]
            )
            sns.boxplot(data=df_melted, x="variable", y="value")
            plt.title("Test Complexity Metrics Distribution")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(self.viz_dir / "test_complexity_distribution.png")
            plt.close()

    def _generate_test_evolution(self):
        """Generate test evolution visualization"""
        module_test_evolution = defaultdict(list)
        for node in sorted(self.analyzer.nodes.values(), key=lambda x: x.line_number):
            if "test" in node.name.lower():
                module_test_evolution[node.module].append(node.line_number)

        if module_test_evolution:
            plt.figure(figsize=(15, 8))
            for module, line_numbers in module_test_evolution.items():
                plt.plot(range(len(line_numbers)), line_numbers, label=module, marker="o")
            plt.title("Test Distribution Across Module Lines")
            plt.xlabel("Test Sequence")
            plt.ylabel("Line Number in Module")
            plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
            plt.tight_layout()
            plt.savefig(self.viz_dir / "test_evolution.png")
            plt.close()

    def _generate_test_similarity_network(self):
        """Generate test similarity network visualization"""
        test_nodes = [node for node in self.analyzer.nodes.values() if "test" in node.name.lower()]
        similarity_graph = nx.Graph()

        for i, node1 in enumerate(test_nodes):
            for node2 in test_nodes[i + 1 :]:
                similarity = self._calculate_test_similarity(node1, node2)
                if similarity > 0.5:  # Only show strong similarities
                    similarity_graph.add_edge(node1.name, node2.name, weight=similarity)

        if similarity_graph.number_of_edges() > 0:
            plt.figure(figsize=(15, 15))
            pos = nx.spring_layout(similarity_graph)
            edges = similarity_graph.edges()
            weights = [similarity_graph[u][v]["weight"] * 2 for u, v in edges]

            nx.draw(
                similarity_graph,
                pos,
                with_labels=True,
                node_color="lightgreen",
                node_size=1000,
                font_size=8,
                width=weights,
                edge_color="gray",
                alpha=0.7,
            )
            plt.title("Test Similarity Network")
            plt.savefig(self.viz_dir / "test_similarity_network.png", bbox_inches="tight")
            plt.close()

    def _calculate_test_similarity(self, node1, node2) -> float:
        """Calculate similarity between two test nodes"""
        score = 0
        if set(node1.parameters) & set(node2.parameters):
            score += 0.3
        if set(node1.decorators) & set(node2.decorators):
            score += 0.3
        if node1.type == node2.type:
            score += 0.4
        return score

    def _get_simplified_call_graph(self) -> nx.DiGraph:
        """Create a simplified version of the call graph for visualization"""
        sorted_nodes = sorted(
            self.analyzer.call_graph.nodes(), key=lambda x: self.analyzer.call_graph.degree(x), reverse=True
        )[:50]
        return self.analyzer.call_graph.subgraph(sorted_nodes)
