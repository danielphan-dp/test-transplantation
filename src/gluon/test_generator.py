import os
import json
import re
import argparse
from openai import OpenAI

from prompt_generator import (
    generate_transplant_analysis_prompt,
    generate_additional_files_prompt,
    generate_test_creation_prompt
)

class TestGenerator:
    def __init__(self, output_dir="./__internal__/results"):
        """Initialize the TestGenerator with OpenAI API key and output directory"""
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def call_openai_api(self, prompt):
        """Call OpenAI GPT-4o API with the given prompt"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=4000
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return None
    
    def read_file(self, file_path):
        """Read content from a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
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
    
    def analyze_transplantation_potential(self, host_code_file, host_code, donor_code_file, donor_code, donor_test_file, donor_test):
        """Analyze if test methods can be transplanted from donor to host"""
        prompt = generate_transplant_analysis_prompt(
            host_code_file, host_code, 
            donor_code_file, donor_code, 
            donor_test_file, donor_test
        )
        response = self.call_openai_api(prompt)
        
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
    
    def identify_additional_files(self, host_code_file, transplant_analysis_result):
        """Identify additional files needed for test generation"""
        prompt = generate_additional_files_prompt(
            host_code_file, 
            json.dumps(transplant_analysis_result, indent=2)
        )
        response = self.call_openai_api(prompt)
        result = self.parse_json_from_response(response)
        
        if not result:
            # Create a default response if parsing failed
            result = {
                "host_files_needed": "None",
                "donor_files_needed": "None"
            }
        
        return result
    
    def fetch_additional_files(self, host_repo, donor_repo, additional_files_info, base_path="./"):
        """Fetch content of additional files identified as needed"""
        host_files = []
        donor_files = []
        
        if additional_files_info.get("host_files_needed") and additional_files_info["host_files_needed"] != "None":
            for file_info in additional_files_info["host_files_needed"]:
                file_path = file_info["file_path"]
                # Try different path variations to find the file
                possible_paths = [
                    f"{base_path}{file_path}",
                    f"{base_path}{host_repo}/{file_path}",
                    f"{base_path}/repositories/{host_repo}/{file_path}"
                ]
                
                content = None
                for path in possible_paths:
                    content = self.read_file(path)
                    if content:
                        break
                
                if content:
                    host_files.append({"file_path": file_path, "content": content})
                else:
                    print(f"Warning: Could not find host file {file_path}")
        
        if additional_files_info.get("donor_files_needed") and additional_files_info["donor_files_needed"] != "None":
            for file_info in additional_files_info["donor_files_needed"]:
                file_path = file_info["file_path"]
                possible_paths = [
                    f"{base_path}{file_path}",
                    f"{base_path}{donor_repo}/{file_path}",
                    f"{base_path}/repositories/{donor_repo}/{file_path}"
                ]
                
                content = None
                for path in possible_paths:
                    content = self.read_file(path)
                    if content:
                        break
                
                if content:
                    donor_files.append({"file_path": file_path, "content": content})
                else:
                    print(f"Warning: Could not find donor file {file_path}")
        
        return host_files, donor_files
    
    def generate_test_file(self, host_code_file, host_code, donor_code_file, donor_code, 
                          donor_test_file, donor_test, transplant_analysis_result,
                          additional_files_info, host_files, donor_files):
        """Generate the transplanted test file"""
        prompt = generate_test_creation_prompt(
            host_code_file, host_code,
            donor_code_file, donor_code,
            donor_test_file, donor_test,
            json.dumps(transplant_analysis_result, indent=2),
            json.dumps(additional_files_info, indent=2),
            host_files, donor_files
        )
        response = self.call_openai_api(prompt)
        
        # Extract code block if present
        code_pattern = r'```python\s*([\s\S]*?)\s*```|```\s*([\s\S]*?)\s*```'
        matches = re.search(code_pattern, response, re.DOTALL)
        
        if matches:
            for group in matches.groups():
                if group:
                    return group.strip()
        
        # If no code block, return the full response
        return response
    
    def process_retrieved_pairs(self, retrieved_pairs_file, base_path="./"):
        """Process all retrieved pairs from the JSON file"""
        try:
            with open(retrieved_pairs_file, 'r', encoding='utf-8') as f:
                retrieved_pairs = json.load(f)
            
            results = {"relevant_pairs": []}
            
            for pair_idx, pair in enumerate(retrieved_pairs.get("relevant_pairs", [])):
                print(f"Processing pair {pair_idx + 1}/{len(retrieved_pairs.get('relevant_pairs', []))}")
                host_item = pair.get("host_item", {})
                similar_items = pair.get("similar_items", [])
                
                host_code_file = host_item.get("code", "").strip()
                
                # Make sure the path doesn't have leading spaces
                if host_code_file.startswith(" "):
                    host_code_file = host_code_file[1:]
                
                # Try different path variations to find the host code file
                host_code = None
                for path_variant in [
                    f"{base_path}{host_code_file}",
                    f"{base_path}flask/{host_code_file}",
                    f"{base_path}/repositories/flask/{host_code_file}"
                ]:
                    host_code = self.read_file(path_variant)
                    if host_code:
                        break
                
                if not host_code:
                    print(f"Error: Could not read host code file {host_code_file}")
                    continue
                
                host_output = {
                    "test": host_item.get("test", ""),
                    "code": host_code_file,
                }
                
                result_item = {
                    "host_item": host_output,
                    "similar_items": []
                }
                
                for item_idx, similar_item in enumerate(similar_items):
                    print(f"  Processing similar item {item_idx + 1}/{len(similar_items)}")
                    donor_code_file = similar_item.get("code", "").strip()
                    donor_test_file = similar_item.get("test", "").strip()
                    donor_framework = similar_item.get("framework", "")
                    
                    if not donor_code_file or not donor_test_file or not donor_framework:
                        continue
                    
                    # Try different path variations for donor files
                    donor_code = None
                    donor_test = None
                    
                    for path_variant in [
                        f"{base_path}{donor_code_file}",
                        f"{base_path}{donor_framework}/{donor_code_file}",
                        f"{base_path}/repositories/{donor_framework}/{donor_code_file}"
                    ]:
                        donor_code = self.read_file(path_variant)
                        if donor_code:
                            break
                    
                    for path_variant in [
                        f"{base_path}{donor_test_file}",
                        f"{base_path}{donor_framework}/{donor_test_file}",
                        f"{base_path}/repositories/{donor_framework}/{donor_test_file}"
                    ]:
                        donor_test = self.read_file(path_variant)
                        if donor_test:
                            break
                    
                    if not donor_code or not donor_test:
                        print(f"Error: Could not read donor files: {donor_code_file} or {donor_test_file}")
                        continue
                    
                    # Step 1: Analyze transplantation potential
                    print("  Analyzing transplantation potential...")
                    transplant_analysis_result = self.analyze_transplantation_potential(
                        host_code_file, host_code,
                        donor_code_file, donor_code,
                        donor_test_file, donor_test
                    )
                    
                    if not transplant_analysis_result:
                        print(f"  Skipping donor {donor_framework}/{donor_code_file} as tests cannot be transplanted")
                        continue
                    
                    # Step 2: Identify and fetch additional files
                    print("  Identifying additional files needed...")
                    additional_files_info = self.identify_additional_files(
                        host_code_file, transplant_analysis_result
                    )
                    
                    print("  Fetching additional files...")
                    host_files, donor_files = self.fetch_additional_files(
                        "flask", donor_framework, additional_files_info, base_path
                    )
                    
                    # Step 3: Generate test file
                    print("  Generating test file...")
                    generated_test = self.generate_test_file(
                        host_code_file, host_code,
                        donor_code_file, donor_code,
                        donor_test_file, donor_test,
                        transplant_analysis_result,
                        additional_files_info,
                        host_files, donor_files
                    )
                    
                    # Determine name for generated test file
                    host_repo_output_dir = os.path.join(self.output_dir, "flask")
                    os.makedirs(host_repo_output_dir, exist_ok=True)
                    
                    host_test_file = host_item.get("test", "")
                    if not host_test_file:
                        # Create a name based on host code file
                        file_base = os.path.basename(host_code_file)
                        file_name = os.path.splitext(file_base)[0]
                        host_test_file = f"test_transplanted_{file_name}_{donor_framework}.py"
                    else:
                        # If the host already has a test file, create a new name to avoid conflicts
                        file_name = os.path.splitext(os.path.basename(host_test_file))[0]
                        host_test_file = f"{file_name}_transplanted_{donor_framework}.py"
                    
                    # Write generated test to file
                    generated_test_path = os.path.join(host_repo_output_dir, host_test_file)
                    self.write_file(generated_test_path, generated_test)
                    print(f"  Test file generated: {generated_test_path}")
                    
                    # Add result to output
                    result_item["similar_items"].append({
                        "test": donor_test_file,
                        "code": donor_code_file,
                        "framework": donor_framework,
                        "transplant_analysis": transplant_analysis_result,
                        "additional_files_info": additional_files_info,
                        "generated_test": generated_test_path
                    })
                
                if result_item["similar_items"]:
                    results["relevant_pairs"].append(result_item)
            
            # Write results to JSON file
            output_path = os.path.join(self.output_dir, "transplanted_tests_results.json")
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
    parser.add_argument('--retrieved_pairs', type=str, required=True, help='Path to retrieved pairs JSON file')
    parser.add_argument('--output_dir', type=str, default='./__internal__/results', help='Output directory')
    parser.add_argument('--base_path', type=str, default='./', help='Base path for file resolution')
    
    args = parser.parse_args()

    if not args.api_key:
        args.api_key = os.environ.get("OPENAI_API_KEY")
    
    if not os.environ.get("OPENAI_API_KEY"):
        print("Error: No OpenAI API key provided. Please set OPENAI_API_KEY environment variable or use --api-key")
        return
    
    generator = TestGenerator(args.output_dir)
    generator.process_retrieved_pairs(args.retrieved_pairs, args.base_path)

if __name__ == "__main__":
    main()