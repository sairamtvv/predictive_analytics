import jugaad_data as jd
import yfinance as yf

from jugaad_data.nse import NSELive
from jugaad_data.nse import stock_df

import traceback

import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta
from jugaad_data.nse import index_raw


import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

class DataFetcher():
    def __init__(self, symbol, n_years=0, n_months =0 , n_days=0, to_date=datetime.date.today(), from_date=datetime.date.today()):

        time_diff =  to_date - from_date

        if time_diff.days==0 and (n_years+n_months+n_days) !=0:
            self.n_years = n_years
            self.to_date = datetime.date.today()
            self.from_date = self.to_date - relativedelta(years=n_years, months=n_months, days=n_days)
            print(self.from_date, self.to_date)
        elif time_diff.days!=0 and n_years == 0:
            self.to_date = self.to_date
            self.from_date = from_date


        self.symbol = symbol



          # Parameter for historical years


    def convert_to_date(self, date_str):
        date_obj = datetime.datetime.strptime(date_str, '%d %b %Y')
        return date_obj


    def get_historical_index_data_with_juggad(self, plot=True):
        # Fetch the index data

        #todo:remove the folder that is made in .cache folder /home/sai/.cache

        raw_index_data = index_raw(symbol="NIFTY 50", from_date=self.from_date, to_date=self.to_date)

        # Converting into dataframe and processing the data
        nifty_historical_df = (pd.DataFrame(raw_index_data) \
                           .assign(
            HistoricalDate=lambda x: x['HistoricalDate'].apply(self.convert_to_date)) \
                           .sort_values('HistoricalDate') \
                           .drop_duplicates() \
                           .loc[lambda x: x['Index Name'] == 'Nifty 50'] \
                           .reset_index(drop=True))


        if plot:
            self.plot_nify_data(nifty_historical_df)

        return nifty_historical_df



    def plot_nify_data(self, nifty_historical_df):
        plt.figure(figsize=(12, 6))

        nifty_historical_df['CLOSE'] = nifty_historical_df['CLOSE'].astype('float')

        # Plot the historical Nifty data
        plt.plot(nifty_historical_df['HistoricalDate'].values,
              nifty_historical_df['CLOSE'].values)

        # Calculate and plot the trend line
        x_values = np.arange(len(nifty_historical_df)).reshape(-1, 1)
        y_values = nifty_historical_df['CLOSE'].values.reshape(-1, 1)
        regressor = LinearRegression().fit(x_values, y_values)
        trend_line = regressor.predict(x_values)
        plt.plot(nifty_historical_df['HistoricalDate'].values, trend_line, linestyle='--',
              color='g', label='Trend Line')

        # Set the title and labels
        plt.title('Nifty Index')
        plt.xlabel('Date')
        plt.ylabel('Closing Price')
        plt.legend()

        # Show the plot
        plt.tight_layout()
        plt.show()

    def get_info_on_index_last_price_juggad(self):
        n = NSELive()
        if self.symbol == "NIFTY 50":
            data = n.live_index('NIFTY 50')
        else:
            data = n.stock_quote(self.symbol)
        print(data['name'], data['timestamp'], data['data'][0]['lastPrice'])

    def get_stock_data_with_juggad(self, series="EQ"):
        """ Only for equity for now """
        df = stock_df(symbol=self.symbol,
                            from_date=self.from_date,
                            to_date=self.to_date,
                            series=series)
        return df


    def fetch_data(self):

        if self.symbol == "NIFTY 50":
            try:
                df = self.get_historical_index_data_with_juggad()
                df.rename(columns={"HistoricalDate":"DATE"}, inplace=True)
                return df
            except Exception as er:
                print(er)
        #if it is any other stock
        else:
            try:
                df = self.get_stock_data_with_juggad()
                return df
            except:
                print("trace for error from jugad and now tryingto fetch data using yahoo finance..")
                traceback.print_exc()
                try:
                    df= self.fetch_data_using_yfinance()
                    return df
                except Exception as er:
                    print(er)











    def fetch_data_using_yfinance(self):
        yfinance_symbol = self.symbol + ".NS"

        # end date data is excluded
        stock_data = yf.download(yfinance_symbol, start='2023-01-01', end='2023-01-06')
        info = yf.Ticker(yfinance_symbol).info
        print(f"info for {self.symbol} from yfinance")

        print(info['sharesOutstanding'], info['floatShares'], info['currentPrice'])

        return stock_data




if __name__ == "__main__":
    #data_fetcher_obj = DataFetcher(symbol="NIFTY 50", n_years=3)
    data_fetcher_obj = DataFetcher(symbol="TATAMOTORS", n_years=3)
    df = data_fetcher_obj.fetch_data()
    print(df)


