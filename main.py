import json
from urllib.parse import parse_qs, urlparse
import requests
from bs4 import BeautifulSoup


GOOGLE_FORM_LINK = "https://docs.google.com/forms/d/e/1FAIpQLSdZeaipy_AvGN2RgXRysuKObsS_g0l7QJJCshCn3nWR5JlQ0w" \
                   "/viewform?usp=sf_link "
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    "accept-language": "ru-RU"
}
FIRST_PAGE_URL = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"


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
            url = "https://" + f'www.zillow.com/homes/for_rent/1-_beds/{page}_p/?searchQueryState=%7B%22pagination%22%3A%7B%22currentPage%22%3A{page}%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.63417281103516%2C%22east%22%3A-122.23248518896484%2C%22south%22%3A37.662044042279824%2C%22north%22%3A37.88836565815623%7D%2C%22mapZoom%22%3A12%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D'
            response = requests.get(url, headers=HEADERS).text
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

