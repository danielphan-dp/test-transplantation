import os
import json
import glob
from openai import OpenAI
import time

# Initialize the OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def read_file_content(file_path):
    """Read file content, handling potential errors."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except Exception as e:
        return f"Error reading file: {str(e)}"

def generate_pair_summary(test_content, code_contents, test_file, code_files, comments):
    """Generate a detailed summary of the test-code pair using GPT-4o.
    
    Parameters:
    - test_content: Content of the test file
    - code_contents: List of contents of code files or single content string
    - test_file: Path of the test file
    - code_files: List of paths of code files or single path string
    - comments: List of comments from maintainer
    """
    # Handle both single code file and multiple code files cases
    if isinstance(code_files, list):
        # Multiple code files
        code_files_str = ", ".join(code_files)
        code_blocks = []
        
        for i in range(len(code_contents)):
            file_content = code_contents[i]
            # Add the code block with the file name
            code_blocks.append(f"CODE FILE {i+1}: {code_files[i]}\n```python\n{file_content}\n```")
                
        code_section = "\n\n".join(code_blocks)
    else:
        # Single code file
        code_files_str = code_files
        code_section = f"CODE FILE: {code_files}\n```python\n{code_contents}\n```"

    # Construct the prompt optimized for embedding and similarity search
    prompt = f"""
You are an expert code analyzer tasked with explaining test-code pairs from a Python web framework project. Your summaries will be used in an embedding-based search system to find similar test-code relationships.

TEST FILE: {test_file}
```python
{test_content[:30000]}
```

{code_section}

COMMENTS FROM MAINTAINER: {', '.join(comments)}

Generate a semantically rich summary (400-600 words) optimized for embedding and similarity search that covers:

1. TECHNICAL SPECIFICS:
   - Specific classes, methods, and functions being tested (use exact names)
   - Framework components and their interactions
   - Design patterns implemented (e.g., Factory, Singleton, Observer)
   - Technical mechanisms (e.g., dependency injection, middleware processing)

2. TESTING APPROACH:
   - Testing methodologies used (unit, integration, mock objects, fixtures)
   - Edge cases and boundary conditions tested
   - Error handling and exception testing strategies

3. CODE ARCHITECTURE:
   - Component relationships and dependencies
   - Data flow patterns
   - Key abstractions and their implementations
   - API surface and public interfaces

4. DISTINCTIVE FEATURES:
   - Unusual or noteworthy implementation details
   - Performance considerations
   - Security-related testing
   - Framework-specific patterns

Make your summary technically precise with specific terminology that would distinguish this test-code pair from others. Include meaningful technical details that would create a distinctive semantic signature for embedding models. Avoid generic descriptions that could apply to many test-code pairs.

Format as a information-rich list of bullet points, without headings or sections. Use specific technical terms rather than general descriptions whenever possible.
"""

    # Make the API call with retry logic for rate limits
    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an expert code analyzer that provides technically precise, semantically rich summaries of test-code relationships in Python web frameworks. Your summaries should be optimized for embedding-based similarity search, focusing on specific technical details, distinctive implementation patterns, and precise terminology rather than general descriptions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0,  # Lower temperature for more consistent output
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            error_msg = str(e).lower()
            if "rate limit" in error_msg and attempt < max_retries - 1:
                wait_time = (2 ** attempt) * 5  # Exponential backoff: 5s, 10s, 20s, etc.
                print(f"    Rate limit hit. Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
                continue
            else:
                return f"Error generating summary: {str(e)}"

def generate_code_summary(code_content, code_file):
    """Generate a summary focused only on the code file, optimized for embedding and similarity search.
    
    Parameters:
    - code_content: Content of the code file or list of contents
    - code_file: Path of the code file or list of paths
    """
    # Handle both single code file and multiple code files cases
    if isinstance(code_file, list):
        # Multiple code files
        code_files_str = ", ".join(code_file)
        
        # Use the first code file for the summary or combine multiple if manageable
        if len(code_file) == 1:
            code_display = f"CODE FILE: {code_file[0]}\n```python\n{code_content[0]}\n```"
        else:
            # Include all files
            code_blocks = []
            for i in range(len(code_file)):
                code_blocks.append(f"CODE FILE {i+1}: {code_file[i]}\n```python\n{code_content[i]}\n```")
            code_display = "\n\n".join(code_blocks)
    else:
        # Single code file
        code_files_str = code_file
        code_display = f"CODE FILE: {code_file}\n```python\n{code_content}\n```"

    # Construct the prompt for code-only summary
    prompt = f"""
You are an expert code analyzer tasked with explaining Python code files from web frameworks. Your code summaries will be used in an embedding-based search system to find similar implementation patterns across frameworks.

{code_display}

Generate a technically precise, semantically rich summary (300-400 words) of this code, optimized for embedding-based similarity search. Focus on:

1. CORE FUNCTIONALITY:
   - Specific classes and methods implemented (use exact names)
   - Primary responsibilities and purpose of this module
   - Public APIs and interfaces exposed

2. IMPLEMENTATION DETAILS:
   - Algorithms and data structures used
   - Design patterns implemented (e.g., Factory, Singleton, Observer)
   - Core mechanisms (e.g., event handling, middleware, routing)

3. ARCHITECTURAL ROLE:
   - How this component fits into the larger framework
   - Dependencies on other components
   - What dependencies this component resolves
   - Initialization and lifecycle patterns

4. DISTINCTIVE CHARACTERISTICS:
   - Unique implementation approaches 
   - Performance optimizations
   - Security features
   - Error handling strategies
   - Framework-specific idioms

Make your summary technically precise with specific terminology that would distinguish this code from similar implementations in other frameworks. Include meaningful technical details that would create a distinctive semantic signature for embedding models.

Format as a information-rich list of bullet points, without headings or sections. Use specific technical terms rather than general descriptions. Focus on what makes this code distinctive for accurate similarity matching across frameworks.
"""

    # Make the API call with retry logic for rate limits
    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an expert code analyzer that provides technically precise, semantically rich summaries of Python web framework code. Your summaries should be optimized for embedding-based similarity search, focusing on specific implementation details, architectural patterns, and precise technical terminology to enable accurate cross-framework comparisons."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0,  # Lower temperature for more consistent output
                max_tokens=800
            )
            return response.choices[0].message.content
        except Exception as e:
            error_msg = str(e).lower()
            if "rate limit" in error_msg and attempt < max_retries - 1:
                wait_time = (2 ** attempt) * 5  # Exponential backoff: 5s, 10s, 20s, etc.
                print(f"    Rate limit hit. Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
                continue
            else:
                return f"Error generating code summary: {str(e)}"

def process_tcm_file(tcm_file_path):
    """Process a single TCM JSON file."""
    print(f"Processing {tcm_file_path}...")
    
    # Load the TCM JSON file
    with open(tcm_file_path, 'r') as f:
        tcm_data = json.load(f)
    
    # Extract the framework name from the file path (e.g., flask from flask_tcm.json)
    framework = os.path.basename(tcm_file_path).split('_')[0]
    repo_path = f"./__internal__/data_repo/{framework}"
    
    # Process each test-code pair
    total_pairs = len(tcm_data["aligned_tc"])
    for idx, pair in enumerate(tcm_data["aligned_tc"]):
        test_file = pair["test"]
        code_file = pair["code"].strip() if isinstance(pair["code"], str) else [cf.strip() for cf in pair["code"]]
        comments = pair.get("comments", [])
        
        # Check if summaries already exist
        has_pair_summary = "pair_summary" in pair and pair["pair_summary"] and not pair["pair_summary"].startswith("Error")
        has_code_summary = "code_summary" in pair and pair["code_summary"] and not pair["code_summary"].startswith("Error")
        
        # For backward compatibility, check for "summary" field and rename it to "pair_summary" if needed
        if "summary" in pair and pair["summary"] and not pair["summary"].startswith("Error"):
            if not has_pair_summary:
                pair["pair_summary"] = pair["summary"]
                has_pair_summary = True
            # Keep the original summary field as well for backward compatibility
        
        if has_pair_summary and has_code_summary:
            if isinstance(code_file, list):
                code_file_display = f"[{len(code_file)} files]"
            else:
                code_file_display = code_file
            print(f"  [{idx+1}/{total_pairs}] Skipping (summaries exist): {test_file} -> {code_file_display}")
            continue
        
        if isinstance(code_file, list):
            code_file_display = f"[{len(code_file)} files]"
        else:
            code_file_display = code_file
        print(f"  [{idx+1}/{total_pairs}] Analyzing: {test_file} -> {code_file_display}")
        
        # Construct file paths and read content
        test_path = os.path.join(repo_path, test_file)
        
        # Check if test file exists
        if not os.path.exists(test_path):
            error_msg = f"Error: Test file not found: {test_path}"
            print(f"    {error_msg}")
            if not has_pair_summary:
                pair["pair_summary"] = error_msg
            if not has_code_summary:
                pair["code_summary"] = error_msg
            continue
            
        # Read test file content
        test_content = read_file_content(test_path)
        
        # Handle single code file or multiple code files
        if isinstance(code_file, list):
            # Multiple code files
            code_paths = [os.path.join(repo_path, cf) for cf in code_file]
            code_exists = [os.path.exists(cp) for cp in code_paths]
            
            if not all(code_exists):
                missing_files = [cf for cf, exists in zip(code_file, code_exists) if not exists]
                error_msg = f"Error: Some code files not found: {', '.join(missing_files)}"
                print(f"    {error_msg}")
                if not has_pair_summary:
                    pair["pair_summary"] = error_msg
                if not has_code_summary:
                    pair["code_summary"] = error_msg
                continue
            
            # Read content of all code files
            code_contents = [read_file_content(cp) for cp in code_paths]
        else:
            # Single code file
            code_path = os.path.join(repo_path, code_file)
            if not os.path.exists(code_path):
                error_msg = f"Error: Code file not found: {code_path}"
                print(f"    {error_msg}")
                if not has_pair_summary:
                    pair["pair_summary"] = error_msg
                if not has_code_summary:
                    pair["code_summary"] = error_msg
                continue
            
            code_contents = read_file_content(code_path)
        
        # Generate pair summary if needed
        if not has_pair_summary:
            print(f"    Generating pair summary...")
            pair_summary = generate_pair_summary(test_content, code_contents, test_file, code_file, comments)
            pair["pair_summary"] = pair_summary
        
        # Generate code summary if needed
        if not has_code_summary:
            print(f"    Generating code summary...")
            code_summary = generate_code_summary(code_contents, code_file)
            pair["code_summary"] = code_summary
        
        # Save progress after each analysis
        if not os.path.exists("./__internal__/tc_sets_summary"):
            os.makedirs("./__internal__/tc_sets_summary")
        progress_file = os.path.join("./__internal__/tc_sets_summary", f"{framework}_tcm_with_summaries.json")
        with open(progress_file, 'w') as f:
            json.dump(tcm_data, f, indent=2)
            
        print(f"    Summaries generated and progress saved.")
        
        # Sleep to avoid API rate limits
        time.sleep(2)
    
    # Save the updated TCM file
    output_path = os.path.join("./__internal__/tc_sets_summary", f"{framework}_tcm_with_summaries.json")
    with open(output_path, 'w') as f:
        json.dump(tcm_data, f, indent=2)
    
    print(f"  Saved updated file to {output_path}")
    return output_path

def main():
    import argparse
    import sys
    
    # Create the main parser
    parser = argparse.ArgumentParser(description='Tools for test-code mapping analysis')

    parser.add_argument('--files', nargs='+', help='Specific TCM files to process (e.g., flask_tcm.json)')
    parser.add_argument('--all', action='store_true', help='Process all TCM files in ./__internal__/tc_sets')
    parser.add_argument('--frameworks', nargs='+', help='Specific frameworks to process (e.g., flask sanic)')
    parser.add_argument('--api-key', help='OpenAI API key (or set OPENAI_API_KEY environment variable)')
    parser.add_argument('--pair-only', action='store_true', help='Generate only pair summaries')
    parser.add_argument('--code-only', action='store_true', help='Generate only code summaries')
    
    args = parser.parse_args()

    
    # Set API key if provided
    if args.api_key:
        os.environ["OPENAI_API_KEY"] = args.api_key

    # Check for API key
    if not os.environ.get("OPENAI_API_KEY"):
        print("Error: No OpenAI API key provided. Please set OPENAI_API_KEY environment variable or use --api-key")
        return

    # Determine which files to process
    tcm_files = []

    if args.files:
        # Process specific files
        tcm_files = [os.path.join("./__internal__/tc_sets", f) for f in args.files]
        tcm_files = [f for f in tcm_files if os.path.exists(f)]
        missing = [f for f in args.files if not os.path.exists(os.path.join("./__internal__/tc_sets", f))]
        if missing:
            print(f"Warning: These files were not found: {', '.join(missing)}")
    elif args.frameworks:
        # Process specific frameworks
        for framework in args.frameworks:
            file = os.path.join("./__internal__/tc_sets", f"{framework}_tcm.json")
            if os.path.exists(file):
                tcm_files.append(file)
            else:
                print(f"Warning: File not found for framework '{framework}': {file}")
    elif args.all or not (args.files or args.frameworks):
        # Process all files or default behavior
        tcm_files = glob.glob("./__internal__/tc_sets/*_tcm.json")

    if not tcm_files:
        print("No TCM JSON files found to process.")
        return

    print(f"Will process {len(tcm_files)} files: {', '.join(tcm_files)}")

    processed_files = []
    for tcm_file in tcm_files:
        processed_file = process_tcm_file(tcm_file)
        processed_files.append(processed_file)

    print("\nProcessing complete. Files generated:")
    for file in processed_files:
        print(f"- {file}")

if __name__ == "__main__":
    main()