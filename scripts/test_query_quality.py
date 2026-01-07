# scripts/test_query_quality.py

from query_quality import is_vague_query

TEST_QUERIES = [
    "My brother was arrested",
    "Tell me about law"
]

print("\n=== VAGUE QUERY DETECTION TEST ===\n")

for q in TEST_QUERIES:
    result = is_vague_query(q)
    print(f"Query: {q}")
    print(f"Is Vague: {result['is_vague']}")
    print(f"Reason: {result['reason']}")
    print("-" * 40)
