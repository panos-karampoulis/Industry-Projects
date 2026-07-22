from src.fama_french import fama_french_regression



def calculate_hml_exposures(
    returns,
    factors
):

    hml_betas = {}


    for asset in returns.columns:

        try:

            result = fama_french_regression(
                returns[asset],
                factors
            )


            hml_betas[asset] = (
                result["HML Beta"]
            )


        except Exception:

            continue


    return hml_betas