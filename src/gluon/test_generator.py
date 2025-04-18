import os
import json
import re
import argparse
import glob
from openai import OpenAI

from .prompt_generator import (
    generate_transplant_analysis_prompt,
    generate_additional_files_prompt,
    generate_test_creation_prompt
)

from .data_extractor import DataExtractor
from .config import DATA_REPO_PATH

class TestGenerator:
    def __init__(self, host_repo, output_dir="./__internal__/results"):
        """Initialize the TestGenerator with OpenAI API key and output directory"""
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        self.data_extractor = DataExtractor()
        self.host_repo = host_repo

        # Read host repo files from __internal__/repo_file_paths/{host_repo}.json
        with open(f"./__internal__/repo_file_paths/{host_repo}_code_file_paths.json", "r") as f:
            self.host_repo_files = json.load(f)
        # A dictionary of donor repo files
        self.donor_repo_files = {}

        self.conversation_history = []
    
    def call_openai_api(self, prompt, maintain_conversation_history=False):
        """
        Call OpenAI GPT-4o API with the given prompt
        
        Parameters:
        - prompt: The prompt to send to the API
        - maintain_history: Whether to maintain conversation history
        """
        try:
            # Prepare messages - either a new conversation or continuation
            if maintain_conversation_history and self.conversation_history:
                # Add the new user message to existing conversation
                messages = self.conversation_history + [{"role": "user", "content": prompt}]
            else:
                # Start a new conversation
                messages = [{"role": "user", "content": prompt}]
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.2,
                max_tokens=4000
            )

            # If maintaining history, update the conversation history
            if maintain_conversation_history:
                self.conversation_history = messages + [
                    {"role": "assistant", "content": response.choices[0].message.content}
                ]

            return response.choices[0].message.content
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return None
    
    def write_file(self, file_path, content):
        """Write content to a file"""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            return True
        except Exception as e:
            print(f"Error writing to file {file_path}: {e}")
            return False
    
    def parse_json_from_response(self, response):
        """Extract and parse JSON from API response"""
        if not response:
            return None
            
        try:
            # First, try to parse the entire response as JSON
            return json.loads(response)
        except json.JSONDecodeError:
            # If that fails, try to extract JSON using regex
            json_pattern = r'```json\s*([\s\S]*?)\s*```|```\s*([\s\S]*?)\s*```|({[\s\S]*})'
            matches = re.search(json_pattern, response, re.DOTALL)
            
            if matches:
                for group in matches.groups():
                    if group:
                        try:
                            return json.loads(group.strip())
                        except json.JSONDecodeError:
                            continue
            
            # If we still can't find valid JSON, look for { and } characters
            start = response.find('{')
            end = response.rfind('}') + 1
            
            if start >= 0 and end > start:
                try:
                    json_str = response[start:end]
                    return json.loads(json_str)
                except json.JSONDecodeError:
                    pass
            
            print(f"Failed to extract JSON from response: {response[:200]}...")
            return None
    
    def analyze_transplantation_potential(self, host_code_files, host_code, donor_code_files, donor_code, donor_test_file, donor_test, host_repo_files, donor_repo_files):
        """Analyze if test methods can be transplanted from donor to host"""
        self.conversation_history = []

        prompt = generate_transplant_analysis_prompt(
            host_code_files, host_code, 
            donor_code_files, donor_code, 
            donor_test_file, donor_test,
            host_repo_files, donor_repo_files
        )
        response = self.call_openai_api(prompt, maintain_conversation_history=True)
        
        # Check if response is just "None"
        if response and response.strip().lower() == "none":
            return None
        
        # Try to parse as JSON if not "None"
        result = self.parse_json_from_response(response)
        
        # If parsing failed but we have a response, it might be a simple string
        if not result and response:
            print(f"Warning: Failed to parse JSON response. Raw response: {response[:200]}...")
            return None
        
        return result
    
    def identify_additional_files(self, host_code_files, transplant_analysis_result, host_repo_files, donor_repo_files):
        """Identify additional files needed for test generation"""
        prompt = generate_additional_files_prompt(
            host_code_files, 
            json.dumps(transplant_analysis_result, indent=2),
            host_repo_files, donor_repo_files
        )
        response = self.call_openai_api(prompt, maintain_conversation_history=True)
        result = self.parse_json_from_response(response)
        
        if not result:
            # Create a default response if parsing failed
            result = {
                "host_files_needed": "None",
                "donor_files_needed": "None"
            }
        
        return result
    
    def fetch_additional_files(self, donor_repo, additional_files_info):
        """Fetch content of additional files identified as needed"""
        host_files = []
        donor_files = []
        
        if additional_files_info.get("host_files_needed") and additional_files_info["host_files_needed"] != "None":
            for file_info in additional_files_info["host_files_needed"]:
                file_path = file_info["file_path"]
                
                content = self.data_extractor.extract_code_file_by_path(f"{DATA_REPO_PATH}/{self.host_repo}", file_path)
                
                if content:
                    host_files.append({"file_path": file_path, "content": content})
                else:
                    print(f"Warning: Could not find host file {file_path}")
        
        if additional_files_info.get("donor_files_needed") and additional_files_info["donor_files_needed"] != "None":
            for file_info in additional_files_info["donor_files_needed"]:
                file_path = file_info["file_path"]
                
                content = self.data_extractor.extract_code_file_by_path(f"{DATA_REPO_PATH}/{donor_repo}", file_path)
                
                if content:
                    donor_files.append({"file_path": file_path, "content": content})
                else:
                    print(f"Warning: Could not find donor file {file_path}")
        
        return host_files, donor_files
    
    def generate_test_file(self, host_code_files, host_code, donor_code_files, donor_code, 
                          donor_test_file, donor_test, transplant_analysis_result,
                          additional_files_info, host_files, donor_files):
        """Generate the transplanted test file"""
        prompt = generate_test_creation_prompt(
            host_code_files, host_code,
            donor_code_files, donor_code,
            donor_test_file, donor_test,
            json.dumps(transplant_analysis_result, indent=2),
            json.dumps(additional_files_info, indent=2),
            host_files, donor_files
        )
        response = self.call_openai_api(prompt, maintain_conversation_history=False)
        
        # Extract code block if present
        code_pattern = r'```python\s*([\s\S]*?)\s*```|```\s*([\s\S]*?)\s*```'
        matches = re.search(code_pattern, response, re.DOTALL)
        
        if matches:
            for group in matches.groups():
                if group:
                    return group.strip()
        
        # If no code block, return the full response
        return response
    
    def process_retrieved_pairs(self, retrieved_pairs_file):
        """Process all retrieved pairs from the JSON file"""
        try:
            with open(retrieved_pairs_file, 'r', encoding='utf-8') as f:
                retrieved_pairs = json.load(f)
            
            results = {"relevant_pairs": []}
            
            for pair_idx, pair in enumerate(retrieved_pairs.get("relevant_pairs", [])):
                print(f"Processing pair {pair_idx + 1}/{len(retrieved_pairs.get('relevant_pairs', []))}")
                host_item = pair.get("host_item", {})
                similar_items = pair.get("similar_items", [])
                
                # Read host code file
                host_code = None
                host_code = self.data_extractor.extract_code_file(f"{DATA_REPO_PATH}/{self.host_repo}", host_item)
                host_code_files = host_item.get("code", "")
                
                if not host_code:
                    print(f"Error: Could not read host code file {host_code_files}")
                    continue
                
                host_output = {
                    "test": host_item.get("test", ""),
                    "code": host_code_files,
                }
                
                result_item = {
                    "host_item": host_output,
                    "similar_items": []
                }
                
                for item_idx, similar_item in enumerate(similar_items):
                    print(f"  Processing similar item {item_idx + 1}/{len(similar_items)}")
                    donor_framework = similar_item.get("framework", "")

                    if donor_framework not in self.donor_repo_files:
                        with open(f"./__internal__/repo_file_paths/{donor_framework}_code_file_paths.json", "r") as f:
                            self.donor_repo_files[donor_framework] = json.load(f)

                    # Try different path variations for donor files
                    donor_code = None
                    donor_test = None
                    donor_code_files = similar_item.get("code", "")
                    donor_test_file = similar_item.get("test", "")
                    code_similarity_score = similar_item.get("code_similarity_score", 0)

                    donor_code = self.data_extractor.extract_code_file(f"{DATA_REPO_PATH}/{donor_framework}", similar_item)
                    donor_test = self.data_extractor.extract_test_code(f"{DATA_REPO_PATH}/{donor_framework}", similar_item)
                    
                    if not donor_code or not donor_test:
                        print(f"Error: Could not read donor files")
                        continue
                    
                    # Step 1: Analyze transplantation potential
                    print("  Analyzing transplantation potential...")
                    transplant_analysis_result = self.analyze_transplantation_potential(
                        host_code_files, host_code,
                        donor_code_files, donor_code,
                        donor_test_file, donor_test, 
                        self.host_repo_files, self.donor_repo_files[donor_framework]
                    )
                    
                    if not transplant_analysis_result:
                        print(f"  Skipping donor {donor_framework}/{donor_test_file} as tests cannot be transplanted")
                        continue
                    
                    # Step 2: Identify and fetch additional files
                    print("  Identifying additional files needed...")
                    additional_files_info = self.identify_additional_files(
                        host_code_files, transplant_analysis_result,
                        self.host_repo_files, self.donor_repo_files[donor_framework]
                    )
                    
                    print("  Fetching additional files...")
                    host_files, donor_files = self.fetch_additional_files(
                        donor_framework, additional_files_info
                    )
                    
                    # Step 3: Generate test file
                    print("  Generating test file...")
                    generated_test = self.generate_test_file(
                        host_code_files, host_code,
                        donor_code_files, donor_code,
                        donor_test_file, donor_test,
                        transplant_analysis_result,
                        additional_files_info,
                        host_files, donor_files
                    )
                    
                    # Determine name for generated test file
                    host_repo_output_dir = os.path.join(self.output_dir, self.host_repo)
                    os.makedirs(host_repo_output_dir, exist_ok=True)
                    
                    donor_test_name = os.path.basename(donor_test_file).split(".")[0]
                    host_test_file = f"transplanted_{donor_test_name}_from_{donor_framework}.py"
                    # Handle if the file already exists
                    i = 1
                    while os.path.exists(os.path.join(host_repo_output_dir, host_test_file)):
                        host_test_file = f"transplanted_{donor_test_name}_from_{donor_framework}_v{i}.py"
                        i += 1
                    
                    # Write generated test to file
                    generated_test_path = os.path.join(host_repo_output_dir, host_test_file)
                    self.write_file(generated_test_path, generated_test)
                    print(f"  Test file generated: {generated_test_path}")
                    
                    # Add result to output
                    result_item["similar_items"].append({
                        "framework": donor_framework,
                        "test": donor_test_file,
                        "code": donor_code_files,
                        "code_similarity_score": code_similarity_score,
                        "transplant_analysis": transplant_analysis_result,
                        "additional_files_info": additional_files_info,
                        "generated_test": generated_test
                    })
                
                if result_item["similar_items"]:
                    results["relevant_pairs"].append(result_item)
            
            # Write results to JSON file
            output_path = os.path.join(self.output_dir, f"{self.host_repo}_transplanted_tests_results.json")
            self.write_file(output_path, json.dumps(results, indent=2))
            print(f"Results written to {output_path}")
            
            return results
        
        except Exception as e:
            print(f"Error processing retrieved pairs: {e}")
            import traceback
            traceback.print_exc()
            return None

def main():
    parser = argparse.ArgumentParser(description='Generate tests by transplanting from donor tests')
    parser.add_argument('--api_key', type=str, help='OpenAI API key')
    parser.add_argument('--retrieved_pairs', type=str, help='Path to retrieved pairs JSON file')
    parser.add_argument('--frameworks', nargs='+', help='Specific frameworks to process')
    parser.add_argument('--all', action='store_true', help='Process all retrieved pairs')
    parser.add_argument('--output_dir', type=str, default='./__internal__/results', help='Output directory')
    
    args = parser.parse_args()

    if not args.api_key:
        args.api_key = os.environ.get("OPENAI_API_KEY")
    
    if not os.environ.get("OPENAI_API_KEY"):
        print("Error: No OpenAI API key provided. Please set OPENAI_API_KEY environment variable or use --api-key")
        return

    if args.retrieved_pairs:
        host_repo = os.path.basename(args.retrieved_pairs).split("_")[0]
        generator = TestGenerator(host_repo, args.output_dir)
        generator.process_retrieved_pairs(args.retrieved_pairs)
    elif args.frameworks:
        for framework in args.frameworks:
            file = os.path.join("./__internal__/relevant_pairs", f"{framework}_code_retrieved_pairs.json")
            if os.path.exists(file):
                host_repo = framework
                generator = TestGenerator(host_repo, args.output_dir)
                generator.process_retrieved_pairs(file)
    elif args.all:
        processed_files = glob.glob("./__internal__/relevant_pairs/*_code_retrieved_pairs.json")
        for file in processed_files:
            host_repo = os.path.basename(file).split("_")[0]
            generator = TestGenerator(host_repo, args.output_dir)
            generator.process_retrieved_pairs(file)

if __name__ == "__main__":
    main()