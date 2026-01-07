# scripts/test_rag.py
"""
Refinement Layer 3 – Step 1 Test
Purpose: Evaluate response synthesis quality after temperature tuning.
Focus: Flow | Redundancy | Explanation quality
"""

from rag_pipeline import answer_query

TEST_CASES = [
    {
        "label": "Document Explanation – FIR",
        "query": "Explain FIR"
    },
    {
        "label": "Document Explanation – RTI",
        "query": "What is RTI application?"
    },
    {
        "label": "Document Explanation – Bail",
        "query": "What is a bail application?"
    },
    {
        "label": "Legal Concept – IPC Section",
        "query": "What is IPC Section 420?"
    },
    {
        "label": "Legal Concept – Arrest",
        "query": "What does arrest mean under Indian law?"
    }
]


def run_tests():
    print("\n" + "=" * 80)
    print("REFINEMENT LAYER 3 – STEP 1 | SYNTHESIS QUALITY TEST")
    print("Focus: Explanation flow, reduced repetition, natural narration")
    print("=" * 80)

    for i, test in enumerate(TEST_CASES, start=1):
        print(f"\nTEST {i}: {test['label']}")
        print("-" * 80)
        print("QUERY:")
        print(test["query"])
        print("\nRESPONSE:\n")

        response = answer_query(test["query"])
        print(response)

        print("-" * 80)

    print("\nAll synthesis tests completed.\n")


if __name__ == "__main__":
    run_tests()
