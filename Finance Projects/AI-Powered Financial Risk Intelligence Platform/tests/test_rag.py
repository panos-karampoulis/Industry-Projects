from app.rag import ask_financial_assistant



companies = [
    "amazon",
    "microsoft",
    "nvidia"
]


question = (
    "What are the main AI risks?"
)



for company in companies:


    print("\n====================")
    print(company.upper())
    print("====================")


    response = ask_financial_assistant(
        question,
        company
    )


    print("\nANSWER:\n")

    print(
        response["answer"]
    )


    print("\nTOP SOURCES:")

    for source in response["sources"][:3]:

        print(
            source["source_id"],
            source["score"]
        )