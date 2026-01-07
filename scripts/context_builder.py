def build_context(docs):
    """
    Convert retrieved documents into a clean, labeled context string
    that can be safely passed to the LLM.
    """

    if not docs:
        return ""

    context_blocks = []

    for idx, doc in enumerate(docs, start=1):
        block = f"""
[Source {idx}]
{doc.page_content}
"""
        context_blocks.append(block.strip())

    return "\n\n".join(context_blocks)
