import json
import requests
from urllib.parse import parse_qs, urlparse
from bs4 import BeautifulSoup
from input_data import FIRST_PAGE_URL, HEADERS, change_url


class DataManager:

    def __init__(self):
        self.house_links = []
        self.addresses = []
        self.prices = []
        self.data = []
        self.params = parse_qs(urlparse(FIRST_PAGE_URL).query)

    def get_page_count(self):
        response = requests.get(FIRST_PAGE_URL, headers=HEADERS, params=self.params).text
        soup = BeautifulSoup(response, "html.parser")
        ads_count = int(soup.find("span", class_="result-count").text.split(" ")[0])
        number_ads_per_page = 40
        if ads_count % number_ads_per_page == 0:
            count_pages = ads_count / number_ads_per_page
        else:
            count_pages = ads_count // number_ads_per_page + 1
        return count_pages

    def get_data(self):
        # for page in range(1, self.get_page_count() + 1)
        for page in range(1, 3):
            response = requests.get(change_url(page), headers=HEADERS).text
            soup = BeautifulSoup(response, "html.parser")
            self.data.append(json.loads(soup.select_one("script[data-zrr-shared-data-key]").contents[0].strip("!<>-")))

    def get_house_links(self):
        for data_block in self.data:
            links = [result["detailUrl"] for result in data_block["cat1"]["searchResults"]["listResults"]]
            formatted_links = [link.replace(link, "https://www.zillow.com" + link) if not link.startswith("http") else link for link in links]
            self.house_links.extend(formatted_links)

    def get_addresses(self):
        for data_block in self.data:
            address = [result["address"] for result in data_block["cat1"]["searchResults"]["listResults"]]
            self.addresses.extend(address)

    def get_prices(self):
        for data in self.data:
            for result in data["cat1"]["searchResults"]["listResults"]:
                if "units" in result:
                    self.prices.append(int(result["units"][0]["price"].strip("$+/mo").replace(",", "")))
                else:
                    self.prices.append(int(result["price"].strip("$+/mo").replace(",", "")))


if __name__ == "__main__":
    data_parser = DataManager()
    data_parser.get_data()
    data_parser.get_house_links()
    data_parser.get_addresses()
    data_parser.get_prices()
    print(data_parser.prices)
