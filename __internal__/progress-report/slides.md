---
marp: true
theme: default
paginate: true
---

# Progress Report for Gluon (Test Transplanter)

## Ching-Ting Tsai, Daniel Phan, Yinxi Li

---

## Introduction

- **Challenges**
  - Open-source LLMs are hard to use and sometimes not work as expected
  - This problem requires long context, which is hard for LLMs to handle
- **Software Testing Importance**
  - Crucial for safety-critical and reliability-critical systems
- **Software Transplantation**
  - Extract features from a donor to a host program
  - Requires code adaptation
- **Our Aim**
  - Automate unit test transplantation
  - Utilize Retrieval Augmented Generation (RAG) and LLMs

---

## Data Collection

- **Repository Selection**
  - Handpicked 10 popular Python API repositories
- **Unit Test Extraction**
  - Parsed tests from `test` directories
- **Attributes Collected**
  - Name, module, class, file path
  - Source code, docstrings, decorators
  - Methods under test (challenging to identify)

---

## Data Collection Procedure

- **Parsing Challenges**
  - Complex import patterns
  - Matching tests to methods under test
- **Methodology**
  - Built ASTs for source files
  - Matched imports and paths to link tests with methods
- **Results**
  - Collected 10,676 tests from 344 classes
  - Average 1.4 methods under test per test

---

## Evaluation Pairs Collection

- **Purpose**
  - Identify similar unit tests between donor and host programs
- **Natural Language Descriptions**
  - Generated using LLMs for better understanding
- **Similarity Search**
  - Used FAISS vector database
  - Set similarity threshold for matching
- **Challenges**
  - Data completeness
  - Quality assurance in retrieval

---

## Case Study: FastAPI and Flask

- **Donor Test (Flask)**
  - `test_json_request_and_response`
  - Validates JSON processing in requests and responses
- **Host Test (FastAPI)**
  - `test_call_api`
  - Validates JSON handling across multiple endpoints
- **Relevance**
  - Both tests focus on JSON data integrity
  - Suitable for transplantation evaluation

---

## Retrieval Augmented Generation Pipeline

- **Process Overview**
  1. **Retrieval**
     - Locate organ test and relevant context
  2. **Augmentation**
     - Compile organ test with additional tests
  3. **Generation**
     - Use GPT-4 for code generation
  4. **Evaluation**
     - Validate generated test in host program

---

## RAG Pipeline Steps

| **Step**        | **Description**                          | **Tools Used**  |
|-----------------|------------------------------------------|-----------------|
| Retrieval       | Locate tests in donor program            | FAISS, LLM      |
| Augmentation    | Compile relevant tests and context       | Python Scripts  |
| Generation      | Generate transplanted test using GPT-4   | GPT-4 API       |
| Evaluation      | Compare with existing host tests         | Manual Review   |

---

## Evaluation Methods

- **Manual Inspection**
  - Check logical correctness
  - Ensure code relevance and adherence to standards
- **Code Metrics**
  - Code coverage analysis
  - Maintainability scores
- **Execution Tests**
  - Verify code runs without errors
  - Check integration with host program
- **LLM Utilization**
  - Use LLMs for code review
  - Assess structure and quality

---

## Comparison: Transplantation vs. LLM-Generated Tests

| **Criterion**       | **Transplantation** | **LLM-Generated Tests** |
|---------------------|---------------------|-------------------------|
| Relevance           | High                | Medium                  |
| Code Quality        | Consistent          | Varies                  |
| Execution Success   | Higher              | Lower                   |
| Developer Effort    | Reduced             | Moderate                |
| Integration Ease    | Better              | Requires Adjustment     |

---

## Conclusion

- **Challenges**
  - Data completeness and matching accuracy
  - Ensuring executability of transplanted tests
  - Scalability and Efficiency

---
