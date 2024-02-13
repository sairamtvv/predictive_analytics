import json
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import urllib.request

import pathlib



class Scrape:
    def __init__(self, url, headers,soup):
        self.headers = headers
        self.url = url
        self.soup = soup

    # dataframe
    def promoter_pledging(self):
        data = requests.get(self.url, headers=headers)
        soup = BeautifulSoup(data.content, 'html.parser')
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as i:
            html = i.read()
        data = pd.read_html(html)[0]
        data = pd.DataFrame(data)
        return data

    # list
    def brands(self):
        soup = self.soup
        brands = soup.find_all("span", attrs={"class": "badgebrand badgebrand-primary mb-3"})
        brand_list = []
        for brand in brands:
            text = brand.text
            brand_list.append(text)
        return brand_list

    # dict
    def index_presence(self):
        soup = self.soup
        ip = soup.find_all("p", attrs={"class": "mb-1"})
        index_values = soup.find_all("div", attrs={"class": "row no-gutters mt-3 pb-3"})
        index_names = []
        for names in ip:
            new_names = names.text.strip()
            index_names.append(new_names)
        match = re.search(r'\d+(\.\d+)?', index_values[1].text)
        value = match.group(0)
        index_val = []
        for value in index_values:
            value = value.text
            match = re.search(r'\d+(\.\d+)?', value)
            val2 = match.group(0)
            index_val.append(val2)
        dictionary = dict(zip(index_names, index_val))
        return dictionary

    def peer_comparison(self):
        headers = self.headers
        data = requests.get(self.url, headers=headers)
        soup = BeautifulSoup(data.content, 'html.parser')
        req = urllib.request.Request(self.url, headers=headers)
        try:
            with urllib.request.urlopen(req) as response:
                html = response.read()
                data = pd.read_html(html)[0]
                data_df = list(data)
                return data_df
        except urllib.error.HTTPError as e:
            print("HTTPError:", e.code, e.reason)
        except urllib.error.URLError as e:
            print("URLError:", e.reason)
        except ValueError:
           print("ValueError: No tables found in the HTML")
        return None

    # dataframe
    def share_holding_pattern(self):
        headers = self.headers
        data = requests.get(self.url, headers=headers)
        soup = BeautifulSoup(data.content, 'html.parser')
        body = soup.find('tbody')
        tbody = soup.find('tbody')

        # Create an empty list to store the row data
        data_rows = []

        # Iterate over the rows within the 'tbody'
        for row in tbody.find_all('tr'):
            # Create an empty list to store the cell data for each row
            row_data = []

            # Iterate over the cells within each row
            for cell in row.find_all('td'):
                # Extract the data from the cell and append to the row_data list
                data = cell.get_text().strip()
                row_data.append(data)

            # Append the row_data list to the data_rows list
            data_rows.append(row_data)
        # Create a DataFrame from the data_rows list
        df = pd.DataFrame(data_rows)
        # Check if the headers list has the correct length
        header = ['Name', 'No. of Shares', '% Holding']
        if len(df.columns) == len(header):
            # Assign the headers to the DataFrame
            df.columns = header
        else:
            print("Length of headers list does not match the number of columns in the DataFrame.")
        df = df.rename(columns={0: "Name", 1: "No. of Shares", 2: "% Holding"})
        return df

    # dataframe


    def pros_nd_cons_2(self):
        soup = self.soup
        pros_and_cons = soup.find("div", attrs={"id": "mainContent_ProsAndCons"})

        pnc = str(pros_and_cons)

        soup_4 = BeautifulSoup(pnc, 'html.parser')

        limitation = soup_4.find('ul', class_="limitations")


        limit_list = []

        strength = soup_4.find('ul', class_="strength")

        strong_list = []

        for limit in limitation:
            limit = limit.text
            limit_list.append(limit)

        for strong in strength:
            strong = strong.text
            strong_list.append(strong)

        new_limit_list = [value for value in limit_list if value != '\n']
        new_limit_list = pd.DataFrame(new_limit_list).rename(columns={0: "limitations"})

        new_strong_list = [value for value in strong_list if value != '\n']
        new_strong_list = pd.DataFrame(new_strong_list).rename(columns={0: "strenght"})

        cnpdf = pd.concat([new_strong_list, new_limit_list], axis=1)

        return cnpdf

    # dataframe
    def six_tables(self):
        soup = self.soup
        tables = soup.find_all('table', class_='table table-sm table-hover screenertable table-responsive-sm')

        dataframes = []

        for table in tables:
            try:
                headings = []
                for th in table.find('thead').find_all('th'):
                    headings.append(th.text.strip())

                rows = []
                for row in table.find('tbody').find_all('tr'):
                    row_data = []
                    for cell in row.find_all('td'):
                        row_data.append(cell.text.strip())

                    # Adjust the number of columns based on the available data
                    if len(row_data) != len(headings):
                        diff = len(headings) - len(row_data)
                        if diff > 0:
                            row_data.extend([''] * diff)
                        else:
                            row_data = row_data[:len(headings)]

                    rows.append(row_data)

                df = pd.DataFrame(rows, columns=headings)
                dataframes.append(df)

            except Exception as e:
                print(f"An error occurred while fetching the table: {e}")
                pass

        # Print the dataframes or perform other operations with them
        df_list = []
        for df in dataframes:
            df_list.append(df)

        six_tables_particulars = soup.find_all("th", scope="row")


        particulars_list = []

        for i in six_tables_particulars:
            i = i.text
            particulars_list.append(i)


        def replace_first_column_with_list(dataframe, column_name, replacement_list):
            dataframe[column_name] = replacement_list
            return dataframe

        def shift_col(data_id):
            i = len(dataframes[data_id].columns) - 1
            while i in dataframes[data_id].iloc[:, i]:
                dataframes[data_id].iloc[:, i] = dataframes[data_id].iloc[:, i - 1]
                i -= 1
            return dataframes[data_id]#

        dataframes[1] = shift_col(1)
        dataframes[1] = replace_first_column_with_list(dataframes[1],"PARTICULARS",particulars_list[0:11])

        dataframes[2] = shift_col(2)
        dataframes[2] = replace_first_column_with_list(dataframes[2], 'Particulars', particulars_list[22:38])

        dataframes[3] = shift_col(3)
        dataframes[3] = replace_first_column_with_list(dataframes[3], 'PARTICULARS', particulars_list[38:46])


        return df_list

    # list
    def essen(self):
        soup = self.soup
        essen = soup.find_all("div", class_="col-6 col-md-4 compess")
        small_text_list = [tag.text.strip() for tag in essen]
        cleaned_texts = [text.replace('\r\n', '') for text in small_text_list]
        cleaned_texts = [text.replace('\xa0', '') for text in cleaned_texts]
        cleaned_texts = [text.replace('\n', '') for text in cleaned_texts]
        target_width = len(cleaned_texts[1])

        # Adjust the spacing for each extracted text
        adjusted_texts = [text.ljust(target_width) for text in cleaned_texts]
        target_width = len(adjusted_texts[9])

        # Adjust the spacing for each extracted text
        adjusted_texts = [text.ljust(target_width) for text in adjusted_texts]
        cleaned_list = [item.replace(" ", "") for item in adjusted_texts]

        modified_list = [': '.join(item.split()) for item in cleaned_list]
        modified_list_2 = []
        for item in modified_list:
            modified_item = re.sub(r'(\d)', r':\1', item, count=1)
            modified_list_2.append(modified_item)

        modified_list_2.remove('AddYourRatio')
        return modified_list_2

    # dict
    def pc(self):
        soup = self.soup
        pc = soup.find("div", class_="row")
        ratings = soup.find("div", class_="row no-gutters mt-2 ratingdetails")
        soup___ = BeautifulSoup(str(ratings), 'html.parser')
        div_elements = soup___.find_all('div', {'aria-label': True})
        h1_elements = soup___.find_all('h6')
        aria_lables = [div['aria-label'] for div in div_elements]
        titles = []

        for texts in h1_elements:
            item = texts.get_text()
            titles.append(item)

        limited_data = [element[:9] for element in titles]
        dict_rating = {'mainContent_finstarrating': limited_data, 'rating': aria_lables}
        ratios = soup.find('div', class_="row ratiorow")
        soup____5 = BeautifulSoup(str(ratios), 'html.parser')
        values = soup____5.find_all('span', class_="Number")
        durations = soup____5.find_all('span', class_='durationvalue')
        duration = soup____5.find_all('span', class_='duration')
        value_list = []
        duration_list = []
        durations_ = []

        for number in values:
            val = number.get_text()
            value_list.append(val)

        for period in durations:
            time = period.get_text()
            duration_list.append(time)

        for Period in duration:
            time = Period.get_text()
            durations_.append(time)

        div_elements = soup____5.find_all('div', class_='col-12 col-md-3', id=True)
        Main_content_list = []
        for div in div_elements:
            Main_content_list.append(div['id'])

        Names = []
        for id_ in Main_content_list:
            Name = soup____5.find("div", id=id_)
            Names.append(Name)


        name1 = soup____5.find('div', id=Main_content_list)
        h4_tag = soup____5.find_all('h4')
        # h4_string = h4_tag.text.strip()
        h4_texts = []
        for Text in h4_tag:
            string = Text.text.strip()
            h4_texts.append(string)


        dict__ = {"ratios": h4_texts, "values": value_list, "duration_list": duration_list, "durations_": durations_}
        return dict__

    # dataframe
    def cards(self):
        soup = self.soup
        Cards = soup.find_all("div", class_="compess")
        divs = soup.find_all('div', class_='compess')

        # Extract the span IDs
        span_ids = []
        for div in divs:
            span = div.find('span')
            if span and 'id' in span.attrs:
                span_ids.append(span['id'])

        soup___6 = BeautifulSoup(str(Cards), 'html.parser')
        names2 = soup___6.find_all("p")
        test = names2[0].get_text()

        values = []

        for i in names2:
            value = i.get_text()
            value = value.strip('    ').replace('\n', '').replace('\r', '').replace('   ', '')
            # value = value.strip('    ').split('\xa0')
            values.append(value)

        values = values[21:]
        amount = soup.find_all('div', class_="col-5")
        amount_list = []

        for i in amount:
            number__ = i.get_text()
            number__ = number__.strip(' ').replace('\n', '').replace('\r', '').replace('   ', '')
            amount_list.append(number__)

        index_dict = {'name': values, 'amount': amount_list}
        index_dict = pd.DataFrame(index_dict)
        return index_dict

    # dict
    def summary_def(self):
        headers = self.headers
        data = requests.get(self.url, headers=headers)
        soup = BeautifulSoup(data.content, 'html.parser')
        essentials = soup.find_all("div", attrs={"class": "col-12 col-md-6"})

        essentials_list = []
        for div in essentials:
            name = div.find('span', class_='paramname')
            value = div.find('span', class_='paramval')
            essentials_list.append({'name': name, 'value': value})

        essentials_df = pd.DataFrame(essentials_list)
        new_dict = dict(zip(essentials_df['name'], essentials_df['value']))

        return new_dict
#dataframe
    def ratings(self):
        soup = self.soup
        ratings = soup.find("div", class_="row no-gutters mt-2 ratingdetails")
        soup___ = BeautifulSoup(str(ratings), 'html.parser')
        div_elements = soup___.find_all('div', {'aria-label': True})
        h1_elements = soup___.find_all('h6')
        aria_lables = [div['aria-label'] for div in div_elements]
        titles = []

        for texts in h1_elements:
            item = texts.get_text()
            titles.append(item)

        limited_data = [element[:9] for element in titles]
        dict_rating = {'mainContent_finstarrating': limited_data, 'rating': aria_lables}
        dict_rating = pd.DataFrame(dict_rating)
        return dict_rating

    def run(self):
        
        folder_path = str(pathlib.Path(__file__).parent /"data")
        #folder_path = "C:/Users/mehul/PycharmProjects/pythonWEBSCRAPE 2/data/"
        Company = 'BAJAJELEC'#<----   CHANGE HERE AS WELL

        df = self.promoter_pledging()
        df.to_csv(f"{folder_path}promoter_pledging_{Company}.csv")
        print("promoter pledging data saved successfully....")

        brand_list = self.brands()
        dict_brand_list = {'brand':brand_list}
        df_dict_brand_list = pd.DataFrame(dict_brand_list)
        df_dict_brand_list.to_csv(f"{folder_path}brand_list_{Company}.csv")
        print("brand list data saved successfully....")

        modified_list_2 = self.essen()
        modified_list_2 = pd.DataFrame(modified_list_2)
        modified_list_2.to_csv(f"{folder_path}essentials_List_2_{Company}.csv")
        print("essentials data saved successfully....")

        df = self.share_holding_pattern()
        df.to_csv(f"{folder_path}share_holding_pattern_{Company}.csv")
        print("share holding pattern saved successfully....")

        dictionary = self.index_presence()
        #dictionary_df = pd.DataFrame(dictionary)
        #dictionary_df.to_csv(f"C:/Users/mehul/PycharmProjects/pythonWEBSCRAPE 2/index_presence_{Company}.csv")
        with open(f'{folder_path}index_presence_{Company}.json', 'w') as fp:
            json.dump(dictionary, fp)
        print("index presence saved successfully....")


        df_list = self.six_tables()
        df_list[0].index.rename('Quarterly Results', inplace=True)
        df_list[1].index.rename('P and L', inplace=True)
        df_list[2].index.rename('Balance Sheet', inplace=True)
        df_list[3].index.rename('Cash Flow', inplace=True)
        df_list[4].index.rename('Promoter Details', inplace=True)
        df_list[5].index.rename('Investor Details', inplace=True)

        for i in df_list:
            i.to_csv(f"{folder_path}{Company}_{i.index.name}.csv")
            print(f"{i.index.name} saved successfully....")

        print("tabular data saved successfully....")


        dict__ = self.pc()
        with open(f'{folder_path}pc_{Company}.json', 'w') as fp:
            json.dump(dictionary, fp)
        print("index-peer saved successfully....")

        index_dict = self.cards()
        index_dict = index_dict.to_csv(f"{folder_path}cards_{Company}.csv")
        print("cards saved successfully....")

        new_dict = self.summary_def()
       # with open(f'{folder_path}summary_def_{Company}.json', 'w') as fp:
        #    json.dump(dictionary, fp)
        #print("overall-summary saved successfully....")

        dict_rating = self.ratings()
        dict_rating.to_csv(f"{folder_path}rating_{Company}.csv")
        print("ratings saved successfully....")

        cnpd_2 = self.pros_nd_cons_2()
        cnpd_2.to_csv(f"{folder_path}pcnd_{Company}.csv")
        print("pros and cons saved successfully.....")

        return True





# run = Scrape(url)

if __name__ == "__main__":
    Company = 'BAJAJELEC'####<---------change here
    url = f"https://ticker.finology.in/company/{Company}"
    headers = ({'User-Agent':
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 OPR/98.0.0.0 (Edition std-1)',
               'Accept-Language': 'en-US, en;q=0.5'})
    data = requests.get(url, headers)
    soup = BeautifulSoup(data.content, 'html.parser')

    scraper = Scrape(url, headers,soup)
    scraper.run()
    print(url)