import sys
import os


# ============================================================
# ADD PROJECT ROOT TO PYTHON PATH
# ============================================================

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)



from src.config.countries import (
    get_active_countries
)


from src.data_loader.market_downloader import (
    MarketDownloader
)




# ============================================================
# MAIN PIPELINE
# ============================================================


def run_pipeline():


    countries = get_active_countries()


    print("\n")
    print("=" * 70)
    print("EUROPEAN ENERGY MARKET PIPELINE")
    print("=" * 70)


    print(
        "\nACTIVE COUNTRIES:"
    )

    print(
        countries
    )



    results = []



    for country in countries:


        try:


            downloader = MarketDownloader(
                country
            )


            downloader.run()


            results.append({

                "country": country,

                "status": "SUCCESS"

            })



        except Exception as e:


            print("\nERROR:", country)

            print(
                "Exception type:",
                type(e).__name__
            )

            print(
                "Exception details:",
                repr(e)
            )

            results.append({

                "country": country,

                "status": "FAILED",

                "error": str(e)

            })



    print("\n")
    print("=" * 70)
    print("PIPELINE SUMMARY")
    print("=" * 70)



    for result in results:


        print(
            result
        )




# ============================================================
# EXECUTION
# ============================================================


if __name__ == "__main__":


    run_pipeline()