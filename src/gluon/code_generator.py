import os
os.environ["OPENAI_API_KEY"] = "sk-<API_KEY>"

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
        
    def index_repository(self, repo_path: str, load_tests: bool = False) -> FAISS:
        """Index a source code repository and return vectorstore
        
        Args:
            repo_path: Path to the repository
            load_tests: If True, load only test files, otherwise load non-test files
        Returns:
            FAISS vector store containing the indexed documents
        """
        # Check cache key with load_tests parameter
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
        template = """You are a software engineer tasked with writing a unit test for a Python function.

        The function you need to test is:
        ```python
        {method_under_test}
        ```

        You have access to the following context:
        1. Relevant source code snippets:
        {relevant_source}

        2. Relevant test code snippets:
        {relevant_tests}

        3. Donor test cases:
        {donor_tests}

        4. Donor method under test:
        {donor_method_under_test}
        
        5. Donor test explanations:
        {donor_test_explanations}

        Write a unit test for the given function using the provided context.
        """

        return ChatPromptTemplate.from_messages([
            ("system", "You are a software engineer tasked with writing a unit test for a Python function."),
            ("user", template)
        ])
    

    def generate_test(self, repo_path: str, method_under_test: str, donor_tests: str, donor_method_under_test: str, donor_test_explanations: str) -> str:
        """Generate a unit test for the given method using multiple sources of context
        
        Args:
            repo_path: Path to the host repository
            method_under_test: Dictionary containing method information to test
            donor_tests: List of relevant donor tests with explanations
            
        Returns:
            Generated unit test code as string
        """
        # Get relevant source code from repo (excluding tests)
        source_db = self.indexer.index_repository(repo_path, load_tests=False)
        relevant_source = source_db.similarity_search(
            method_under_test, 
            k=3
        )
        
        # Get relevant test code from repo
        test_db = self.indexer.index_repository(repo_path, load_tests=True) 
        relevant_tests = test_db.similarity_search(
            method_under_test,
            k=3
        )

        # Generate test using LLM
        chain = self.prompt | self.llm | StrOutputParser()
        return chain.invoke({
            "method_under_test": method_under_test,
            "relevant_source": relevant_source,
            "relevant_tests": relevant_tests,
            "donor_tests": donor_tests,
            "donor_method_under_test": donor_method_under_test,
            "donor_test_explanations": donor_test_explanations
        })

    