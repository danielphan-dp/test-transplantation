from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class RepoInfo:
    """Repository information"""

    name: str
    root_path: Path
    main_package: Optional[str] = None
    is_package: bool = False
