# Features/Legal Chatbot/scripts/test_intent_router.py

from intent_router import classify_intent, QueryIntent

test_queries = [
    "What is an FIR?",
    "Explain bail application",
    "Which document should I file to get information from the government?",
    "Someone threatened me on a phone call",
    "What does Section 154 of CrPC say?",
    "My neighbour cheated me of money"
]

for query in test_queries:
    intent = classify_intent(query)
    print(f"QUERY: {query}")
    print(f"INTENT: {intent.name}")
    print("-" * 60)
