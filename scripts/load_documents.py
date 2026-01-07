import json
from langchain_core.documents import Document

def load_documents(json_path):
    docs = []
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        content = f"""
{item['identifier']} — {item['title_or_term']}

{item['bare_text']}

Explanation:
{item['plain_english_explanation']}
"""
        metadata = {
            "law_type": item["law_type"],
            "identifier": item["identifier"],
            "source": item["source"]
        }

        docs.append(
            Document(
                page_content=content.strip(),
                metadata=metadata
            )
        )

    return docs
