from threading import Thread

from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import urllib.request
import json
import sys


url = "https://ticker.finology.in/company/RELIANCE"
header = ({'User-Agent':
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 OPR/98.0.0.0 (Edition std-1)',
           'Accept-Language': 'en-US, en;q=0.5'})
data = requests.get(url, header)
soup = BeautifulSoup(data.content, 'html.parser')



class Scrape:
    def __init__(self, url):
        self.url = url

    def Promoter_Pledging (self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 OPR/98.0.0.0 (Edition std-1)',
            'Accept-Language': 'en-US, en;q=0.5'
        }
        data = requests.get(self.url, headers=headers)
        soup = BeautifulSoup(data.content, 'html.parser')


        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as i:
            html = i.read()

        data = pd.read_html(html)[0]
        data.df = pd.DataFrame(data)

        return data.df

    def Brands(self):
        brands = soup.find_all("span", attrs={"class": "badgebrand badgebrand-primary mb-3"})
        brand_list = []
        for brand in brands:
            text = brand.text
            brand_list.append(text)
        return brand_list
    def index_presence(self):
        ip = soup.find_all("p",attrs={"class":"mb-1"})
        index_values = soup.find_all("div", attrs={"class": "row no-gutters mt-3 pb-3"})

        index_names = []

        for names in ip:
            new_names = names.text.strip()
            index_names.append(new_names)

        match = re.search(r'\d+(\.\d+)?', index_values[1].text)
        value = match.group(0)
        print(value)

        index_val = []

        for value in index_values:
            value = value.text
            match = re.search(r'\d+(\.\d+)?', value)
            val2 = match.group(0)
            index_val.append(val2)

        dictionary = dict(zip(index_names, index_val))

        return dictionary


        def index_presence(self):
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 OPR/98.0.0.0 (Edition std-1)',
                'Accept-Language': 'en-US, en;q=0.5'
            }
            data = requests.get(self.url, headers=headers)
            soup = BeautifulSoup(data.content, 'html.parser')
            ip = soup.find_all("p", attrs={"class": "mb-1"})
            index_values = soup.find_all("div", attrs={"class": "row no-gutters mt-3 pb-3"})

            index_names = []

            for names in ip:
                new_names = names.text.strip()
                index_names.append(new_names)

            match = re.search(r'\d+(\.\d+)?', index_values[1].text)
            value = match.group(0)
            print(value)

            index_val = []

            for value in index_values:
                value = value.text
                match = re.search(r'\d+(\.\d+)?', value)
                val2 = match.group(0)
                index_val.append(val2)

            dictionary = dict(zip(index_names, index_val))

            return dictionary

    def peer_comparison(self):
        headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 OPR/98.0.0.0 (Edition std-1)',
                'Accept-Language': 'en-US, en;q=0.5'
        }
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

    def share_holding_pattern(self):
        headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 OPR/98.0.0.0 (Edition std-1)',
                'Accept-Language': 'en-US, en;q=0.5'
         }
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

            # Print the resulting DataFrame
            print(df)

            df = df.rename(columns={0: "Name", 1: "No. of Shares", 2: "% Holding"})
            return df
    def pros_nd_cons(self):
        pros_and_cons = soup.find("div", attrs={"id": "mainContent_ProsAndCons"})

        pnc = str(pros_and_cons)

        soup_4 = BeautifulSoup(pnc, 'html.parser')

        limitation = soup_4.find('ul', class_="limitations")
        limitation

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

    def six_tables(self):
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

        return df_list

    def essen(self):
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

    def pc(self):
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

        Main_content_list

        Names = []
        for id_ in Main_content_list:
            Name = soup____5.find("div", id=id_)
            Names.append(Name)
        Main_content_list

        name1 = soup____5.find('div', id=Main_content_list)
        h4_tag = soup____5.find_all('h4')
        # h4_string = h4_tag.text.strip()

        h4_texts = []

        for Text in h4_tag:
            string = Text.text.strip()
            h4_texts.append(string)

        h4_texts

        dict__ = {"ratios": h4_texts, "values": value_list, "duration_list": duration_list, "durations_": durations_}
        return dict__

    def cards(self):
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

        values

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

    def summary_def(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 OPR/98.0.0.0 (Edition std-1)',
            'Accept-Language': 'en-US, en;q=0.5'
        }
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


    def ratings(self):
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

    def brands(self):
        brands = soup.find_all("span", attrs={"class": "badgebrand badgebrand-primary mb-3"})

        brand_list = []
        for brand in brands:
            text = brand.text
            brand_list.append(text)

        return brand_list
    def find_name(self):
        name = soup.find("span",attrs={"class":"h1 font-weight-bold"})
        name = name.get_text()
        return name

    '''def runall(self):
        if __name__ == '__main__':

            #list isnt callable
            Thread(target=self.brands()).start()
            Thread(target=self.cards()).start()
            Thread(target=self.summary_def()).start()
            Thread(target=self.summary()).start()
            Thread(target=self.Branches()).start()
            Thread(target=self.peer_comparison()).start()
            Thread(target=self.essen()).start()'''
            





#run = Scrape(url)

url = "https://ticker.finology.in/company/RELIANCE"


scraper = Scrape(url)

name = scraper.find_name()
print(name)

Promoter_Pledging = scraper.Promoter_Pledging()

print(Promoter_Pledging )

branch_list = scraper.Brands()
print(branch_list)



index_presence = scraper.index_presence()
print(index_presence)

peer_comparison = scraper.peer_comparison()
print(peer_comparison)

share_holding_pattern = scraper.share_holding_pattern()
print(share_holding_pattern)

print(type(share_holding_pattern))
cnpdf = scraper.pros_nd_cons()
print(cnpdf)
six_tables = scraper.six_tables()
print(six_tables)
essen = scraper.essen()
print('essen')
print(essen)
pc = scraper.pc()
print(pc)
print("\ncards")
cards = scraper.cards()
print(cards)
ratings = scraper.ratings()
print(ratings)

print("summary_def")
summary_def = scraper.summary_def()
print(summary_def)
brands = scraper.brands()
print(brands)




