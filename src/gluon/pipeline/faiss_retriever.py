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
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever

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

    @classmethod
    def ensemble(cls, faiss_db, data, query, faiss_topk, bm25_topk):
        """
        Perform ensemble search, retrieve top-k results from FAISS DB and BM25 retriever
        :param faiss_db: FAISS DB vector store
        :param data: Donor data to be retrieved
        :param query: Query to search for
        :param faiss_topk: Number of top-k results to retrieve from FAISS DB
        :param bm25_topk: Number of top-k results to retrieve from BM25
        :return: Top-k results from FAISS DB and BM25
        """
        documents = []
        for d in data:
            doc = Document(
                page_content=d,
                metadata={"type": type},
            )
            documents.append(doc)

        bm25_retriever = BM25Retriever.from_documents(documents)
        bm25_retriever.k = bm25_topk
        retriever = EnsembleRetriever(
            retrievers=[
                faiss_db.as_retriever(search_kwargs={"k": faiss_topk}),
                bm25_retriever
            ],
            weights=[0.6, 0.4],
        )
        return retriever.invoke(query)


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

    def extract_method_explanation(self, data: List[dict]) -> List[str]:
        """Extract method explanations from test data entries"""
        method_explanations = []
        for item in data:
            for method in item["methods_under_test"]:
                method_explanations.append(method["method_explanation"])
        print(f"Extracted {len(method_explanations)} method explanations")
        return method_explanations





class Processor:
    """Process and retrieve similar test cases across multiple repositories"""
    def __init__(self, host_name: str, index_key: str, retrieve_method: str):
        """
        Initialize the processor
        :param host_name: Name of the host repository
        :param index_key: Key to index ('source_code', 'methods_under_test', 'method_explanation')
        :param retrieve_method: Retrieval method to use ('similarity_search', 'mmr', 'similarity_score_threshold', 'ensemble')
        """
        self.embedding_model_name = "sentence-transformers/all-mpnet-base-v2"
        self.host_name = host_name
        self.index_key = index_key
        self.retrieve_method = retrieve_method
        self.data_dir = "./__internal__/collected_tests_explanation"
        self.faiss_dir = "./__internal__/faissdb"
        self.output_dir = "./__internal__/pairs_output"

        # Initialize databases
        self.db = CodebaseIndexer(self.embedding_model_name)
        self.data_extractor = TestDataExtractor()

        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)

    def _get_all_repos(self) -> List[str]:
        """Get all repository names from the data directory"""
        files = os.listdir(self.data_dir)
        repos = [f.replace("collected_tests_explanation__", "").replace(".json", "")
                for f in files if f.endswith('.json')]
        return [repo for repo in repos if repo != self.host_name]

    def _extract_data_by_key(self, data: List[dict]) -> List[str]:
        """Extract data based on the index key"""
        if self.index_key == "source_code":
            return self.data_extractor.extract_source_code(data)
        elif self.index_key == "methods_under_test":
            return self.data_extractor.extract_methods_under_test(data)
        elif self.index_key == "code_explanation":
            return self.data_extractor.extract_code_explanations(data)
        elif self.index_key == "method_explanation":
            return self.data_extractor.extract_method_explanation(data)
        else:
            raise ValueError(f"Invalid index key: {self.index_key}")

    def _process_methods_under_test(self, test_data: dict, method_index: int) -> dict:
        """Create a copy of test data with only one method under test"""
        result = test_data.copy()
        if "methods_under_test" in result and len(result["methods_under_test"]) > method_index:
            result["methods_under_test"] = [result["methods_under_test"][method_index]]
        return result

    def _retrieve_similar_items(self, query: str, donor_data: List[str], k: int = 10) -> List:
        """Retrieve similar items using the specified retrieval method"""
        if self.retrieve_method == "similarity_search":
            return Retriever.similarity_search(self.db.GetVector(), query, k)
        elif self.retrieve_method == "mmr":
            return Retriever.mmr(self.db.GetVector(), query, k, fetch_k=k*2)
        elif self.retrieve_method == "similarity_score_threshold":
            # return Retriever.similarity_score_threshold(self.db.GetVector(), query, k, score_threshold=0.6)
            return Retriever.similarity_score_threshold(self.db.GetVector(), query, 5, score_threshold=0.6)
        elif self.retrieve_method == "ensemble":
            return Retriever.ensemble(self.db.GetVector(), donor_data, query, k, bm25_topk=5)
        else:
            raise ValueError(f"Invalid retrieve method: {self.retrieve_method}")

    def process(self) -> List[tuple]:
        """
        Process the repositories and return similar test cases
        :return: List of tuples containing (host_test, List[similar_donor_tests])
        """
        # Load host data
        host_file = f"{self.data_dir}/collected_tests_explanation__{self.host_name}.json"
        host_data = self.data_extractor.load_data(host_file)
        host_extracted = self._extract_data_by_key(host_data)

        # Get all donor repositories
        donor_repos = self._get_all_repos()

        # Process donor data
        all_donor_data = []
        all_donor_extracted = []

        for donor_name in donor_repos:
            donor_file = f"{self.data_dir}/collected_tests_explanation__{donor_name}.json"
            donor_data = self.data_extractor.load_data(donor_file)
            all_donor_data.extend(donor_data)
            all_donor_extracted.extend(self._extract_data_by_key(donor_data))

        # Create or load FAISS database
        donor_db_path = f"{self.faiss_dir}/{self.host_name}/{self.index_key}"
        os.makedirs(os.path.dirname(donor_db_path), exist_ok=True)

        if not os.path.exists(f"{donor_db_path}/index.faiss"):
            self.db.StoreData(all_donor_extracted, type="donor_data")
            self.db.SaveToLocal(donor_db_path)
        else:
            self.db.LoadFromLocal(donor_db_path)

        # Process and retrieve similar items
        results = []
        for idx, host_item in enumerate(host_extracted):
            retrieved_items = self._retrieve_similar_items(host_item, all_donor_extracted)

            if not retrieved_items:
                continue

            # print(retrieved_items)

            host_test = host_data[idx]
            similar_tests = []

            for retrieved in retrieved_items:
                donor_test_idx = all_donor_extracted.index(retrieved.page_content)
                similar_tests.append(all_donor_data[donor_test_idx])

            if similar_tests:
                results.append((host_test, similar_tests))

        return results


    def store_results(self, results: List[tuple]) -> None:
        """
        Store the retrieved pairs in a JSON file
        :param results: List of tuples containing (host_test, List[similar_donor_tests])
        """
        output_data = []

        for host_test, similar_tests in results:
            pair = {
                "host_test": host_test,
                "similar_tests": similar_tests
            }
            output_data.append(pair)

        output_filename = f"retrieve_pairs_{self.host_name}_{self.index_key}_{self.retrieve_method}.json"
        output_path = os.path.join(self.output_dir, output_filename)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({"pairs": output_data}, f, indent=2, ensure_ascii=False)

        print(f"Stored {len(results)} pairs in {output_path}")


if __name__ == "__main__":
    # Example usage
    processor = Processor(
        host_name="uvicorn",
        index_key="method_explanation",
        retrieve_method="similarity_score_threshold"
    )
    print(f"Processing {processor.host_name} with {processor.index_key} and {processor.retrieve_method}")
    results = processor.process()
    processor.store_results(results)

    processor = Processor(
        host_name="aiohttp",
        index_key="method_explanation",
        retrieve_method="similarity_score_threshold"
    )
    print(f"Processing {processor.host_name} with {processor.index_key} and {processor.retrieve_method}")
    results = processor.process()
    processor.store_results(results)

    processor = Processor(
        host_name="connexion",
        index_key="method_explanation",
        retrieve_method="similarity_score_threshold"
    )
    print(f"Processing {processor.host_name} with {processor.index_key} and {processor.retrieve_method}")
    results = processor.process()
    processor.store_results(results)

    processor = Processor(
        host_name="flask",
        index_key="method_explanation",
        retrieve_method="similarity_score_threshold"
    )
    print(f"Processing {processor.host_name} with {processor.index_key} and {processor.retrieve_method}")
    results = processor.process()
    processor.store_results(results)

    processor = Processor(
        host_name="fastapi",
        index_key="method_explanation",
        retrieve_method="similarity_score_threshold"
    )
    print(f"Processing {processor.host_name} with {processor.index_key} and {processor.retrieve_method}")
    results = processor.process()
    processor.store_results(results)

    processor = Processor(
        host_name="gunicorn",
        index_key="method_explanation",
        retrieve_method="similarity_score_threshold"
    )
    print(f"Processing {processor.host_name} with {processor.index_key} and {processor.retrieve_method}")
    results = processor.process()
    processor.store_results(results)

    processor = Processor(
        host_name="sanic",
        index_key="method_explanation",
        retrieve_method="similarity_score_threshold"
    )
    print(f"Processing {processor.host_name} with {processor.index_key} and {processor.retrieve_method}")
    results = processor.process()
    processor.store_results(results)

    processor = Processor(
        host_name="pyramid",
        index_key="method_explanation",
        retrieve_method="similarity_score_threshold"
    )
    print(f"Processing {processor.host_name} with {processor.index_key} and {processor.retrieve_method}")
    results = processor.process()
    processor.store_results(results)

    # Print some example results
    # for idx, (host_test, similar_tests) in enumerate(results[:2]):  # Show first 2 results
    #     print(f"\nExample {idx + 1}:")
    #     print(f"Host test from {host_test['repo_name']}:")
    #     print(f"Source code: {host_test['source_code'][:200]}...")
    #     print("\nSimilar tests from donor repos:")
    #     for similar in similar_tests[:2]:  # Show first 2 similar tests
    #         print(f"\nFrom {similar['repo_name']}:")
    #         print(f"Source code: {similar['source_code'][:200]}...")