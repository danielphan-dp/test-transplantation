import logging
import json
import git
import ast
import networkx as nx
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Dict, Set, List, Tuple
from collections import defaultdict

from ..models.repo_info import RepoInfo
from ..models.call_node import CallNode
from .visualization import VisualizationGenerator
from ..visitors.call_graph_visitor import CallGraphVisitor


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
        self.visualization = VisualizationGenerator(self)

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
        """Process Python files in parallel"""
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
        """Export analysis results"""
        try:
            self._export_metrics()
            self._export_graphs()
            self.visualization.generate_visualizations()
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
            # Create new graphs with only essential attributes
            call_graph = nx.DiGraph()
            module_graph = nx.DiGraph()

            # Copy nodes and edges with minimal attributes for call graph
            for node in self.call_graph.nodes():
                # Get only essential attributes and provide defaults
                attrs = self.call_graph.nodes[node]
                cleaned_attrs = {
                    "module": attrs.get("module", ""),
                    "name": attrs.get("name", ""),
                    "type": attrs.get("type", ""),
                }
                call_graph.add_node(node, **cleaned_attrs)

            # Copy edges
            call_graph.add_edges_from(self.call_graph.edges())

            # For module graph, just copy structure without attributes
            module_graph.add_nodes_from(self.module_graph.nodes())
            module_graph.add_edges_from(self.module_graph.edges())

            # Export call graph
            nx.write_gexf(call_graph, self.output_dir / "call_graph.gexf")

            # Export module graph
            nx.write_gexf(module_graph, self.output_dir / "module_graph.gexf")

            # Export as adjacency lists
            with open(self.output_dir / "call_graph.txt", "w") as f:
                for source, target in call_graph.edges():
                    f.write(f"{source} -> {target}\n")

            with open(self.output_dir / "module_graph.txt", "w") as f:
                for source, target in module_graph.edges():
                    f.write(f"{source} -> {target}\n")

        except Exception as e:
            self.logger.error(f"Error exporting graphs: {str(e)}")
