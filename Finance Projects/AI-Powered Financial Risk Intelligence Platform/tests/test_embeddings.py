from app.document_loader import load_pdf
from app.text_splitter import split_text

from app.embeddings import generate_embeddings
from app.vector_store import create_vector_store



def build_company_vectorstore(
    company
):


    file = (
        f"documents/{company}/"
        f"{company}_annual_report.pdf"
    )


    print(
        f"Loading document: {file}"
    )


    text = load_pdf(
        file
    )


    chunks = split_text(
        text
    )


    print(
        "Chunks created:",
        len(chunks)
    )


    embeddings = generate_embeddings(
        chunks
    )


    print(
        "Embedding shape:",
        embeddings.shape
    )


    create_vector_store(
        embeddings,
        chunks,
        company=company
    )


    print(
        f"{company.upper()} vector database created!"
    )




if __name__ == "__main__":


    build_company_vectorstore(
        "microsoft"
    )