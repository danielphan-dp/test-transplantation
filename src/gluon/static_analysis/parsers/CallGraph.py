import ast
import os
import networkx as nx
from typing import Dict, Set, Optional, List, Tuple, Any, Union
from concurrent.futures import ThreadPoolExecutor
import logging
from dataclasses import dataclass
from collections import Counter, defaultdict
import git
import json
from pathlib import Path
import sys
import warnings
from typing import Iterator


@dataclass
class RepoInfo:
    """Repository information"""

    name: str
    root_path: Path
    main_package: Optional[str] = None
    is_package: bool = False


@dataclass
class CallNode:
    """Represents a callable node (function/method) in the call graph"""

    name: str
    module: str
    class_name: Optional[str]
    line_number: int
    type: str  # 'function', 'method', 'class_method', 'static_method'
    decorators: List[str]
    docstring: Optional[str]
    parameters: List[str]
    is_external: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "module": self.module,
            "class_name": self.class_name,
            "line_number": self.line_number,
            "type": self.type,
            "decorators": self.decorators,
            "docstring": self.docstring,
            "parameters": self.parameters,
            "is_external": self.is_external,
        }

    @property
    def full_name(self) -> str:
        """Generate a unique identifier for the node"""
        parts = [self.module]
        if self.class_name:
            parts.append(self.class_name)
        parts.append(self.name)
        return "::".join(parts)


class CallGraphVisitor(ast.NodeVisitor):
    """AST visitor for building the call graph"""

    def __init__(self, builder: "CallGraphBuilder"):
        self.builder = builder
        self.current_class: Optional[str] = None
        self.current_function: Optional[str] = None
        self.imports: Dict[str, str] = {}

    def visit_ClassDef(self, node: ast.ClassDef):
        """Process class definitions"""
        previous_class = self.current_class
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = previous_class

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Process function definitions"""
        self._process_function_def(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        """Process async function definitions"""
        self._process_function_def(node, is_async=True)

    def _process_function_def(self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef], is_async: bool = False):
        """Process function/method definition"""
        func_id = self._get_function_id(node.name)
        func_type = self._get_function_type(node)
        parameters = [arg.arg for arg in node.args.args]

        # Create node
        self.builder.nodes[func_id] = CallNode(
            name=node.name,
            module=self.builder.module,
            class_name=self.current_class,
            line_number=node.lineno,
            type=func_type,
            decorators=[self._get_decorator_name(d) for d in node.decorator_list],
            docstring=ast.get_docstring(node),
            parameters=parameters,
        )

        # Process function body
        previous_function = self.current_function
        self.current_function = func_id
        self.generic_visit(node)
        self.current_function = previous_function

    def visit_Call(self, node: ast.Call):
        """Process function calls"""
        if self.current_function is None:
            return self.generic_visit(node)

        called_func_id = self._get_call_target(node)
        if called_func_id:
            self.builder.edges.append((self.current_function, called_func_id))
            if "::" not in called_func_id:  # External dependency
                self.builder.external_deps.add(called_func_id)

        self.generic_visit(node)

    def _get_function_id(self, func_name: str) -> str:
        """Generate unique identifier for a function"""
        if self.current_class:
            return f"{self.builder.module}::{self.current_class}::{func_name}"
        return f"{self.builder.module}::{func_name}"

    def _get_function_type(self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> str:
        """Determine the type of function"""
        if not self.current_class:
            return "function"

        decorators = {self._get_decorator_name(d) for d in node.decorator_list}
        if "@staticmethod" in decorators:
            return "static_method"
        elif "@classmethod" in decorators:
            return "class_method"
        return "method"

    def _get_decorator_name(self, node: ast.expr) -> str:
        """Extract decorator name from AST node"""
        if isinstance(node, ast.Name):
            return f"@{node.id}"
        elif isinstance(node, ast.Attribute):
            return f"@{self._get_attribute_name(node)}"
        elif isinstance(node, ast.Call):
            return f"@{self._get_call_name(node)}"
        return str(node)

    def _get_call_target(self, node: ast.Call) -> Optional[str]:
        """Determine the target of a function call"""
        if isinstance(node.func, ast.Name):
            return self._resolve_name(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            return self._resolve_attribute(node.func)
        return None

    def _resolve_name(self, name: str) -> str:
        """Resolve a simple name to its full path"""
        return self.imports.get(name, name)

    def _resolve_attribute(self, node: ast.Attribute) -> str:
        """Resolve an attribute access to its full path"""
        parts = []
        current = node
        while isinstance(current, ast.Attribute):
            parts.append(current.attr)
            current = current.value

        if isinstance(current, ast.Name):
            parts.append(current.id)
        else:
            return None

        return ".".join(reversed(parts))

    def _get_call_name(self, node: ast.Call) -> str:
        """Get the name of a call node"""
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            return self._get_attribute_name(node.func)
        return str(node.func)

    def _get_attribute_name(self, node: ast.Attribute) -> str:
        """Get the full name of an attribute node"""
        parts = []
        current = node
        while isinstance(current, ast.Attribute):
            parts.append(current.attr)
            current = current.value
        if isinstance(current, ast.Name):
            parts.append(current.id)
        return ".".join(reversed(parts))


class CallGraphBuilder:
    """Handles the AST visiting and graph building logic"""

    def __init__(self, file_path: Path, repo_root: Path):
        self.file_path = file_path
        self.repo_root = repo_root
        self.module = str(file_path.relative_to(repo_root))
        self.nodes: Dict[str, CallNode] = {}
        self.edges: List[Tuple[str, str]] = []
        self.external_deps: Set[str] = set()

    def process_file(self) -> Tuple[Dict[str, CallNode], List[Tuple[str, str]], Set[str]]:
        """Process a single file and return its nodes, edges, and external dependencies"""
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                content = f.read()

            visitor = CallGraphVisitor(self)
            tree = ast.parse(content)
            visitor.visit(tree)

            return self.nodes, self.edges, self.external_deps
        except Exception as e:
            logging.error(f"Error processing {self.file_path}: {str(e)}")
            return {}, [], set()


class RepoAnalyzer:
    """Main class for repository analysis"""

    def __init__(self, repo_path: str, output_dir: str = None, include_tests: bool = False):
        self.repo_path = Path(repo_path).resolve()
        self.output_dir = Path(output_dir) if output_dir else self.repo_path / "call_graph_analysis"
        self.repo_info = self._analyze_repo_structure()
        self.logger = self._setup_logger()
        self.call_graph = nx.DiGraph()
        self.module_graph = nx.DiGraph()
        self.nodes: Dict[str, CallNode] = {}
        self.external_deps: Set[str] = set()
        self.include_tests = include_tests

    def _setup_logger(self) -> logging.Logger:
        """Configure logging"""
        logger = logging.getLogger("RepoAnalyzer")
        logger.setLevel(logging.INFO)

        # Create handlers
        console_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(self.output_dir / "analysis.log")

        # Create formatters and add it to handlers
        log_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        console_handler.setFormatter(log_format)
        file_handler.setFormatter(log_format)

        # Add handlers to the logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        return logger

    def _analyze_repo_structure(self) -> RepoInfo:
        """Analyze repository structure to determine main package and type"""
        name = self.repo_path.name

        # Check if it's a Git repository
        try:
            repo = git.Repo(self.repo_path)
            name = repo.remotes.origin.url.split("/")[-1].replace(".git", "")
        except (git.InvalidGitRepositoryError, AttributeError):
            pass

        # Look for setup.py or pyproject.toml
        is_package = (self.repo_path / "setup.py").exists() or (self.repo_path / "pyproject.toml").exists()

        # Try to identify main package
        main_package = None
        potential_packages = [d for d in self.repo_path.iterdir() if d.is_dir() and (d / "__init__.py").exists()]

        if len(potential_packages) == 1:
            main_package = potential_packages[0].name

        return RepoInfo(name, self.repo_path, main_package, is_package)

    def _collect_python_files(self) -> List[Path]:
        """Collect all Python files in the repository"""
        python_files = []

        for path in self.repo_path.rglob("*.py"):
            # Skip virtual environments
            if any(part.startswith(".") or part in {"venv", "env"} for part in path.parts):
                continue

            # Skip test files unless specifically requested
            if not self.include_tests and "test" in path.name:
                continue

            python_files.append(path)

        return python_files

    def analyze(self):
        """Main analysis method"""
        self.logger.info(f"Starting analysis of repository: {self.repo_info.name}")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        python_files = self._collect_python_files()
        self.logger.info(f"Found {len(python_files)} Python files")

        self._process_files(python_files)
        self._build_module_graph()
        self._export_analysis()

    def _process_files(self, python_files: List[Path]):
        """Process Python files in parallel with better error handling"""
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(self._process_single_file, file_path): file_path for file_path in python_files}

            for future in futures:
                try:
                    file_path = futures[future]
                    nodes, edges, external = future.result()
                    self._update_graphs(nodes, edges, external)
                except Exception as e:
                    self.logger.error(f"Failed to process {futures[future]}: {str(e)}")

    def _process_single_file(self, file_path: Path) -> Tuple[Dict[str, CallNode], List[Tuple[str, str]], Set[str]]:
        """Process a single file with the CallGraphBuilder"""
        builder = CallGraphBuilder(file_path, self.repo_path)
        return builder.process_file()

    def _update_graphs(self, nodes: Dict[str, CallNode], edges: List[Tuple[str, str]], external_deps: Set[str]):
        """Update both call graph and module graph"""
        # Update nodes and call graph
        for node_id, node in nodes.items():
            self.nodes[node_id] = node
            self.call_graph.add_node(node_id, **node.to_dict())

        # Add edges to call graph
        for source, target in edges:
            if source in self.nodes:
                self.call_graph.add_edge(source, target)

        # Track external dependencies
        self.external_deps.update(external_deps)

    def _build_module_graph(self):
        """Build a simplified module dependency graph"""
        module_deps = defaultdict(set)

        for source, target in self.call_graph.edges():
            if source in self.nodes and target in self.nodes:
                source_module = self.nodes[source].module
                target_module = self.nodes[target].module
                if source_module != target_module:
                    module_deps[source_module].add(target_module)

        # Create module graph
        for source, targets in module_deps.items():
            for target in targets:
                self.module_graph.add_edge(source, target)

    def _export_analysis(self):
        """Export analysis results with better error handling"""
        try:
            self._export_metrics()
            self._export_graphs()
            self._export_visualizations()
        except Exception as e:
            self.logger.error(f"Error during export: {str(e)}")

    def _export_metrics(self):
        """Export various metrics about the codebase"""
        metrics = {
            "total_functions": len(self.nodes),
            "total_calls": self.call_graph.number_of_edges(),
            "external_dependencies": sorted(list(self.external_deps)),
            "modules": sorted(list(self.module_graph.nodes())),
            "module_dependencies": sorted(list(self.module_graph.edges())),
            "complexity_metrics": {
                "avg_incoming_calls": sum(d for _, d in self.call_graph.in_degree()) / max(len(self.nodes), 1),
                "avg_outgoing_calls": sum(d for _, d in self.call_graph.out_degree()) / max(len(self.nodes), 1),
                "max_incoming_calls": max((d for _, d in self.call_graph.in_degree()), default=0),
                "max_outgoing_calls": max((d for _, d in self.call_graph.out_degree()), default=0),
            },
        }

        metrics_file = self.output_dir / "metrics.json"
        with open(metrics_file, "w") as f:
            json.dump(metrics, f, indent=2)

    def _export_graphs(self):
        """Export graph data in various formats"""
        try:
            # Export call graph
            nx.write_gexf(self.call_graph, self.output_dir / "call_graph.gexf")

            # Export module graph
            nx.write_gexf(self.module_graph, self.output_dir / "module_graph.gexf")

            # Export as adjacency lists for easier processing
            with open(self.output_dir / "call_graph.txt", "w") as f:
                for source, target in self.call_graph.edges():
                    f.write(f"{source} -> {target}\n")

            with open(self.output_dir / "module_graph.txt", "w") as f:
                for source, target in self.module_graph.edges():
                    f.write(f"{source} -> {target}\n")
        except Exception as e:
            self.logger.error(f"Error exporting graphs: {str(e)}")

    def _export_visualizations(self):
        """Generate visualizations with proper error handling"""
        try:
            import matplotlib.pyplot as plt
            import seaborn as sns

            viz_dir = self.output_dir / "visualizations"
            viz_dir.mkdir(exist_ok=True)

            if len(self.module_graph) > 0:
                self._generate_module_visualization(viz_dir)
            if len(self.call_graph) > 0:
                self._generate_call_graph_visualization(viz_dir)
            self._generate_statistics_visualizations(viz_dir)

        except ImportError as e:
            self.logger.warning(f"Visualization packages not available: {str(e)}")
        except Exception as e:
            self.logger.error(f"Error generating visualizations: {str(e)}")

    def _generate_module_visualization(self, viz_dir: Path):
        """Generate module dependency visualization"""
        import matplotlib.pyplot as plt

        plt.figure(figsize=(15, 10))
        pos = nx.spring_layout(self.module_graph)
        nx.draw(
            self.module_graph, pos, with_labels=True, node_color="lightblue", node_size=2000, font_size=8, arrows=True
        )
        plt.title("Module Dependencies")
        plt.savefig(viz_dir / "module_dependencies.png", bbox_inches="tight")
        plt.close()

    def _generate_call_graph_visualization(self, viz_dir: Path):
        """Generate call graph visualization"""
        import matplotlib.pyplot as plt

        # Only visualize a subset of the call graph if it's too large
        if self.call_graph.number_of_nodes() > 100:
            self.logger.warning("Call graph too large, visualizing only top components")
            graph = self._get_simplified_call_graph()
        else:
            graph = self.call_graph

        plt.figure(figsize=(20, 15))
        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, with_labels=True, node_color="lightgreen", node_size=1500, font_size=6, arrows=True)
        plt.title("Function Call Graph")
        plt.savefig(viz_dir / "call_graph.png", bbox_inches="tight")
        plt.close()

    def _generate_statistics_visualizations(self, viz_dir: Path):
        """Generate statistical visualizations"""
        import matplotlib.pyplot as plt
        import seaborn as sns
        import numpy as np
        import pandas as pd
        from collections import Counter, defaultdict

        # Degree distribution
        plt.figure(figsize=(10, 6))
        degrees = [d for _, d in self.call_graph.degree()]
        if degrees:  # Only create histogram if we have data
            plt.hist(degrees, bins=min(50, len(set(degrees))), alpha=0.75)
            plt.xlabel("Number of Connections")
            plt.ylabel("Frequency")
            plt.title("Function Connection Distribution")
            plt.savefig(viz_dir / "degree_distribution.png")
        plt.close()

        # Module complexity
        module_complexity = defaultdict(int)
        for node in self.nodes.values():
            module_complexity[node.module] += 1

        if module_complexity:  # Only create bar plot if we have data
            plt.figure(figsize=(12, 6))
            modules = list(module_complexity.keys())
            counts = list(module_complexity.values())
            plt.bar(range(len(modules)), counts)
            plt.xticks(range(len(modules)), modules, rotation=45, ha="right")
            plt.xlabel("Module")
            plt.ylabel("Number of Functions")
            plt.title("Module Complexity")
            plt.tight_layout()
            plt.savefig(viz_dir / "module_complexity.png")
        plt.close()

        # 1. Function Types Distribution (Pie Chart)
        plt.figure(figsize=(10, 8))
        type_counts = Counter(node.type for node in self.nodes.values())
        plt.pie(type_counts.values(), labels=type_counts.keys(), autopct="%1.1f%%")
        plt.title("Distribution of Function Types")
        plt.savefig(viz_dir / "function_types.png")
        plt.close()

        # 2. Module Dependencies Heatmap
        if len(self.module_graph) > 0:
            plt.figure(figsize=(12, 10))
            modules = sorted(self.module_graph.nodes())
            adj_matrix = nx.adjacency_matrix(self.module_graph, nodelist=modules).todense()
            sns.heatmap(adj_matrix, xticklabels=modules, yticklabels=modules, cmap="YlOrRd", square=True)
            plt.title("Module Dependencies Heatmap")
            plt.xticks(rotation=45, ha="right")
            plt.yticks(rotation=0)
            plt.tight_layout()
            plt.savefig(viz_dir / "module_dependencies_heatmap.png")
            plt.close()

        # 3. Function Complexity by Parameters
        plt.figure(figsize=(12, 6))
        param_counts = [len(node.parameters) for node in self.nodes.values()]
        sns.boxplot(x=param_counts)
        sns.stripplot(x=param_counts, color="red", alpha=0.3)
        plt.title("Distribution of Function Parameters")
        plt.xlabel("Number of Parameters")
        plt.savefig(viz_dir / "parameter_distribution.png")
        plt.close()

        # 4. Decorator Usage Analysis
        decorator_counts = Counter([decorator for node in self.nodes.values() for decorator in node.decorators])
        if decorator_counts:
            plt.figure(figsize=(12, 6))
            decorators, counts = zip(*decorator_counts.most_common())
            sns.barplot(x=list(counts), y=list(decorators))
            plt.title("Most Common Decorators")
            plt.xlabel("Count")
            plt.tight_layout()
            plt.savefig(viz_dir / "decorator_usage.png")
            plt.close()

        # 5. Module Dependency Network Centrality
        if len(self.module_graph) > 0:
            plt.figure(figsize=(12, 6))
            centrality_measures = {
                "In-Degree": nx.in_degree_centrality(self.module_graph),
                "Out-Degree": nx.out_degree_centrality(self.module_graph),
                "Betweenness": nx.betweenness_centrality(self.module_graph),
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
            plt.savefig(viz_dir / "module_centrality.png")
            plt.close()

        # 1. Test Coverage Heatmap
        test_coverage = defaultdict(lambda: defaultdict(int))
        for node in self.nodes.values():
            if "test" in node.name.lower():
                # Count which modules are being tested
                for edge in self.call_graph.out_edges(node.full_name):
                    target = self.nodes.get(edge[1])
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
            plt.savefig(viz_dir / "test_coverage_matrix.png")
            plt.close()

        # 2. Test Dependency Graph
        test_dependencies = defaultdict(set)
        for node in self.nodes.values():
            if "test" in node.name.lower():
                for edge in self.call_graph.out_edges(node.full_name):
                    target = self.nodes.get(edge[1])
                    if target and "test" in target.name.lower():
                        test_dependencies[node.name].add(target.name)

        if test_dependencies:
            G = nx.DiGraph(test_dependencies)
            plt.figure(figsize=(15, 10))
            pos = nx.spring_layout(G)
            nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=2000, font_size=8, arrows=True)
            plt.title("Test Dependency Network")
            plt.savefig(viz_dir / "test_dependencies.png", bbox_inches="tight")
            plt.close()

        # 3. Test Complexity Distribution
        test_metrics = []
        for node in self.nodes.values():
            if "test" in node.name.lower():
                metrics = {
                    "name": node.name,
                    "parameters": len(node.parameters),
                    "out_degree": self.call_graph.out_degree(node.full_name),
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
            plt.savefig(viz_dir / "test_complexity_distribution.png")
            plt.close()

        # 4. Module Test Coverage Evolution
        module_test_evolution = defaultdict(list)
        for node in sorted(self.nodes.values(), key=lambda x: x.line_number):
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
            plt.savefig(viz_dir / "test_evolution.png")
            plt.close()

        # 5. Test Similarity Network
        def calculate_similarity(node1, node2):
            """Calculate similarity between two test nodes"""
            score = 0
            if set(node1.parameters) & set(node2.parameters):
                score += 0.3
            if set(node1.decorators) & set(node2.decorators):
                score += 0.3
            if node1.type == node2.type:
                score += 0.4
            return score

        test_nodes = [node for node in self.nodes.values() if "test" in node.name.lower()]
        similarity_graph = nx.Graph()

        for i, node1 in enumerate(test_nodes):
            for node2 in test_nodes[i + 1 :]:
                similarity = calculate_similarity(node1, node2)
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
            plt.savefig(viz_dir / "test_similarity_network.png", bbox_inches="tight")
            plt.close()

    def _get_simplified_call_graph(self) -> nx.DiGraph:
        """Create a simplified version of the call graph for visualization"""
        # Get the most connected nodes
        sorted_nodes = sorted(self.call_graph.nodes(), key=lambda x: self.call_graph.degree(x), reverse=True)[
            :50
        ]  # Take top 50 nodes

        # Create subgraph
        return self.call_graph.subgraph(sorted_nodes)


def main():
    """Main entry point for the call graph analyzer"""
    if len(sys.argv) < 2:
        print("Usage: python call_graph.py <repository_path> [output_directory] [--include-tests]")
        sys.exit(1)

    repo_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    include_tests = "--include-tests" in sys.argv

    try:
        analyzer = RepoAnalyzer(repo_path, output_dir, include_tests)
        analyzer.analyze()
    except Exception as e:
        print(f"Error analyzing repository: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
