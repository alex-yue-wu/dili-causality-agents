from crewai.tools import tool
from langchain_community.document_loaders import PyPDFLoader


@tool("PDFReaderTool")
def PDFReaderTool(file_path: str) -> str:
    """Extract text from PDF and return as string."""
    loader = PyPDFLoader(file_path)
    pages = loader.load()

    return "\n".join([page.page_content for page in pages])
