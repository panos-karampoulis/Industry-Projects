from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


def create_research_report(
        filename,
        company,
        signal,
        probability,
        quality,
        risk,
        valuation,
        summary
):

    doc = SimpleDocTemplate(
        filename
    )


    styles = getSampleStyleSheet()

    story = []


    story.append(
        Paragraph(
            "AI Investment Research Report",
            styles["Title"]
        )
    )


    story.append(
        Spacer(1,20)
    )


    # Company Overview

    story.append(
        Paragraph(
            "Company Overview",
            styles["Heading2"]
        )
    )


    story.append(
        Paragraph(
            f"""
            Company: {company.get('companyName','')}
            <br/>
            Symbol: {company.get('symbol','')}
            <br/>
            Sector: {company.get('sector','')}
            <br/>
            Industry: {company.get('industry','')}
            """,
            styles["BodyText"]
        )
    )


    story.append(
        Spacer(1,15)
    )


    # Recommendation

    story.append(
        Paragraph(
            "AI Model Prediction",
            styles["Heading2"]
        )
    )


    story.append(
        Paragraph(
            f"""
            Recommendation: {signal}
            <br/>
            Model Confidence: {probability:.1%}
            """,
            styles["BodyText"]
        )
    )


    story.append(
        Spacer(1,15)
    )


    # Scores

    story.append(
        Paragraph(
            "Investment Scores",
            styles["Heading2"]
        )
    )


    story.append(
        Paragraph(
            f"""
            Quality Score: {quality}/100
            <br/>
            Risk Score: {risk}/100
            <br/>
            Valuation Score: {valuation}/100
            """,
            styles["BodyText"]
        )
    )


    story.append(
        Spacer(1,15)
    )


    # Thesis

    story.append(
        Paragraph(
            "Investment Thesis",
            styles["Heading2"]
        )
    )


    story.append(
        Paragraph(
            summary.replace(
                "\n",
                "<br/>"
            ),
            styles["BodyText"]
        )
    )


    story.append(
        Spacer(1,15)
    )


    story.append(
        Paragraph(
            "Conclusion",
            styles["Heading2"]
        )
    )


    story.append(
        Paragraph(
            """
            This report combines machine learning prediction,
            fundamental analysis and explainable AI insights.
            """,
            styles["BodyText"]
        )
    )


    doc.build(
        story
    )