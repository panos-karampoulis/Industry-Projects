import pandas as pd


from src.config.settings import (
    HISTORICAL_START_DATE,
    get_current_date,
    RAW_DATA_DIR
)


from src.config.countries import (
    get_country_config
)


from src.data_loader.base_downloader import (
    BaseDownloader
)


from src.data_loader.chunk_manager import (
    ChunkManager
)


from src.data_loader.entsoe_client import (
    EntsoeClient
)


from src.data_loader.validator import (
    validate_dataframe
)




class MarketDownloader(BaseDownloader):



    def __init__(
            self,
            country
    ):


        config = get_country_config(
            country
        )


        super().__init__(
            country,
            config
        )


        self.client = EntsoeClient()



        self.load_chunks = ChunkManager(

            self.country_dir,

            "load"

        )


        self.price_chunks = ChunkManager(

            self.country_dir,

            "prices"

        )




    # =====================================================
    # YEAR GENERATOR
    # =====================================================


    def get_years(self):


        start_year = int(

            HISTORICAL_START_DATE[:4]

        )


        end_year = int(

            get_current_date()[:4]

        )


        return range(

            start_year,

            end_year + 1

        )




    # =====================================================
    # YEAR DATES
    # =====================================================


    def get_year_dates(
            self,
            year
    ):


        start = pd.Timestamp(
            f"{year}-01-01"
        )


        current_date = pd.Timestamp(
            get_current_date()
        )


        if year == current_date.year:

            end = current_date


        else:

            end = pd.Timestamp(
                f"{year}-12-31"
            )


        return start, end




    # =====================================================
    # DOWNLOAD LOAD CHUNKS
    # =====================================================


    def download_load(self):


        for year in self.get_years():


            if self.load_chunks.exists(year):


                print(

                    f"Load {year} exists - skipping"

                )

                continue



            print(

                f"Downloading load {year}"

            )


            start, end = self.get_year_dates(

                year

            )



            df = self.client.get_load_data(

                self.country,

                start,

                end

            )



            validate_dataframe(

                df,

                f"{self.country} load {year}"

            )



            self.load_chunks.save(

                df,

                year

            )




        merged = self.load_chunks.merge()



        if merged is not None:


            self.save_csv(

                merged,

                "load.csv"

            )




    # =====================================================
    # DOWNLOAD PRICES CHUNKS
    # =====================================================


    def download_prices(self):


        for year in self.get_years():


            if self.price_chunks.exists(year):


                print(

                    f"Prices {year} exists - skipping"

                )

                continue



            print(

                f"Downloading prices {year}"

            )



            start, end = self.get_year_dates(

                year

            )



            df = self.client.get_day_ahead_prices(

                self.country,

                start,

                end

            )



            validate_dataframe(

                df,

                f"{self.country} prices {year}"

            )



            self.price_chunks.save(

                df,

                year

            )



        merged = self.price_chunks.merge()



        if merged is not None:


            self.save_csv(

                merged,

                "day_ahead_prices.csv"

            )




    # =====================================================
    # RUN
    # =====================================================


    def run(self):


        print("\n")
        print("="*70)
        print(

            self.country.upper()

        )
        print("="*70)



        self.download_load()



        self.download_prices()



        print(

            f"{self.country} completed"

        )