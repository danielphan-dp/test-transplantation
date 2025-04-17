import os
import json
from .config import DATA_REPO_PATH, REPOSITORIES
from .data_extractor import DataExtractor

class RepoParser:
    def __init__(self, framework, src_path):
        self.framework = framework
        self.repo_path = os.path.join(DATA_REPO_PATH, framework)
        self.data_extractor = DataExtractor()
        self.src_path = src_path
        self.output_dir = os.path.join("__internal__", "repo_file_paths")
        os.makedirs(self.output_dir, exist_ok=True)

    
    def output_repo_files(self):
        """
        Output all files in the repository to a json file
        """
        file_paths = self.data_extractor.extract_code_file_paths(self.repo_path, self.src_path)
        
        with open(f"{self.output_dir}/{self.framework}_code_file_paths.json", "w") as f:
            json.dump(file_paths, f)
        

if __name__ == "__main__":
    
    for framework, paths in REPOSITORIES.items():
        parser = RepoParser(framework, paths[0])
        parser.output_repo_files()