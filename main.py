from fetch_data.fetch_indian_stocks import DataFetcher
#
# df = get_stock_data("JFC", "2018-01-01", "2019-01-01")
# print(df.head())

data_fetcher_obj = DataFetcher(symbol="ASIANPAINT", n_years=1)
df = data_fetcher_obj.fetch_data()
df.rename(columns={"DATE":"dt", "CLOSE":"close"}, inplace =True)
df = df[["dt","close"]]
df.set_index("dt", inplace=True)