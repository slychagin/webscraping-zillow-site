from data_manager import DataManager
from sheet_manager import SheetManager

parser = DataManager()

input_page_count = int(input(f"Zillow ran {parser.get_page_count()} pages with 40 rental ads per page."
                             f"How many pages to save in a file? "))
parser.get_data(input_page_count)
parser.get_addresses()
parser.get_prices()
parser.get_house_links()
total_list = list(zip(parser.addresses, parser.prices, parser.house_links))
print(list(total_list))


sheet_creator = SheetManager()

for (address, price, link) in total_list:
    sheet_creator.fill_sheet(address, price, link)
