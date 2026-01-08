from dotenv import load_dotenv
load_dotenv()

from retriever import get_retriever
from context_builder import build_context
from system_prompt import LEGAL_QA_SYSTEM_PROMPT
from langchain_openai import ChatOpenAI

from document_selector import select_document
from document_templates import DOCUMENT_TEMPLATES
from intent_router import classify_intent, QueryIntent

# Phase 1 + Phase 2 + Phase 3 imports
from query_quality import is_vague_query
from clarification import get_clarification_question
from response_formatter import format_response


# -------------------------------------------------
# Procedural & advice refusal messages
# -------------------------------------------------
PROCEDURAL_REFUSAL_MESSAGE = (
    "This system provides legal information only. "
    "It does not provide procedural guidance or instructions."
)

ADVICE_REFUSAL_MESSAGE = (
    "This system provides general legal information only. "
    "It cannot predict outcomes or give legal advice."
)


# -------------------------------------------------
# Utility: Deterministic document renderer
# -------------------------------------------------
def render_document_template(template: dict) -> str:
    """
    Converts structured document information into a natural,
    narrative-style explanation while remaining deterministic and safe.
    """

    return f"""
{template['what_it_is']}

This document exists to address a specific legal need. 
{template['why_it_exists']}

In practice, it is typically relevant in situations such as the following.
{template['when_it_is_used']}

It is also important to be clear about its limitations.
{template['what_it_does_not_do']}
""".strip()


# -------------------------------------------------
# Document type detection
# -------------------------------------------------
def detect_document_type(query: str) -> str | None:
    query = query.lower().strip()

    DOCUMENT_MAP = {
        "fir": ["fir", "first information report"],
        "rti": ["rti", "right to information"],
        "bail": ["bail", "bail application", "anticipatory bail"],
        "legal_notice": ["legal notice"]
    }

    for doc_key, keywords in DOCUMENT_MAP.items():
        for kw in keywords:
            if kw in query:
                return doc_key

    return None


# -------------------------------------------------
# Document Explanation Handler (PHASE 3 WRAPPED)
# -------------------------------------------------
def handle_document_explanation(user_query: str) -> str:
    document_key = detect_document_type(user_query)

    if not document_key or document_key not in DOCUMENT_TEMPLATES:
        return "The information is not available in the current legal knowledge base."

    raw_explanation = render_document_template(
        DOCUMENT_TEMPLATES[document_key]
    )

    return format_response(
        title=DOCUMENT_TEMPLATES[document_key]["title"],
        explanation=raw_explanation,
        note="This is general legal information, not legal advice."
    )


def handle_document_selection(user_query: str) -> str:
    selection = select_document(user_query)

    if not selection:
        return "The information is not available in the current legal knowledge base."

    explanation = (
        f"{selection['document']}\n\n"
        f"{selection['reason']}"
    )

    return format_response(
        title="Suggested Document",
        explanation=explanation,
        note="This is indicative guidance only and not legal advice."
    )



# -------------------------------------------------
# MAIN ENTRY POINT
# -------------------------------------------------
def answer_query(user_query: str) -> str:
    # ---------------------------------------------
    # Phase 2: Single-turn clarification for vague queries
    # ---------------------------------------------
    vague_check = is_vague_query(user_query)

    if vague_check["is_vague"]:
        return get_clarification_question(vague_check["reason"])

    # ---------------------------------------------
    # Intent classification (only if NOT vague)
    # ---------------------------------------------
    intent = classify_intent(user_query)

    # 🚫 BLOCK PROCEDURAL QUERIES
    if intent == QueryIntent.PROCEDURAL:
        return PROCEDURAL_REFUSAL_MESSAGE

    # 🚫 BLOCK ADVICE / OUTCOME QUERIES
    if intent == QueryIntent.ADVICE:
        return ADVICE_REFUSAL_MESSAGE

    # ✅ Document explanation
    if intent == QueryIntent.DOCUMENT_EXPLANATION:
        return handle_document_explanation(user_query)

    # ✅ Document selection
    if intent == QueryIntent.DOCUMENT_SELECTION:
        return handle_document_selection(user_query)

    # -------------------------------------------------
    # Day-1 RAG behaviour (pure legal info)
    # -------------------------------------------------
    retriever = get_retriever()
    docs = retriever.invoke(user_query)

    if not docs:
        return "The information is not available in the current legal knowledge base."

    context = build_context(docs)

    if not context.strip():
        return "The information is not available in the current legal knowledge base."

    llm = ChatOpenAI(
    model="meta-llama/Llama-3.1-8B-Instruct",
    temperature=0.25
    )


    messages = [
        {"role": "system", "content": LEGAL_QA_SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"""
Legal Context:
{context}

Question:
{user_query}
"""
        }
    ]

    response = llm.invoke(messages)

    return format_response(
        title="Legal Information",
        explanation=response.content,
        note="This is general legal information, not legal advice."
    )

