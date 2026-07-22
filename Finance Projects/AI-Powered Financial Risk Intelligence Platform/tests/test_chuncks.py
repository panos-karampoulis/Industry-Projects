from app.document_loader import load_pdf
from app.text_splitter import split_text



file = (
    "documents/"
    "2026-Annual-Report-Web.pdf"
)


text = load_pdf(file)


chunks = split_text(
    text
)


print(
    "Number of chunks:",
    len(chunks)
)


print("\nFIRST CHUNK\n")

print(
    chunks[0]
)