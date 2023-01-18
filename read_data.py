import pandas as pd

def read_data(filename):
        
    # READ DATA:
    dataframe = pd.read_csv(filename, encoding='latin-1', index_col = None)

    # change the column names:
    dataframe = dataframe.rename(columns={'FakeName': 'FullNm', 'FakeMail': 'Email_Address'})

    # Filter Data:

    # Select the date only for 2022
    dataframe = dataframe[dataframe.Booking_Date >= '2022-01-01']

    # Select people who have more than 100 flight
    dataframe['FullNm_count'] = dataframe.groupby('FullNm')['FullNm'].transform('count')
    dataframe = dataframe[dataframe.FullNm_count >= 100]

    nm_of_data = 30
    dataframe = dataframe.groupby('FullNm').head(nm_of_data)
    dataframe = dataframe[['FullNm', 'Email_Address', 'Orig_Airport', 'Dest_Airport']]

    return dataframe