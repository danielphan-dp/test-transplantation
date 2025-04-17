import json
import os

def read_file_content(file_path):
    """Read file content, handling potential errors."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except Exception as e:
        return f"Error reading file: {str(e)}"


class DataExtractor:
    """Extract and process test data from JSON files"""
    @staticmethod
    def load_data(file_path):
        """Load data from a JSON file"""
        with open(file_path, "r") as f:
            return json.load(f)["aligned_tc"]
    
    @staticmethod
    def extract_test_code(repo_path, pair_data):
        """Extract test code from the pair data"""
        test_file = pair_data["test"]
        test_path = os.path.join(repo_path, test_file)
        return read_file_content(test_path)
    
    @staticmethod
    def extract_code_file(repo_path, pair_data):
        """Extract code file from the pair data"""
        code_files = pair_data["code"]
        if isinstance(code_files, list):
            # Multiple code files
            code_paths = [os.path.join(repo_path, cf.strip()) for cf in code_files]
            return [read_file_content(cp) for cp in code_paths]
        else:
            # Single code file
            code_path = os.path.join(repo_path, code_files.strip())
            return read_file_content(code_path)
        
    @staticmethod
    def extract_pair_summary(data):
        """Extract pair summary from the pair data"""
        pair_summaries = []
        for pair in data:
            pair_summaries.append(pair["pair_summary"])
        print(f"Extracted {len(pair_summaries)} pair summaries")
        return pair_summaries
    
    @staticmethod
    def extract_code_summary(data):
        """Extract code summary from the pair data"""
        code_summaries = []
        for pair in data:
            code_summaries.append(pair["code_summary"])
        print(f"Extracted {len(code_summaries)} code summaries")
        return code_summaries
    
    @staticmethod
    def extract_code_file_paths(repo_path, src_path):
        """Extract file paths from the repository"""
        file_paths = []
        src_path = os.path.join(repo_path, src_path)
        # Get all file paths in the src_path
        for root, dirs, files in os.walk(src_path):
            for file in files:
                file_paths.append(os.path.join(src_path, file))
        print(f"Extracted {len(file_paths)} file paths")
        return file_paths
    
