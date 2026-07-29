import os
import pandas as pd



class ChunkManager:


    def __init__(
            self,
            base_path,
            dataset_name
    ):


        self.base_path = base_path

        self.dataset_name = dataset_name


        self.dataset_dir = os.path.join(

            base_path,

            dataset_name

        )


        os.makedirs(

            self.dataset_dir,

            exist_ok=True

        )



    # ======================================================
    # YEAR RANGE
    # ======================================================


    def get_years(
            self,
            start_year,
            end_year
    ):


        return list(

            range(

                start_year,

                end_year + 1

            )

        )



    # ======================================================
    # FILE PATH
    # ======================================================


    def get_chunk_file(
            self,
            year
    ):


        return os.path.join(

            self.dataset_dir,

            f"{self.dataset_name}_{year}.csv"

        )



    # ======================================================
    # CHECK EXISTENCE
    # ======================================================


    def exists(
            self,
            year
    ):


        return os.path.exists(

            self.get_chunk_file(year)

        )



    # ======================================================
    # SAVE YEAR
    # ======================================================


    def save(
            self,
            df,
            year
    ):


        path = self.get_chunk_file(

            year

        )


        df.to_csv(

            path,

            index=False

        )


        print(

            f"Saved chunk: {path}"

        )



    # ======================================================
    # LOAD CHUNKS
    # ======================================================


    def merge(self):


        files = sorted([

            f

            for f in os.listdir(

                self.dataset_dir

            )

            if f.endswith(".csv")

        ])



        if not files:

            return None



        frames = []



        for file in files:


            path = os.path.join(

                self.dataset_dir,

                file

            )


            df = pd.read_csv(

                path,

                parse_dates=[

                    "timestamp"

                ]

            )


            frames.append(df)



        merged = pd.concat(

            frames,

            ignore_index=True

        )


        merged = (

            merged

            .drop_duplicates(

                subset=[

                    "timestamp"

                ]

            )

            .sort_values(

                "timestamp"

            )

            .reset_index(

                drop=True

            )

        )


        return merged