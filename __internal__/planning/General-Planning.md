# Research High-Level Overview: Leveraging LLMs for Software Engineering Tasks

## Project Focus: Test Transplantation

### Objective
Develop a system for transplanting unit tests between software projects, with a focus on semi-automated processes.

### Approach Options
1. Retrieval-Augmented Generation (RAG)
2. Fine-tuning (challenging, requires substantial data)
3. Prompting
4. RAG + Prompting (requires less data, potentially most promising)

### Implementation Plan

#### 1. Data Collection
- Download diverse Python repositories
- Use Python parsers (e.g., `ast` module) to extract unittest code ("potential organs")

#### 2. Scenario Development
Example: A company with two products, Product A and Product B

#### 3. Dataset Creation
- Focus on basic projects: Web Development, API Development (e.g., Django vs Flask)
- Look for concrete pairs of mature repositories for transplantation
- Create an `Examples.md` file to document sample cases
- Estimate required number of datapoints (TBD)

#### 4. Data Structure
Input: [Project A, Test in Project A, Project B]
Output: [Test in Project B]

#### 5. Codebase Parsing
Utilize the `ast` module for Python code analysis

### Next Steps
1. Define specific criteria for selecting repositories
2. Develop a script to automate unittest extraction
3. Create initial dataset with 5-10 example pairs
4. Experiment with RAG + Prompting approach
5. Evaluate results and refine methodology

### Resources
- Python `ast` module documentation
- GitHub API for repository discovery
- Copilot LLM for assistance with unfamiliar tasks

### Notes
- Semi-automated approach allows for human oversight and quality control
- Consider version control integration for seamless test updates
- Explore potential for cross-language test transplantation in future iterations
