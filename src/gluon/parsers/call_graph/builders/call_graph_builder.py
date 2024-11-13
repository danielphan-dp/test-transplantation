from pathlib import Path
from typing import Dict, List, Set, Tuple
import ast
import logging
from dataclasses import dataclass
from ...CallGraph import CallNode, CallGraphVisitor


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
