import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

URL = "https://www.zillow.com/homes/for_rent/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.40698752216683%2C%22east%22%3A-122.24270758442269%2C%22south%22%3A37.933119497172605%2C%22north%22%3A38.04311261072654%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A13%7D"
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.42",
    "Accept-Language": "en-US,en;q=0.9,id;q=0.8",
}


# TODO Fetch data from ZILLOW using beautifulsoup
class ZillowData:

    def __init__(self):
        response = requests.get(url=URL, headers=header)
        contents = response.text
        self.soup = BeautifulSoup(contents, "html.parser")

    def get_link(self) -> list:
        property_link = []
        zillow_link = "https://www.zillow.com"
        property_list = self.soup.find_all(name="div", class_="property-card-data")
        for data in property_list:
            href = data.next_element.findNext(name="a").get("href")
            if href[0] == "/":
                href = zillow_link + href
            property_link.append(href)

        return property_link

    def get_price(self) -> list:
        property_price = []
        price_list = self.soup.find_all(name="div", class_="hRqIYX")
        for price in price_list:
            if " " in price.getText():
                clean = price.getText().split(" ")
                price_clean = clean[0]
                property_price.append(price_clean)
            else:
                property_price.append(price.getText())

        return property_price

    def get_address(self) -> list:
        property_address = []
        address_list = self.soup.find_all(name="div", class_="property-card-data")
        for address in address_list:
            address_str = address.find_next("a").get_text()
            property_address.append(address_str)

        return property_address


class GoogleDocs:

    def __init__(self):
        self.URL = "https://docs.google.com/forms/d/e/1FAIpQLSe7qwqTnVUbj475f1fAHYQtiD1-dXNT8C28amLVxdpCrLf3TQ/viewform"
        chrome_webdriver_path = "C:\Developement\chromedriver.exe"
        service = Service(executable_path=chrome_webdriver_path)
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=options, service=service)
        self.driver.maximize_window()

    def send_data(self, address, price, link):
        self.driver.get(url=self.URL)
        time.sleep(1)
        address_property = self.driver.find_element(By.CSS_SELECTOR, ".Xb9hP input")
        address_property.send_keys(address)
        price_property = self.driver.find_element(
            By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input'
        )
        price_property.send_keys(price)
        link_property = self.driver.find_element(
            By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input'
        )
        link_property.send_keys(link)
        kirim_button = self.driver.find_element(
            By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div'
        )
        kirim_button.click()


def main():
    zillowdata = ZillowData()
    docs = GoogleDocs()
    link = zillowdata.get_link()
    price = zillowdata.get_price()
    address = zillowdata.get_address()
    print(link)
    print(price)

    for i in range(0, len(address)):
        docs.send_data(address=address[i], price=price[i], link=link[i])


if __name__ == "__main__":
    main()



