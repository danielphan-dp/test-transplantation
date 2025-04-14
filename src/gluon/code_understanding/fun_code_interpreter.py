from pathlib import Path
import json
from typing import Dict
from uuid import uuid4

from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS  
from langchain_community.docstore.in_memory import InMemoryDocstore
# from langchain_community.document_loaders import GenericLoader
from langchain_community.document_loaders import DirectoryLoader, PythonLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter
from langchain.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser

import os
# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = "sk-<API_KEY>"

class CodebaseIndexer:
    """Index and manage source code repositories using FAISS"""
    def __init__(self, embedding_model_name="sentence-transformers/all-mpnet-base-v2"):
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)
        self.db_cache: Dict[str, FAISS] = {}
        
    def index_repository(self, repo_path: str) -> FAISS:
        """Index a source code repository and return vectorstore"""
        # Check cache
        if (repo_path in self.db_cache):
            return self.db_cache[repo_path]
        
        loader = DirectoryLoader(
            repo_path,
            glob="**/*.py",
            show_progress=True,
            loader_cls=PythonLoader
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
        
        self.db_cache[repo_path] = db
        return db

class TestDataLoader:
    """Load and process test data from JSON files"""
    @staticmethod 
    def load_test_data(json_file: str) -> dict:
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @staticmethod
    def save_test_data(data: dict, output_file: str):
        with open(output_file, 'w', encoding='utf-8') as f: 
            json.dump(data, f, indent=2)
            
    @staticmethod
    def get_repo_path(test_file: str) -> str:
        """Get repository path from test file path"""
        # Extract repo name from collected_tests__<repo>.json
        repo_name = Path(test_file).stem.split("__")[1]
        return f"__internal__/data_repo/{repo_name}"
    
    @staticmethod
    def get_repo_name(test_file: str) -> str:
        """Extract the repository name from the test file path."""
        return Path(test_file).stem.split("__")[1]

class TestExplainer:
    """Generate explanations for test cases using LLM and RAG"""
    def __init__(self, model_name="gpt-4o", temperature=0):
        self.llm = ChatOpenAI(model=model_name, temperature=temperature)
        # self.prompt = self._create_test_explanation_prompt()
        self.prompt = self._create_method_explanation_prompt()
    
    def _create_test_explanation_prompt(self) -> ChatPromptTemplate:
        template = """You are an expert code reviewer analyzing Python unit tests.
        Given the following test and relevant code from the codebase:

        Test Information:
        This is one of the unit tests for the {repository_name} repository.
        Name: {test_name}
        Source Code:
        {source_code}

        Methods Under Test:
        {methods_under_test}

        Module: {module}
        Arguments: {arguments}
        Assertions: {assertions}
        Docstring: {docstring}

        Relevant Code from Codebase:
        {relevant_code}

        Provide a **concise** and **clear** explanation in the following format:

        **Main Purpose of the Test**:
        [Your explanation here]

        **Specific Functionality or Behavior Verified**:
        [Your explanation here]

        **Code Being Tested and How It Works**:
        [Your explanation here]

        **Notable Testing Patterns or Techniques Used**:
        [Your explanation here]

        Focus on the most important aspects of the test and the code. Use clear and precise language to describe the test case.
        """
        
        return ChatPromptTemplate.from_messages([
            # ("system", "You are a specialized code analysis AI that explains unit tests."),
            ("system", "You are a highly skilled software engineer and code analyst specializing in Python unit tests. Your task is to provide detailed and insightful explanations of unit tests, focusing on their purpose, functionality, and implementation details. Be thorough yet concise in your explanations."),
            ("user", template)
        ])

    def generate_test_explanation(self, test: dict, repo_name: str, relevant_docs: list) -> str:
        """Generate explanation for a test using context from codebase"""
        # Format methods under test
        methods_str = "None" if not test.get('methods_under_test') else \
            "\n".join([f"- {m.get('name', 'Unknown')}: {m.get('body', 'No body')}" 
                    for m in test['methods_under_test']])
        
        # Format relevant code
        relevant_code = "\n\n".join([
            f"```python\n{doc.page_content}\n```\n" 
            for doc in relevant_docs
        ])

        # Create chain
        chain = self.prompt | self.llm | StrOutputParser()
        
        return chain.invoke({
            "repository_name": repo_name,
            "test_name": test['name'],
            "source_code": test['source_code'],
            "docstring": test['docstring'],
            "methods_under_test": methods_str, 
            "module": test.get('module', 'Unknown'),
            "arguments": ", ".join(test.get('arguments', [])),
            "assertions": "\n".join(test.get('assertions', [])),
            "relevant_code": relevant_code
        })
    
    def _create_method_explanation_prompt(self) -> ChatPromptTemplate:
        template = """You are an expert assistant helping to explain Python methods.
        Given the following method details and relevant code snippets from the repository:

        **Method Name**:
        {method_name}

        **Method Body**:
        ```python
        {method_body}
        ```

        Relevant Code Snippets:
        {relevant_code}

        Provide a **concise** explanation in the following format:

        **Main Purpose of the Method**:
        [Your explanation here]

        **How It Works**:
        [Your explanation here]

        Focus on clarity and relevance, ensuring the explanation assists developers in understanding the method's functionality and usage.
        """
        
        return ChatPromptTemplate.from_messages([
            ("system", "You are a skilled Python code assistant focused on explaining methods clearly and concisely."),
            ("user", template)
        ])

    def generate_explanation(self, method: dict, relevant_docs: list) -> str:
        """Generate explanation for a method using context from codebase"""
        # Format relevant code
        relevant_code = "\n\n".join([
            f"```python\n{doc.page_content}\n```\n" 
            for doc in relevant_docs
        ])

        # Create chain
        chain = self.prompt | self.llm | StrOutputParser()
        
        return chain.invoke({
            "method_name": method.get("name", "Unknown"),
            "method_body": method.get("body", "No body provided"),
            "relevant_code": relevant_code
        })

def main():
    # Initialize
    loader = TestDataLoader()
    indexer = CodebaseIndexer()
    explainer = TestExplainer()
    
    data_dir = Path("./__internal__/collected_tests/tests_v3_without_django")
    for json_file in data_dir.glob("collected_tests__*.json"):

        if not json_file.stem.endswith("flask"):
            print(f"Skipping {json_file}")
            continue

        print(f"\nProcessing tests from: {json_file}")
        
        test_data = loader.load_test_data(json_file)
        repo_name = loader.get_repo_name(json_file)
        repo_path = loader.get_repo_path(json_file)
        print(f"Indexing repository: {repo_path}")
        db = indexer.index_repository(repo_path)
        
        retriever = db.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 5}
        )
        
        total = len(test_data["tests"])
        count = 0

        for test in test_data["tests"]:
            print(f"({count+1}/{total}) Processing test {test['name']}")
            count += 1
            
            methods = test.get("methods_under_test", [])
            if not methods:
                print(f"Skipping test {test['name']} as it has no methods under test.")
                continue

            for method in methods:
                try:
                    # Use method details and relevant code for retrieval
                    query = f"{method['name']}\n{method['body']}"
                    relevant_docs = retriever.get_relevant_documents(query)

                    explanation = explainer.generate_explanation(method, relevant_docs)
                    method["method_explanation"] = explanation

                except Exception as e:
                    print(f"Error processing method {method['name']}: {str(e)}")
                    method["method_explanation"] = f"Error generating explanation: {str(e)}"

        
        # Save augmented test data
        output_dir = Path("./__internal__/collected_tests_explanation")
        output_dir.mkdir(exist_ok=True)
        output_file = output_dir / f"collected_tests_explanation__{json_file.stem.split('__')[1]}.json"
        loader.save_test_data(test_data, output_file)
        print(f"Saved explained tests to {output_file}")


def generate_eval_pairs_explanation():
    # Initialize
    loader = TestDataLoader()
    indexer = CodebaseIndexer()
    explainer = TestExplainer()
    
    data_dir = Path("./__internal__/collected_tests/tests_v3_without_django")
    for json_file in data_dir.glob("collected_tests__*.json"):

        print(f"\nProcessing tests from: {json_file}")
        
        test_data = loader.load_test_data(json_file)
        repo_name = loader.get_repo_name(json_file)
        repo_path = loader.get_repo_path(json_file)
        print(f"Indexing repository: {repo_path}")
        db = indexer.index_repository(repo_path)
        
        retriever = db.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 5}
        )
        
        total = len(test_data["tests"])
        count = 0

        for test in test_data["tests"]:
            print(f"({count+1}/{total}) Processing test {test['name']}")
            count += 1
            try:
                # Use method details and relevant code for retrieval
                # query = f"{method['name']}\n{method['body']}"
                query = f"{test['name']}\n{test['source_code']}\n{test['methods_under_test']}"
                relevant_docs = retriever.get_relevant_documents(query)

                explanation = explainer.generate_test_explanation(test, repo_name, relevant_docs)
                test["code_explanation"] = explanation

            except Exception as e:
                print(f"Error processing test {test['name']}: {str(e)}")
                test["code_explanation"] = f"Error generating explanation: {str(e)}"

        
        # Save augmented test data
        output_dir = Path("./__internal__/collected_evaluate_explanation")
        output_dir.mkdir(exist_ok=True)
        output_file = output_dir / f"collected_tests_explanation__{json_file.stem.split('__')[1]}.json"
        loader.save_test_data(test_data, output_file)
        print(f"Saved explained tests to {output_file}")

if __name__ == "__main__":
    main()