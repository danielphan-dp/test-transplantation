import glob
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

from .data_extractor import DataExtractor
from .config import REPOSITORIES



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
    

class RetrieverProcessor:
    """Process TCM summary files and extract data for retriever"""
    def __init__(self, tcm_summary_path, summary_type, retrieve_method, embedding_model):
        self.tcm_summary_path = tcm_summary_path
        self.summary_type = summary_type
        self.retrieve_method = retrieve_method
        self.embedding_model = embedding_model

        self.host_repo = self.tcm_summary_path.replace("_tcm_with_summaries.json", "").split("/")[-1]

        self.faiss_dir = "./__internal__/faiss_db"
        self.output_dir = "./__internal__/retriever_output"

        self.db = CodebaseIndexer(self.embedding_model)
        self.data_extractor = DataExtractor()

        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
    
    def _extract_data_by_type(self, data):
        """Extract data by type"""
        if self.summary_type == "pair":
            return self.data_extractor.extract_pair_summary(data)
        elif self.summary_type == "code":
            return self.data_extractor.extract_code_summary(data)
    
    def _get_all_repos(self):
        """Get all donor repositories"""
        return [repo for repo in REPOSITORIES if repo != self.host_repo]
    
    def _retrieve_similar_items(self, query: str, donor_data: List[str], k: int = 10) -> List:
        """Retrieve similar items using the specified retrieval method"""
        if self.retrieve_method == "similarity_search":
            return Retriever.similarity_search(self.db.GetVector(), query, k)
        elif self.retrieve_method == "similarity_search_with_relevance_scores":
            return Retriever.similarity_search_with_relevance_scores(self.db.GetVector(), query, 1)
        elif self.retrieve_method == "similarity_search_with_score":
            return Retriever.similarity_search_with_score(self.db.GetVector(), query, 1)
        elif self.retrieve_method == "mmr":
            return Retriever.mmr(self.db.GetVector(), query, k, fetch_k=k*2)
        elif self.retrieve_method == "similarity_score_threshold":
            # return Retriever.similarity_score_threshold(self.db.GetVector(), query, k, score_threshold=0.6)
            return Retriever.similarity_score_threshold(self.db.GetVector(), query, 1, score_threshold=0.6)
        elif self.retrieve_method == "ensemble":
            return Retriever.ensemble(self.db.GetVector(), donor_data, query, k, bm25_topk=5)
        else:
            raise ValueError(f"Invalid retrieve method: {self.retrieve_method}")

    def process_tcm_summary_file(self):
        # Load host data
        host_data = self.data_extractor.load_data(self.tcm_summary_path)
        host_extracted_data = self._extract_data_by_type(host_data)

        # Get all donor repositories
        donor_repos = self._get_all_repos()

        # Process donor data
        all_donor_data = []
        all_donor_extracted_data = []
        for donor in donor_repos:
            donor_data = self.data_extractor.load_data(os.path.join(self.tcm_summary_path, f"{donor}_tcm_with_summaries.json"))
            donor_extracted_data = self._extract_data_by_type(donor_data)
            all_donor_data.append(donor_data)
            all_donor_extracted_data.append(donor_extracted_data)
        
        # Create or load FAISS DB
        donor_db_path = f"{self.faiss_dir}/{self.host_repo}/{self.summary_type}"
        os.makedirs(donor_db_path, exist_ok=True)

        if not os.path.exists(f"{donor_db_path}/index.faiss"):
            self.db.StoreData(all_donor_extracted_data, type="donor_data")
            self.db.SaveToLocal(donor_db_path)
        else:
            self.db.LoadFromLocal(donor_db_path)
        
        # Process and retrieve similar items
        results = []
        for idx, host_item in enumerate(host_extracted_data):
            if self.retrieve_method in ["similarity_search_with_relevance_scores", "similarity_search_with_score"]:
                retrieved_items = self._retrieve_similar_items(host_item, all_donor_extracted_data)
                if not retrieved_items:
                    print(f"No retrieved items for host item {idx}")
                    continue
                
                target_host_item = host_data[idx]
                similar_items = []

                for retrieved, score in retrieved_items:
                    donor_pair_idx = all_donor_extracted_data.index(retrieved.page_content)
                    donor_pair = all_donor_data[donor_pair_idx]
                    donor_pair[f"{self.summary_type}_similarity_score"] = float(score)
                    similar_items.append(donor_pair)
                
                if similar_items:
                    results.append((target_host_item, similar_items))
        
        return results
    
    def save_results(self, results: List[tuple]):
        """
        Store the retrieved results in a JSON file
        :param results: List of tuples, each containing a host item and a list of similar items
        """
        output_data = []

        for host_item, similar_items in results:
            pair = {
                "host_item": host_item,
                "similar_items": similar_items
            }
            output_data.append(pair)

        output_dir = "./__internal__/relevant_pairs"
        os.makedirs(output_dir, exist_ok=True)
        output_filename = f"{self.host_repo}_{self.summary_type}_retrieved_pairs.json"
        output_path = os.path.join(output_dir, output_filename)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({"pairs": output_data}, f, indent=2, ensure_ascii=False)

        print(f"Stored {len(results)} pairs in {output_path}")
    

def main(args):

    # Determine which files to process
    tcm_summaries = []
    if args.files:
        tcm_summaries = [os.path.join("./__internal__/tc_sets_summary", f) for f in args.files]
        tcm_summaries = [f for f in tcm_summaries if os.path.exists(f)]
        
        missing = [f for f in args.files if not os.path.exists(os.path.join("./__internal__/tc_sets_summary", f))]
        if missing:
            print(f"Warning: These files were not found: {', '.join(missing)}")
    elif args.frameworks:
        for framework in args.frameworks:
            file = os.path.join("./__internal__/tc_sets_summary", f"{framework}_tcm_with_summaries.json")
            if os.path.exists(file):
                tcm_summaries.append(file)
            else:
                print(f"Warning: File not found for framework '{framework}': {file}")
    elif args.all or not (args.files or args.frameworks):
        tcm_summaries = glob.glob("./__internal__/tc_sets_summary/*_tcm_with_summaries.json")

    if not tcm_summaries:
        print("No TCM JSON files found to process.")
        return

    print(f"Will process {len(tcm_summaries)} files: {', '.join(tcm_summaries)}")

    processed_files = []
    for tcm_summary in tcm_summaries:
        if args.process_pair:
            # retriever_processor = RetrieverProcessor(tcm_summary, "pair", args.retrieve_method, args.embedding_model)
            print("TODO: Implement pair retrieval")
        elif args.process_code:
            retriever_processor = RetrieverProcessor(tcm_summary, "code", args.retrieve_method, args.embedding_model_name)
            results = retriever_processor.process_tcm_summary_file()
            retriever_processor.save_results(results)
            processed_files.append(tcm_summary)

    print("\nProcessing complete. Files generated:")
    for file in processed_files:
        print(f"- {file}")
    


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--files", nargs="+", help="Specific TCM files to process (e.g., flask_tcm_with_summaries.json)")
    parser.add_argument("--all", action="store_true", help="Process all TCM files in ./__internal__/tc_sets_summary")
    parser.add_argument("--frameworks", nargs="+", help="Specific frameworks to process (e.g., flask sanic)")
    parser.add_argument("--process_pair", action="store_true", help="Process only pair summaries")
    parser.add_argument("--process_code", action="store_true", help="Process only code summaries")
    parser.add_argument("--embedding_model_name", type=str, help="Name of the embedding model", default="sentence-transformers/all-mpnet-base-v2")
    parser.add_argument("--retrieve_method", type=str, help="Retrieval method", default="similarity_search")
    args = parser.parse_args()

    main(args)