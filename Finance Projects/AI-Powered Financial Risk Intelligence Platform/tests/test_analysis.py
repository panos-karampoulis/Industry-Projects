from app.company import get_company_profile
from app.analysis import generate_company_report


symbol = "MSFT"


profile = get_company_profile(symbol)


report = generate_company_report(profile)


print("\nCOMPANY SUMMARY")
print(report["company_summary"])


print("\nVALUATION")
print(report["valuation"])


print("\nRISK PROFILE")
print(report["risk_profile"])