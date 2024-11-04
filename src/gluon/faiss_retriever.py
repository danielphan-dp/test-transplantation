import json
import os
import faiss
from uuid import uuid4
from sentence_transformers import SentenceTransformer
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document


def LoadData(json_file):
    with open(json_file) as file:
        return json.load(file)["tests"]
    print(f"Successfully loaded {json_file}")

def ExtractMethodsUnderTest(data):
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

def ExtractSourceCode(data):
    source_codes = []
    for item in data:
        if "source_code" in item and "methods_under_test" in item and item["methods_under_test"]:
            source_codes.append(item["source_code"])
    print(f"Extracted {len(source_codes)} source codes")
    return source_codes


class FaissDB:

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

    # Load the Path
    donor_file = "./__internal__/collected_tests/collected_tests__flask.json"
    host_file = "./__internal__/collected_tests/collected_tests__fastapi.json"

    donor_name = donor_file.split("/")[-1].split("__")[1].split(".")[0]
    host_name = host_file.split("/")[-1].split("__")[1].split(".")[0]

    methods_db_path = f"./__internal__/faissdb/{donor_name}/methods_under_test"
    source_code_db_path = f"./__internal__/faissdb/{donor_name}/source_code"

    # Initialize and store data in FAISS DB
    embedding_model_name = "sentence-transformers/all-mpnet-base-v2"
    methods_db = FaissDB(embedding_model_name)
    source_code_db = FaissDB(embedding_model_name)

    if not os.path.exists(f"./__internal__/faissdb/{donor_name}"):
        os.makedirs(f"./__internal__/faissdb/{donor_name}")

        # Load and extract methods under tests and source codes
        donor_data = LoadData(donor_file)
        donor_methods = ExtractMethodsUnderTest(donor_data)
        donor_source_codes = ExtractSourceCode(donor_data)

        methods_db.StoreData(donor_methods, type="donor_methods")
        source_code_db.StoreData(donor_source_codes, type="donor_source_code")

        methods_db.SaveToLocal(methods_db_path)
        source_code_db.SaveToLocal(source_code_db_path)
    else:
        print("Donor FAISS DB already exists")

    host_data = LoadData(host_file)
    host_methods = ExtractMethodsUnderTest(host_data)
    host_source_codes = ExtractSourceCode(host_data)

    methods_db.LoadFromLocal(methods_db_path)
    source_code_db.LoadFromLocal(source_code_db_path)

    # TESTTTTTT ------------------- TESTTTTTTT
    first_host_method = host_methods[0]
    print(f"First method from host file: {first_host_method}")

    # Search for top-k vectors for the first host method
    k = 30
    results = Retriever.similarity_search_with_score(methods_db.GetVector(), first_host_method, k)
    print(f"\nTop {k} methods from donor file for the first host method:")
    for i, (res, score) in enumerate(results):
        print(f"\nRank {i+1}: Similarity Score {score:.3f}")
        print(f"Method: {res.page_content}")

    print("\n\n\n")

    k = 30
    results = Retriever.similarity_search(methods_db.GetVector(), first_host_method, k)
    print(f"\nTop {k} methods from donor file for the first host method:")
    for i, (res) in enumerate(results):
        print(f"\nRank {i+1}:")
        print(f"Method: {res.page_content}")
    
    print("\n\n\n")

    k = 30
    fetch_k = 50
    results = Retriever.mmr(methods_db.GetVector(), first_host_method, k, fetch_k)
    print(f"\nTop {k} methods from donor file for the first host method:")
    for i, (res) in enumerate(results):
        print(f"\nRank {i+1}:")
        print(f"Method: {res.page_content}")

    print("\n\n\n")

    k = 30
    score_threshold = 0.1 # That is too low
    results = Retriever.similarity_score_threshold(methods_db.GetVector(), first_host_method, k, score_threshold)
    print(f"\nTop {k} methods from donor file for the first host method:")
    for i, (res, score) in enumerate(results):
        print(f"\nRank {i+1}: Similarity Score {score:.3f}")
        print(f"Method: {res.page_content}")