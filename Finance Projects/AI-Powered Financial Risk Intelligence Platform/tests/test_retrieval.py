from app.retrieval import search_documents



query = (
    "What are Amazon AI infrastructure risks?"
)


results = search_documents(
    query,
    top_k=5
)



print(
    "\nSEARCH RESULTS\n"
)


for i, result in enumerate(results):

    print(
        f"\nRESULT {i+1}"
    )

    print(
        "Score:",
        result["score"]
    )


    print(
        result["text"][:500]
    )

    print(
        "-"*80
    )