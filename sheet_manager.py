import csv
from time import sleep
from data_manager import DataManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from input_data import GOOGLE_FORM_LINK


class SheetManager:
    """
    This class save data to google sheets with Selenium.
    """

    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        self.data_manager = DataManager()

    def fill_google_sheet(self, address, price, link):
        """
        This function fill google sheet from data what DataManager class was parsed
        :param address: Address from ad
        :param price: Price from ad
        :param link: Link from ad
        :return: None
        """
        self.driver.get(GOOGLE_FORM_LINK)
        sleep(1)

        enter_address = self.driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div['
                                                           '2]/div/div[1]/div/div[1]/input')
        enter_price = self.driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div['
                                                         '2]/div/div[1]/div/div[1]/input')
        enter_link = self.driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div['
                                                        '2]/div/div[1]/div/div[1]/input')
        enter_send_button = self.driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')

        enter_address.send_keys(address)
        enter_price.send_keys(f"${price}")
        enter_link.send_keys(link)
        enter_send_button.send_keys(Keys.ENTER)

        enter_next_answer = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
        enter_next_answer.send_keys(Keys.ENTER)


def save_to_csv(data):
    """
    This function save all parsed data to csv file.
    :param data: Data what DataManager class was parsed
    :return: None
    """
    with open("rent.csv", "w", newline='') as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["Address", "Price per month", "Link to the property?"])
        writer.writerows(data)

