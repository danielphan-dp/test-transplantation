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
    """Index and manage source code repositories"""
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

class TestExplainer:
    """Generate explanations for test cases using LLM and RAG"""
    def __init__(self, model_name="gpt-4o-mini", temperature=0):
        self.llm = ChatOpenAI(model=model_name, temperature=temperature)
        self.prompt = self._create_test_explanation_prompt()
    
    # Haven't modified the prompt in a proper way (such as FLASK should be replaced with the actual repository name parameter)
    def _create_test_explanation_prompt(self) -> ChatPromptTemplate:
        template = """You are an expert code reviewer analyzing Python unit tests.
        Given the following test and relevant code from the codebase:

        Test Information:
        This is one of the unit tests for the FLASK repository.
        Name: {test_name}
        Source Code:
        Methods Under Test: {methods_under_test} Module: {module} Arguments: {arguments} Assertions: {assertions}

        Relevant Code from Codebase: {relevant_code}

        Provide a concise explanation that covers:

        The main purpose of this test
        What specific functionality or behavior it verifies
        The code being tested and how it works
        Any notable testing patterns or techniques used
        Keep the explanation focused on explaining both the test and the actual code being tested."""
        
        return ChatPromptTemplate.from_messages([
            ("system", "You are a specialized code analysis AI that explains unit tests."),
            ("user", template)
        ])

    def generate_explanation(self, test: dict, relevant_docs: list) -> str:
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
            "test_name": test['name'],
            "source_code": test['source_code'],
            "methods_under_test": methods_str, 
            "module": test.get('module', 'Unknown'),
            "arguments": ", ".join(test.get('arguments', [])),
            "assertions": "\n".join(test.get('assertions', [])),
            "relevant_code": relevant_code
        })

def main():
    # Initialize
    loader = TestDataLoader()
    indexer = CodebaseIndexer()
    explainer = TestExplainer()
    
    data_dir = Path("__internal__/collected_tests")
    for json_file in data_dir.glob("collected_tests__*.json"):

        if not json_file.stem.endswith("flask"):
            print(f"Skipping {json_file}")
            continue

        print(f"\nProcessing tests from: {json_file}")
        
        test_data = loader.load_test_data(json_file)
        
        repo_path = loader.get_repo_path(json_file)
        print(f"Indexing repository: {repo_path}")
        db = indexer.index_repository(repo_path)
        
        retriever = db.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 8}
        )
        
        count = 0

        for test in test_data["tests"]:
            print(f"Processing test: {test['name']}")

            count += 1
            if count > 5:
                break
            
            try:
                # Use test name, source code, and methods under test for retrieval
                query = f"{test['name']}\n{test['source_code']}\n{test['methods_under_test']}"
                relevant_docs = retriever.get_relevant_documents(query)

                # relevant_src_code = retriever.get_relevant_documents(
                #     # Use test name and source code for retrieval
                #     test["name"] + "\n" + test["source_code"]
                # )

                # relevant_methods = retriever.get_relevant_documents(
                #     # Use test name and source code for retrieval
                #     test["methods_under_test"]
                # )
                
                explanation = explainer.generate_explanation(test, relevant_docs)
                test["code_explanation"] = explanation
                
            except Exception as e:
                print(f"Error processing test {test['name']}: {str(e)}")
                test["code_explanation"] = f"Error generating explanation: {str(e)}"
        
        # Save augmented test data
        output_dir = Path("./__internal__/collected_tests_explanation")
        output_dir.mkdir(exist_ok=True)
        output_file = output_dir / f"collected_tests_explanation__{json_file.stem.split('__')[1]}.json"
        loader.save_test_data(test_data, output_file)
        print(f"Saved explained tests to {output_file}")

if __name__ == "__main__":
    main()