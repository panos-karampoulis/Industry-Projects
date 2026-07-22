from app.config import FMP_API_KEY

print("KEY LENGTH:", len(FMP_API_KEY))
print("KEY START:", FMP_API_KEY[:5])


from app.company import (
    get_company_profile,
    get_stock_quote
)


symbol = "MSFT"


profile = get_company_profile(symbol)

quote = get_stock_quote(symbol)


print("COMPANY PROFILE")
print(profile[0])


print("\nQUOTE")
print(quote[0])