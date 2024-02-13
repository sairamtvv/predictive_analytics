from fetch_data.fetch_indian_stocks import DataFetcher
import talib
import pandas_ta as ta
import pandas as pd

import ta as bta

from sklearn.preprocessing import MinMaxScaler

#to do list get data from the 



#
# df = get_stock_data("JFC", "2018-01-01", "2019-01-01")
# print(df.head())

data_fetcher_obj = DataFetcher(symbol="ASIANPAINT", n_years=1)
df = data_fetcher_obj.fetch_data()
#df.rename(columns={"DATE":"dt", "CLOSE":"close"}, inplace =True)

# Assuming you have a DataFrame named 'df' with the columns you mentioned
# Convert 'DATE' column to datetime
df['DATE'] = pd.to_datetime(df['DATE'])

# Set 'DATE' column as index
df.set_index('DATE', inplace=True)

# If your data is not already sorted by date, sort it
df.sort_index(inplace=True)

# Set the frequency if needed (for example, daily frequency)
#df = df.asfreq('D')

# Calculate Weighted Moving Average (WMA)
period_wma = 14
df['WMA'] = ta.wma(df['CLOSE'], length=period_wma)

# Calculate Relative Strength Index (RSI)
period_rsi = 14
df['RSI'] = ta.rsi(df['CLOSE'], length=period_rsi)


# Calculate Volume Weighted Average Price (VWAP)
df['VWAP'] = ta.vwap(df['HIGH'], df['LOW'], df['CLOSE'], df['VOLUME'])

# Calculate Average True Range (ATR)
period_atr = 14
df['ATR'] = ta.atr(df['HIGH'], df['LOW'], df['CLOSE'], length=period_atr)

# Printing the DataFrame with added indicators
# print(df.head())

# Drop the first 14 rows
df = df.iloc[14:]


# Columns to be scaled
columns_to_scale = [ 'CLOSE', "WMA", 'VWAP', "RSI", "ATR", ]

# Initialize MinMaxScaler
scaler = MinMaxScaler()

# Fit scaler on the data and transform the specified columns
df[columns_to_scale] = scaler.fit_transform(df[columns_to_scale])

# Printing the DataFrame with scaled columns
print(df)


# class FeatureEngineer():
#     #WMA, RSI, VWAP, ATR,
#     def __int__(self, df):
#         self.df = df






