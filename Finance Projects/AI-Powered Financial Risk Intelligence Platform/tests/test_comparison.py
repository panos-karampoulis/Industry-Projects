from app.comparison import compare_companies


companies = [
    "MSFT",
    "NVDA",
    "AAPL"
]


df = compare_companies(
    companies
)


print(df)