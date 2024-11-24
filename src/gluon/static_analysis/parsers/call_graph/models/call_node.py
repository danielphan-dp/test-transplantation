from dataclasses import dataclass
from typing import Optional, List, Dict, Any


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
