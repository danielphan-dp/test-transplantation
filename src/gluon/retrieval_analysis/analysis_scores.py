import os
import json
import numpy as np
from typing import List, Dict, Any, Tuple
import statistics
from collections import defaultdict

from ..retriever import RetrieverProcessor, Retriever


class StatisticalRetrieverProcessor(RetrieverProcessor):
    """
    Extended RetrieverProcessor that collects statistical data on retrieval scores
    for all donor data items
    """
    
    def __init__(self, tcm_summary_path, summary_type, retrieve_method, embedding_model):
        super().__init__(tcm_summary_path, summary_type, retrieve_method, embedding_model)
        self.output_dir = "./__internal__/retrieval_analysis"
        os.makedirs(self.output_dir, exist_ok=True)
        
    def _retrieve_similar_items(self, query: str, donor_data: List[str], k: int = None) -> List:
        """
        Retrieve similar items using the specified retrieval method with statistical analysis
        
        Args:
            query: Query to search for
            donor_data: Complete list of donor data
            k: Number of results to retrieve (defaults to all donor data)
        
        Returns:
            List of retrieval results with their scores
        """
        # If k is not specified, use the total number of donor data items
        if k is None:
            k = len(donor_data)
        
        if self.retrieve_method == "similarity_search_with_relevance_scores":
            # Get all possible matching items with scores
            return Retriever.similarity_search_with_relevance_scores(self.db.GetVector(), query, k)
        elif self.retrieve_method == "similarity_search_with_score":
            # Get all possible matching items with scores
            return Retriever.similarity_search_with_score(self.db.GetVector(), query, k)
        else:
            raise ValueError(f"This class only supports 'similarity_search_with_relevance_scores' or 'similarity_search_with_score' methods, got: {self.retrieve_method}")

    def _calculate_statistics(self, scores: List[float]) -> Dict[str, float]:
        """
        Calculate statistics for a list of scores
        
        Args:
            scores: List of similarity scores
            
        Returns:
            Dictionary containing various statistical measures
        """
        if not scores:
            return {
                "min": None,
                "max": None,
                "mean": None,
                "median": None,
                "variance": None,
                "std_dev": None,
                "top-5_score": None,
                "top-10_score": None,
                "top-15_score": None,
                "top-20_score": None,
                "percentile_25": None,
                "percentile_75": None,
                "percentile_90": None,
                "percentile_95": None
            }
        
        scores = sorted(scores)
        
        # Calculate top-k scores (if available)
        top_5_idx = min(4, len(scores) - 1) if len(scores) > 0 else None
        top_10_idx = min(9, len(scores) - 1) if len(scores) > 0 else None
        top_15_idx = min(14, len(scores) - 1) if len(scores) > 0 else None
        top_20_idx = min(19, len(scores) - 1) if len(scores) > 0 else None
        
        return {
            "min": min(scores),
            "max": max(scores),
            "mean": statistics.mean(scores),
            "median": statistics.median(scores),
            "variance": statistics.variance(scores) if len(scores) > 1 else 0,
            "std_dev": statistics.stdev(scores) if len(scores) > 1 else 0,
            "top-5_score": scores[top_5_idx] if top_5_idx is not None else None,
            "top-10_score": scores[top_10_idx] if top_10_idx is not None else None,
            "top-15_score": scores[top_15_idx] if top_15_idx is not None else None,
            "top-20_score": scores[top_20_idx] if top_20_idx is not None else None,
            "percentile_25": np.percentile(scores, 25),
            "percentile_75": np.percentile(scores, 75),
            "percentile_90": np.percentile(scores, 90),
            "percentile_95": np.percentile(scores, 95)
        }
    
    def process_tcm_summary_file(self):
        """
        Process the TCM summary file and collect statistical data on retrieval scores
        
        Returns:
            Tuple of (results, overall_stats) where:
            - results: List of tuples with (host_item, similar_items)
            - overall_stats: Dictionary with overall statistics
        """
        # Load host data
        host_data = self.data_extractor.load_data(self.tcm_summary_path)
        host_extracted_data = self._extract_data_by_type(host_data)

        # Get all donor repositories
        donor_repos = self._get_all_repos()

        # Process donor data
        all_donor_data = []
        all_donor_extracted_data = []
        for donor in donor_repos:
            donor_data = self.data_extractor.load_data(os.path.join(self.tcm_summary_path.replace(f"{self.host_repo}_tcm_with_summaries.json", ""), f"{donor}_tcm_with_summaries.json"))
            donor_extracted_data = self._extract_data_by_type(donor_data)
            all_donor_data.extend(donor_data)
            all_donor_extracted_data.extend(donor_extracted_data)
        
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
        all_scores = []
        
        # For overall statistics
        score_distribution = defaultdict(int)
        score_ranges = [(0.0, 0.1), (0.1, 0.2), (0.2, 0.3), (0.3, 0.4),
                        (0.4, 0.5), (0.5, 0.6), (0.6, 0.7), (0.7, 0.8),
                        (0.8, 0.9), (0.9, 1.0)]
        
        for idx, host_item in enumerate(host_extracted_data):
            if self.retrieve_method in ["similarity_search_with_relevance_scores", "similarity_search_with_score"]:
                # Get all donor data for complete statistical analysis
                retrieved_items = self._retrieve_similar_items(host_item, all_donor_extracted_data, k=len(all_donor_extracted_data))
                
                if not retrieved_items:
                    print(f"No retrieved items for host item {idx}")
                    continue
                
                target_host_item = host_data[idx]
                simplified_host_item = {
                    "test": target_host_item.get("test", ""),
                    "code": target_host_item.get("code", "")
                }
                
                # Extract scores and add to overall statistics
                item_scores = []
                similar_items = []
                
                for retrieved, score in retrieved_items:
                    # Convert score if using relevance scores (might be in different format)
                    score_value = float(score)
                    item_scores.append(score_value)
                    all_scores.append(score_value)
                    
                    # Count scores in ranges for distribution analysis
                    for lower, upper in score_ranges:
                        if lower <= score_value < upper:
                            score_distribution[(lower, upper)] += 1
                            break
                    
                    # Find the donor item
                    donor_pair_idx = all_donor_extracted_data.index(retrieved.page_content)
                    donor_pair = all_donor_data[donor_pair_idx]
                    
                    # Create simplified version with only necessary fields
                    simplified_donor = {
                        "test": donor_pair.get("test", ""),
                        "code": donor_pair.get("code", ""),
                        "score": score_value
                    }
                    similar_items.append(simplified_donor)
                
                # Sort similar items by score (ascending for distance, descending for similarity)
                if self.retrieve_method == "similarity_search_with_relevance_scores":
                    # Higher is better for relevance scores
                    similar_items.sort(key=lambda x: x["score"], reverse=True)
                    item_scores.sort(reverse=True)
                else:
                    # Lower is better for distance scores
                    similar_items.sort(key=lambda x: x["score"])
                    item_scores.sort()
                
                # Calculate statistics for this host item
                item_stats = self._calculate_statistics(item_scores)
                
                # Create the result entry
                result_entry = {
                    "host_item": simplified_host_item,
                    "stats": item_stats,
                    "sorted_scores": item_scores[:20],  # Only store top 20 scores to save space
                    "similar_items": similar_items[:20]  # Only store top 20 items to save space
                }
                
                results.append(result_entry)
        
        # Calculate overall statistics
        overall_stats = {
            "total_host_items": len(results),
            "total_donor_items": len(all_donor_extracted_data),
            "statistics": self._calculate_statistics(all_scores),
            "score_distribution": {f"{lower:.1f}-{upper:.1f}": count 
                                 for (lower, upper), count in sorted(score_distribution.items())}
        }
        
        return results, overall_stats
    
    def save_results(self, results: List[Dict], overall_stats: Dict):
        """
        Store the retrieved results with statistics in a JSON file
        
        Args:
            results: List of result entries with host items and similar items
            overall_stats: Dictionary with overall statistics
        """
        output_data = {
            "summary": overall_stats,
            "relevant_pairs": results
        }

        output_filename = f"{self.host_repo}_{self.summary_type}_{self.retrieve_method}_analysis.json"
        output_path = os.path.join(self.output_dir, output_filename)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)

        print(f"Stored analysis with {len(results)} pairs and overall statistics in {output_path}")
        return output_path


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Statistical analysis of code retrieval scores")
    parser.add_argument("--files", nargs="+", help="Specific TCM files to process (e.g., flask_tcm_with_summaries.json)")
    parser.add_argument("--all", action="store_true", help="Process all TCM files in ./__internal__/tc_sets_summary")
    parser.add_argument("--frameworks", nargs="+", help="Specific frameworks to process (e.g., flask sanic)")
    parser.add_argument("--summary_type", choices=["code", "pair"], default="code", help="Type of summary to process")
    parser.add_argument("--embedding_model_name", type=str, default="sentence-transformers/all-mpnet-base-v2", 
                      help="Name of the embedding model")
    parser.add_argument("--retrieve_method", choices=["similarity_search_with_relevance_scores", "similarity_search_with_score"], 
                      default="similarity_search_with_relevance_scores", help="Retrieval method for analysis")
    args = parser.parse_args()

    # Determine which files to process
    import glob
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
        print(f"\nProcessing {tcm_summary}...")
        retriever_processor = StatisticalRetrieverProcessor(
            tcm_summary, 
            args.summary_type, 
            args.retrieve_method, 
            args.embedding_model_name
        )
        results, overall_stats = retriever_processor.process_tcm_summary_file()
        output_path = retriever_processor.save_results(results, overall_stats)
        processed_files.append(output_path)

    print("\nProcessing complete. Analysis files generated:")
    for file in processed_files:
        print(f"- {file}")


if __name__ == "__main__":
    main()