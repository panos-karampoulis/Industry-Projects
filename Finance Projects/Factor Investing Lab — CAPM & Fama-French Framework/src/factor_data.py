import pandas_datareader.data as web
import pandas as pd



def load_fama_french():

    data = web.DataReader(
        "F-F_Research_Data_Factors_daily",
        "famafrench"
    )


    factors = data[0]


    factors = factors / 100


    factors.index = factors.index.to_timestamp()


    factors = factors.rename(
        columns={
            "Mkt-RF":"MKT_RF",
            "SMB":"SMB",
            "HML":"HML",
            "RF":"RF"
        }
    )


    return factors