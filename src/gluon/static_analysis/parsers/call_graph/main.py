import sys
from .analyzers.repo_analyzer import RepoAnalyzer


def main():
    """Main entry point for the call graph analyzer"""
    if len(sys.argv) < 2:
        print("Usage: python -m gluon.parsers.call_graph <repository_path> [output_directory] [--include-tests]")
        sys.exit(1)

    repo_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    include_tests = "--include-tests" in sys.argv

    try:
        analyzer = RepoAnalyzer(repo_path, output_dir, include_tests)
        analyzer.analyze()
    except Exception as e:
        print(f"Error analyzing repository: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
