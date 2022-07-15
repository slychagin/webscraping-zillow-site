from data_manager import DataManager
from sheet_manager import SheetManager, save_to_csv

parser = DataManager()

# Ask how many pages need to be parsed.
input_page_count = int(input(f"Zillow ran {parser.get_page_count()} pages with 40 rental ads per page "
                             f"How many pages to save in a file? "))

# Choose where you want to save the data.
save_method = input("Choose how to save a data. Enter 'google' to save to Google sheet, 'csv' - to csv file ").lower()

# Parse the data.
parser.get_data(input_page_count)
parser.get_addresses()
parser.get_prices()
parser.get_house_links()
total_list = list(zip(parser.addresses, parser.prices, parser.house_links))

# Save the data.
if save_method == "google":
    sheet_creator = SheetManager()
    for (address, price, link) in total_list:
        sheet_creator.fill_google_sheet(address, price, link)
else:
    save_to_csv(total_list)
