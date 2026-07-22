from app.document_loader import load_pdf


file = (
    "documents/"
    "2026-Annual-Report-Web.pdf"
)


text = load_pdf(file)


print(
    text[:2000]
)