import json
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource


def pdf_knowledge_source_init(context):
    '''Initialize a PDF knowledge source'''
    # Access crew inputs
    pdf_path = context.get("inputs", {}).get("input_pdf")
    print(f"{pdf_path=}")
    if not pdf_path:
        raise ValueError("No PDF path provided in crew inputs")

    return PDFKnowledgeSource(file_path=pdf_path)


def save_as_json(content: dict, filename: str):
    """Save content to a json file."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(content, file)

    print(f"✅ Saved output to {filename}")


def save_as_markdown(content: str, filename: str):
    """Save content to a markdown file, assuming text-like output."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(str(content))

    print(f"✅ Saved output to {filename}")
