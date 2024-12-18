import os
os.environ["OPENAI_API_KEY"] = "sk-<API_KEY>"

import json
from pathlib import Path
from typing import Dict
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import DirectoryLoader, PythonLoader
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class CodebaseIndexer:
    """Index and manage source code repositories using FAISS"""
    def __init__(self, embedding_model_name="sentence-transformers/all-mpnet-base-v2"):
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)
        self.db_cache: Dict[str, FAISS] = {}
        
    def index_repository(self, repo_name: str, load_tests: bool = False) -> FAISS:
        """Index a source code repository and return vectorstore
        
        Args:
            repo_path: Path to the repository
            load_tests: If True, load only test files, otherwise load non-test files
        Returns:
            FAISS vector store containing the indexed documents
        """
        # Check cache key with load_tests parameter
        repo_path = f"./__internal__/data_repo/{repo_name}"
        cache_key = f"{repo_path}_{load_tests}"
        if cache_key in self.db_cache:
            return self.db_cache[cache_key]
        
        # Set glob pattern based on load_tests flag
        if load_tests:
            # Load only Python files inside tests directory
            glob_pattern = "**/tests/**/*.py"
        else:
            # Load Python files excluding tests directory
            glob_pattern = "**/*.py"
            
        loader = DirectoryLoader(
            repo_path,
            glob=glob_pattern,
            show_progress=True,
            loader_cls=PythonLoader,
            exclude=["**/tests/**"] if not load_tests else None
        )
        documents = loader.load()
        
        python_splitter = RecursiveCharacterTextSplitter.from_language(
            language=Language.PYTHON,
            chunk_size=2000,
            chunk_overlap=200
        )
        texts = python_splitter.split_documents(documents)
        
        db = FAISS.from_documents(
            texts,
            self.embeddings,
        )
        
        # Cache with the combined key
        self.db_cache[cache_key] = db
        return db

class UnitTestsGenerator:
    """Generate unit tests from source code using LLM and multiple retrievers"""
    
    def __init__(self, model_name="gpt-4o-mini", temperature=0):
        """Initialize the test generator with specified LLM"""
        self.llm = ChatOpenAI(model_name=model_name, temperature=temperature)
        self.indexer = CodebaseIndexer()
        self.prompt = self._create_test_prompt_template()

    def _create_test_prompt_template(self) -> ChatPromptTemplate:
        template = """You are tasked with generating a Python unit test. Generate ONLY the Python code without any explanations or markdown formatting.

        This is a test generation task for the **host project method** using **similar tests** as references. The goal is to improve the coverage of the method under test while utilizing relevant information from the host project's test code.

        ---

        **Method to Test (from {repo_name}):**
        {method_under_test}

        **Existing Host Test Code:**
        {host_test_source_code}

        **Host Test Information:**
        1. Test Name: {host_test_name}
        2. Module: {host_test_module}
        3. Imports: {host_test_imports}
        4. Assertions: {host_test_assertions}
        5. Arguments: {host_test_arguments}
        6. Fixtures: {host_test_fixtures}
        7. Decorators: {host_test_decorators}
        8. Setup Method: {host_test_setup_method}
        9. Teardown Method: {host_test_teardown_method}

        ---

        **Reference Similar Test Information:**
        1. Source Code: {donor_tests}
        2. Test Name: {test_name}
        3. Required Imports: {imports}
        4. Test Decorators: {decorators}
        5. Test Arguments: {arguments}
        6. Assertions: {assertions}
        7. Setup Method: {setup_method}
        8. Teardown Method: {teardown_method}
        9. Mocks Used: {mocks}

        **Additional Context:**
        1. Similar Method Being Tested: {donor_method_under_test}
        2. Related Source Code from Codebase: {relevant_source}
        3. Related Test Examples: {relevant_tests}

        ---

        ### Requirements:
        1. **Leverage Host Test Information**: Use existing imports, structure, naming conventions, and argument/fixture usage from the host test where applicable.
        2. **Avoid Duplication**: If the host test already tests certain aspects, focus on covering edge cases or alternative scenarios for the method.
        3. **Incorporate Similar Test Insights**: If the similar tests have helpful assertions, mocking strategies, or edge-case handling, include them in the new test.
        4. **Increase Coverage**: Ensure the generated test improves test coverage by testing edge cases, negative cases, or underexplored aspects of the method.
        5. Include any **necessary imports**, **fixtures**, or **mocks** to make the test runnable.
        6. Generate ONLY the Python code without any explanations or markdown formatting.

        ---

        **Hint**: If the existing host test lacks sufficient coverage, expand upon it by generating as many unique test cases as possible. Combine ideas from similar tests and the host test to craft robust, clear, and complete test cases.

        Generate the test code now:
        """

        return ChatPromptTemplate.from_messages([
            ("system", "You are a test generation assistant. Generate only Python code without any explanations or markdown formatting."),
            ("user", template)
        ])
    

    def generate_test(self, repo_name: str, host_test, similar_test) -> str:
        """Generate a unit test for the given method using multiple sources of context"""
        
        method_under_test = host_test["methods_under_test"][0]["body"]
        donor_tests = similar_test["source_code"]
        donor_method_under_test = similar_test["methods_under_test"][0]["body"]

        # Rest of the retrieval logic remains the same
        source_db = self.indexer.index_repository(repo_name, load_tests=False)
        source_retriever = source_db.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 3}
        )
        relevant_source = source_retriever.get_relevant_documents(method_under_test)
        
        test_db = self.indexer.index_repository(repo_name, load_tests=True) 
        test_retriever = test_db.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 3}
        )
        relevant_tests = test_retriever.get_relevant_documents(method_under_test)

        # Generate test using LLM with flattened parameters
        chain = self.prompt | self.llm | StrOutputParser()
        return chain.invoke({
            "repo_name": repo_name,
            "method_under_test": method_under_test,
            "relevant_source": relevant_source,
            "relevant_tests": relevant_tests,
            "donor_tests": donor_tests,
            "donor_method_under_test": donor_method_under_test,
            
            # Similar Test Information
            "test_name": similar_test["name"],
            "test_module": similar_test["module"],
            "class_name": similar_test["class_name"],
            "docstring": similar_test["docstring"],
            "decorators": similar_test.get("decorators", []),
            "arguments": similar_test.get("arguments", []),
            "imports": similar_test.get("imports", []),
            "fixtures": similar_test.get("fixtures", []),
            "assertions": similar_test.get("assertions", []),
            "setup_method": similar_test.get("setup_method"),
            "teardown_method": similar_test.get("teardown_method"),
            "mocks": similar_test.get("mocks", []),
            
            # Host Test Information
            "host_test_name": host_test["name"],
            "host_test_module": host_test["module"],
            "host_test_source_code": host_test["source_code"],
            "host_test_imports": host_test.get("imports", []),
            "host_test_assertions": host_test.get("assertions", []),
            "host_test_arguments": host_test.get("arguments", []),
            "host_test_fixtures": host_test.get("fixtures", []),
            "host_test_decorators": host_test.get("decorators", []),
            "host_test_setup_method": host_test.get("setup_method"),
            "host_test_teardown_method": host_test.get("teardown_method")
        })

    def _create_baseline1_prompt_template(self) -> ChatPromptTemplate:
        template = """You are tasked with generating a Python unit test. Generate ONLY the Python code without any explanations or markdown formatting.

        This is a test generation task for the **host project method** . The goal is to improve the coverage of the method under test while utilizing relevant information from the host project's test code.

        ---

        **Method to Test (from {repo_name}):**
        {method_under_test}

        **Existing Host Test Code:**
        {host_test_source_code}

        **Host Test Information:**
        1. Test Name: {host_test_name}
        2. Module: {host_test_module}
        3. Imports: {host_test_imports}
        4. Assertions: {host_test_assertions}
        5. Arguments: {host_test_arguments}
        6. Fixtures: {host_test_fixtures}
        7. Decorators: {host_test_decorators}
        8. Setup Method: {host_test_setup_method}
        9. Teardown Method: {host_test_teardown_method}

        ---

        ### Requirements:
        1. **Leverage Host Test Information**: Use existing imports, structure, naming conventions, and argument/fixture usage from the host test where applicable.
        2. **Avoid Duplication**: If the host test already tests certain aspects, focus on covering edge cases or alternative scenarios for the method.
        3. **Increase Coverage**: Ensure the generated test improves test coverage by testing edge cases, negative cases, or underexplored aspects of the method.
        5. Include any **necessary imports**, **fixtures**, or **mocks** to make the test runnable.
        6. Generate ONLY the Python code without any explanations or markdown formatting.

        ---

        **Hint**: If the existing host test lacks sufficient coverage, expand upon it by generating as many unique test cases as possible.

        Generate the test code now:
        """

        return ChatPromptTemplate.from_messages([
            ("system", "You are a test generation assistant. Generate only Python code without any explanations or markdown formatting."),
            ("user", template)
        ])
    

    def generate_baseline1_test(self, repo_name: str, host_test) -> str:
        """Generate a unit test for the given method using multiple sources of context"""
        
        method_under_test = host_test["methods_under_test"][0]["body"]

        # Generate test using LLM with flattened parameters
        chain = self.prompt | self.llm | StrOutputParser()
        return chain.invoke({
            "repo_name": repo_name,
            "method_under_test": method_under_test,
            
            # Host Test Information
            "host_test_name": host_test["name"],
            "host_test_module": host_test["module"],
            "host_test_source_code": host_test["source_code"],
            "host_test_imports": host_test.get("imports", []),
            "host_test_assertions": host_test.get("assertions", []),
            "host_test_arguments": host_test.get("arguments", []),
            "host_test_fixtures": host_test.get("fixtures", []),
            "host_test_decorators": host_test.get("decorators", []),
            "host_test_setup_method": host_test.get("setup_method"),
            "host_test_teardown_method": host_test.get("teardown_method")
        })


    def generator_processor(self, repo_name: str) -> None:
        """Process test pairs from JSON file and generate unit tests.
        
        Args:
            repo_name: Name of the repository to process
            
        The function reads the JSON file with test pairs, generates tests for each pair,
        and saves them to individual files.
        """
        # Construct path to JSON file
        json_path = Path(f"./__internal__/pairs_output/retrieve_pairs_{repo_name}_method_explanation_similarity_score_threshold.json")
        
        if not json_path.exists():
            raise FileNotFoundError(f"Could not find pairs file for repo {repo_name} at {json_path}")
            
        # Create output directory
        output_dir = Path(f"__internal__/results/{repo_name}")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Load and process pairs
        with open(json_path, 'r') as f:
            data = json.load(f)
            pairs = data.get("pairs", [])
            
        total_pairs = len(pairs)
        for idx, pair in enumerate(pairs, 1):
            host_test = pair["host_test"]
            similar_tests = pair["similar_tests"]
            
            # Generate test for host test and each similar test
            for similar_test in similar_tests:
                print(f"Processing pair {idx}/{total_pairs} - Generating test for {host_test['name']} based on {similar_test['name']}")
                
                generated_test = self.generate_test(
                    repo_name=repo_name,
                    host_test=host_test,
                    similar_test=similar_test
                )
                
                # Generate unique filename based on host and donor test names
                filename = self.file_generator(
                    output_dir=output_dir,
                    host_test_name=host_test["name"],
                    donor_test_name=similar_test["name"],
                    generated_content=generated_test
                )
                
                print(f"Generated test saved to {filename}")
                
        print(f"\nCompleted processing {total_pairs} test pairs for {repo_name}")

    def file_generator(self, output_dir: Path, host_test_name: str, donor_test_name: str, generated_content: str) -> str:
        """Generate a file containing the test code.
        
        Args:
            output_dir: Directory to write file to
            host_test_name: Name of the host test
            donor_test_name: Name of the donor test
            generated_content: The generated test content
            
        Returns:
            Path to the generated file
        """
        # Create sanitized filename from test names
        filename = f"test_{host_test_name}_from_{donor_test_name}.py"
        # filename = f"new_test_from_{donor_test_name}.py"
        filename = "".join(c if c.isalnum() or c in "._- " else "_" for c in filename)
        
        file_path = output_dir / filename
        
        # Write content to file
        with open(file_path, 'w') as f:
            f.write(generated_content)
            
        return str(file_path)

    def baseline_file_generator(self, output_dir: Path, host_test_name: str, generated_content: str) -> str:
        """Generate a file containing the test code.
        
        Args:
            output_dir: Directory to write file to
            host_test_name: Name of the host test
            generated_content: The generated test content
            
        Returns:
            Path to the generated file
        """
        # Create sanitized filename from test names
        filename = f"test_{host_test_name}_new.py"
        filename = "".join(c if c.isalnum() or c in "._- " else "_" for c in filename)
        
        file_path = output_dir / filename
        
        # Write content to file
        with open(file_path, 'w') as f:
            f.write(generated_content)
            
        return str(file_path)

if __name__ == "__main__":
    generator = UnitTestsGenerator()
    generator.generator_processor("flask")