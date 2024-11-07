import json
import os
import faiss
from typing import List
from uuid import uuid4
from sentence_transformers import SentenceTransformer
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

class TestDataExtractor:
    """Extract and process test data from JSON files"""   
    @staticmethod
    def load_data(json_file: str) -> List[dict]:
        """Load test data from JSON file"""
        with open(json_file) as file:
            return json.load(file)["tests"]
    
    def extract_methods_under_test(self, data: List[dict]) -> List[str]:
        """Extract and combine unique method bodies from test data"""
        methods = []
        for item in data:
            if "methods_under_test" in item and item["methods_under_test"]:
                # Get unique "body"s from the current methods_under_test
                unique_bodies = set()
                for method in item["methods_under_test"]:
                    if "body" in method:
                        unique_bodies.add(method["body"])
                
                if unique_bodies:
                    # Combine all unique "body"s with \n\n separator
                    combined_body = "\n\n".join(unique_bodies)
                    methods.append(combined_body)
        
        print(f"Extracted {len(methods)} methods under test")
        return methods

    def extract_source_code(self, data: List[dict]) -> List[str]:
        """Extract source code from test data entries"""
        source_codes = []
        for item in data:
            if "source_code" in item and "methods_under_test" in item and item["methods_under_test"]:
                source_codes.append(item["source_code"])
        print(f"Extracted {len(source_codes)} source codes")
        return source_codes
    
    def extract_code_explanations(self, data: List[dict]) -> List[str]:
        """Extract code explanations from test data entries"""
        code_explanations = []
        for item in data:
            if "code_explanation" in item and item["code_explanation"] != "No methods under test found":
                code_explanations.append(item["code_explanation"])
        print(f"Extracted {len(code_explanations)} code explanations")
        return code_explanations

class CodebaseIndexer:
    """Index and manage source code repositories using FAISS"""
    def __init__(self, embedding_model_name):
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)
        self.vector_store = FAISS(
            embedding_function=self.embeddings,
            index=faiss.IndexFlatL2(768),
            docstore=InMemoryDocstore(),
            index_to_docstore_id={},
        )

    def StoreData(self, data, type):
        """
        Store data in FAISS DB
        :param data: List of data to store
        :param type: Type of data, e.g. "donor_methods" or "donor_source_code"
        """
        documents = []
        for d in data:
            doc = Document(
                page_content=d,
                metadata={"type": type},
            )
            documents.append(doc)

        uuids = [str(uuid4()) for _ in range(len(documents))]
        self.vector_store.add_documents(documents=documents, ids=uuids)
        print(f"Stored {type} data with length {len(documents)} in FAISS DB")

    def SaveToLocal(self, path, index_name="index"):
        """
        Save the FAISS DB to local path
        :param path: Path to save the FAISS Database
        :param index_name: Name of the index
        """
        self.vector_store.save_local(path, index_name)
        print(f"Saved FAISS DB to {path}")

    def LoadFromLocal(self, path, index_name="index"):
        """
        Load the FAISS DB from local path
        :param path: Path to load the FAISS Database
        :param index_name: Name of the index
        """
        self.vector_store = FAISS.load_local(path, self.embeddings, index_name, allow_dangerous_deserialization=True)
        print(f"Loaded FAISS DB from {path}")

    def GetVector(self):
        """
        Get the FAISS DB vector store
        :return: FAISS DB vector store
        """
        return self.vector_store


class Retriever():
    """Retrieves relevant documents from a FAISS vector store based on semantic similarity to a query"""
    @classmethod
    def similarity_search(cls, db, query, topk):
        """
        Perform similarity search without score return, retrieve top-k results regrardless of the duplicate results
        :param db: FAISS DB vector store
        :param query: Query to search for
        :param topk: Number of top-k results to retrieve
        :return: Top-k results
        """
        retriever = db.as_retriever(search_kwargs={"k": topk})
        return retriever.get_relevant_documents(query)
    
    @classmethod
    def similarity_search_with_score(cls, db, query, topk):
        """
        Perform similarity search with score (L2 distance, smaller is more relevant) return, retrieve top-k results regrardless of the duplicate results
        :param db: FAISS DB vector store
        :param query: Query to search for
        :param topk: Number of top-k results to retrieve
        :return: Top-k results with similarity score (L2 distance, smaller is more relevant)
        """
        return db.similarity_search_with_score(query, k=topk)
    
    @classmethod
    def mmr(cls, db, query, topk, fetch_k):
        """
        Perform Maximal Marginal Relevance (MMR) search, retrieve top-k results with maximal marginal relevance, which is used to reduce redundancy in the search results
        :param db: FAISS DB vector store
        :param query: Query to search for
        :param topk: Number of top-k results to retrieve
        :param fetch_k: Maximum number of results to fetch
        :return: Top-k results with maximal marginal relevance
        """
        retriever = db.as_retriever(search_type="mmr", search_kwargs={"k": topk, "fetch_k": fetch_k})
        return retriever.get_relevant_documents(query)
    
    @classmethod
    def similarity_score_threshold(cls, db, query, topk, score_threshold):
        """
        Perform similarity search with score threshold, retrieve top-k results with similarity score threshold
        :param db: FAISS DB vector store
        :param query: Query to search for
        :param topk: Number of top-k results to retrieve
        :param score_threshold: Similarity score threshold
        :return: Top-k results with similarity score threshold
        """
        retriever = db.as_retriever(search_type="similarity_score_threshold", search_kwargs={"k": topk, "score_threshold": score_threshold})
        return retriever.get_relevant_documents(query)


if __name__ == "__main__":
    # Initialize
    embedding_model_name = "sentence-transformers/all-mpnet-base-v2"
    methods_db = CodebaseIndexer(embedding_model_name)
    source_code_db = CodebaseIndexer(embedding_model_name)
    code_explanation_db = CodebaseIndexer(embedding_model_name)
    donor_data_extractor = TestDataExtractor()
    host_data_extractor = TestDataExtractor()

    
    donor_name = "flask"
    host_name = "fastapi"
    data_dir = "./__internal__/collected_tests_explanation"
    donor_file = f"{data_dir}/collected_tests_explanation__{donor_name}.json"
    host_file = f"{data_dir}/collected_tests_explanation__{host_name}.json"

    methods_db_path = f"./__internal__/faissdb/{donor_name}/methods_under_test"
    source_code_db_path = f"./__internal__/faissdb/{donor_name}/source_code"
    code_explanation_db_path = f"./__internal__/faissdb/{donor_name}/code_explanation"
    

    if not os.path.exists(f"./__internal__/faissdb/{donor_name}"):
        os.makedirs(f"./__internal__/faissdb/{donor_name}")

        # Load and extract methods under tests and source codes
        donor_data = donor_data_extractor.load_data(donor_file)
        donor_methods = donor_data_extractor.extract_methods_under_test(donor_data)
        donor_source_codes = donor_data_extractor.extract_source_code(donor_data)
        donor_code_explanations = donor_data_extractor.extract_code_explanations(donor_data)
        
        methods_db.StoreData(donor_methods, type="donor_methods")
        source_code_db.StoreData(donor_source_codes, type="donor_source_code")
        code_explanation_db.StoreData(donor_code_explanations, type="donor_code_explanation")

        methods_db.SaveToLocal(methods_db_path)
        source_code_db.SaveToLocal(source_code_db_path)
        code_explanation_db.SaveToLocal(code_explanation_db_path)
    else:
        print("Donor FAISS DB already exists")
    
    host_data = host_data_extractor.load_data(host_file)
    host_methods = host_data_extractor.extract_methods_under_test(host_data)
    host_source_codes = host_data_extractor.extract_source_code(host_data)
    host_code_explanations = host_data_extractor.extract_code_explanations(host_data)

    methods_db.LoadFromLocal(methods_db_path)
    source_code_db.LoadFromLocal(source_code_db_path)
    code_explanation_db.LoadFromLocal(code_explanation_db_path)

    # TESTTTTTT ------------------- TESTTTTTTT
    k = 30
    score_threshold = 0.6
    for code_explanation in host_code_explanations:
        results = Retriever.similarity_score_threshold(code_explanation_db.GetVector(), code_explanation, k, score_threshold)
        if not results:
            print("No results found")
            continue
        print(f"\nCode Explanation: {code_explanation}")
        print(f"\nTop {k} code explanations from donor file for the code explanation:")
        for i, (res) in enumerate(results):
            print(f"\nRank {i+1}:")
            print(f"Method: {res.page_content}")


    # first_host_method = host_methods[0]
    # print(f"First method from host file: {first_host_method}")

    # # Search for top-k vectors for the first host method
    # k = 30
    # results = Retriever.similarity_search_with_score(methods_db.GetVector(), first_host_method, k)
    # print(f"\nTop {k} methods from donor file for the first host method:")
    # for i, (res, score) in enumerate(results):
    #     print(f"\nRank {i+1}: Similarity Score {score:.3f}")
    #     print(f"Method: {res.page_content}")

    # print("\n\n\n")

    # k = 30
    # results = Retriever.similarity_search(methods_db.GetVector(), first_host_method, k)
    # print(f"\nTop {k} methods from donor file for the first host method:")
    # for i, (res) in enumerate(results):
    #     print(f"\nRank {i+1}:")
    #     print(f"Method: {res.page_content}")
    
    # print("\n\n\n")

    # k = 30
    # fetch_k = 50
    # results = Retriever.mmr(methods_db.GetVector(), first_host_method, k, fetch_k)
    # print(f"\nTop {k} methods from donor file for the first host method:")
    # for i, (res) in enumerate(results):
    #     print(f"\nRank {i+1}:")
    #     print(f"Method: {res.page_content}")

    # print("\n\n\n")

    # k = 30
    # score_threshold = 0.1 # That is too low
    # results = Retriever.similarity_score_threshold(methods_db.GetVector(), first_host_method, k, score_threshold)
    # print(f"\nTop {k} methods from donor file for the first host method:")
    # for i, (res, score) in enumerate(results):
    #     print(f"\nRank {i+1}: Similarity Score {score:.3f}")
    #     print(f"Method: {res.page_content}")