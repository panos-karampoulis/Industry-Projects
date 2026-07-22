import os
from dotenv import load_dotenv


load_dotenv()


def generate_llm_analysis(
    company_name,
    signal,
    probability,
    quality_score,
    risk_score,
    valuation_score,
    fallback_summary
):

    api_key = os.getenv(
        "OPENAI_API_KEY"
    )


    # Αν δεν υπάρχει API key,
    # χρησιμοποιούμε το υπάρχον summary

    if not api_key:

        return fallback_summary


    try:

        from openai import OpenAI


        client = OpenAI(
            api_key=api_key
        )


        prompt = f"""

You are an equity research analyst.

Analyze this company:

Company:
{company_name}

AI Recommendation:
{signal}

Model Confidence:
{probability:.1%}

Quality Score:
{quality_score}/100

Risk Score:
{risk_score}/100

Valuation Score:
{valuation_score}/100


Write a professional investment research summary.

Include:

1. Investment Thesis
2. Main Strengths
3. Key Risks
4. Final Conclusion

Keep it concise and professional.

"""


        response = client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=[
                {
                    "role":"user",
                    "content":prompt
                }
            ],

            temperature=0.3
        )


        return response.choices[0].message.content



    except Exception:

        return fallback_summary