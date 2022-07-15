import time
from data_manager import DataManager
from sheet_manager import SheetManager, save_to_csv

parser = DataManager()

input_page_count = int(input(f"Zillow ran {parser.get_page_count()} pages with 40 rental ads per page "
                             f"How many pages to save in a file? "))
save_method = input("Choose how to save a data. Enter 'google' to save to Google sheet, 'csv' - to csv file ").lower()

start_parsing = time.perf_counter()

parser.get_data(input_page_count)
parser.get_addresses()
parser.get_prices()
parser.get_house_links()
total_list = list(zip(parser.addresses, parser.prices, parser.house_links))

if save_method == "google":
    sheet_creator = SheetManager()
    for (address, price, link) in total_list:
        sheet_creator.fill_google_sheet(address, price, link)
else:
    save_to_csv(total_list)

end_parsing = time.perf_counter()

total_time = end_parsing - start_parsing
print(total_time)
