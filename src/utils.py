'''
utils.py containes two classes.

VelentinoScrape class allows the process to extract data from the valentino website.
ChromeDriver class uses selenium to automatically load every content before
extracting product details.
'''

import json

import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class ValentinoScrape:
    '''
    The class allows the process to extract data from the valentino website
    '''
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0"
        }
        self.session = requests.Session()
        self.session.headers = self.headers

    def request_(self, url):
        '''Sends a request to the target url'''
        request = self.session.get(url)
        soup = bs(request.content, "html.parser")
        return soup

    def bs_(self, page_source):
        '''Extracts soup object for extracting data'''
        return bs(page_source, "html.parser")

    def nav_menu(self, soup):
        '''Finds all links in the manu bar of the valentino home page and stores as a list'''
        nav_bar = soup.find("ul", {"class": "level-0"})
        menu_item = [item for item in nav_bar.find_all("li", {"class": "hasChildren"})]
        return menu_item

    def secure_site(self, product_links):
        '''Enables all extracted links with correct web link.'''
        https = "https://"
        valentino_url = "www.valentino.com"
        if https not in product_links:
            product_links = https + valentino_url + product_links
        return product_links

    def extract_product_links(self, menu_items):
        '''Removes any duplicates, unwanted categories and saves to dataframe.'''
        excluded_categories = [
            "View all",
            "New Arrivals",
            "READY TO WEAR",
            "BAGS",
            "SHOES",
            "ACCESSORIES",
            "VALENTINO ROSSO",
            "Digital Card",
        ]
        products = {"links": [], "product_category": []}

        for menu_item in menu_items:
            links = menu_item.find_all("a")
            for link in links:
                products["links"].append(self.secure_site(link["href"]))
                products["product_category"].append(link.find("span").get_text())

        prod_df = pd.DataFrame.from_dict(products)
        prod_df = (
            prod_df[~prod_df["product_category"].isin(excluded_categories)]
            .iloc[:103]
            .reset_index(drop=True)
        )
        prod_df.columns = ["links", "product_category"]

        return prod_df

    def extract_products(self, soup_container, product_list, product_type):
        '''Extracts products from each link in menu item'''
        for category in soup_container.find_all("ul", {"class": "products__list"}):
            for item in category.find_all("div", {"class": "item__info"}):
                item_link = item.find("a")["href"]

                try:
                    s_item = self.request_(item_link)
                    item_name = s_item.find("span", {"class": "modelName"}).get_text()
                    currency = (
                        s_item.find("span", {"class": "price"})
                        .find("span", {"class": "currency"})
                        .get_text()
                    )
                    value = (
                        s_item.find("span", {"class": "price"})
                        .find("span", {"class": "value"})
                        .get_text()
                    )
                    product_code = (
                        s_item.find(
                            "div", {"class": "item-description__modelfabricolor"}
                        )
                        .find("span", {"class": "value"})
                        .get_text()
                    )

                    # Check if has item features
                    json_info = s_item.find("li", {"class": "is-selected"})
                    if (
                        json_info is not None
                        and json_info["data-ytos-color-model"] is not None
                    ):
                        info = json.loads(json_info["data-ytos-color-model"])
                        product_list["product_id"].append(info["ProductId"])
                        product_list["color"].append(info["Label"])
                        product_list["image_url"].append(info["Image"])
                    else:
                        product_list["product_id"].append(None)
                        product_list["color"].append(None)
                        product_list["image_url"].append(None)

                    product_list["product_code"].append(product_code)
                    product_list["product_type"].append(product_type)
                    product_list["item_name"].append(item_name)
                    product_list["price"].append(currency + value)
                except AttributeError:
                    print(f"Unable to extract text from page source: {item_link}")

        return product_list


class ChromeDriver:
    '''
    Utilizing selenium to automatically load every content before
    '''
    def __init__(self):
        self.options = Options()
        self.options.binary_location = (
            "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
        )
        self.chrome_driver = "/mnt/c/WINDOWS/chromedriver.exe"
        self.driver = webdriver.Chrome(self.chrome_driver, chrome_options=self.options)
        self.driver.maximize_window()

    def is_load_more_displayed(self):
        '''Checks if there is a 'load more' option'''
        try:
            load_more_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//button[@class="ctaButton ctaButton--lightBorder loadMoreShelvesProducts"]',
                    )
                )
            )
            return load_more_button.is_displayed()
        except TimeoutException:
            return False

    def find_elements(self, url):
        '''Driver automatically clicks and waits until all products are shown before extracting items.'''
        self.driver.get(url)
        self.driver.implicitly_wait(5)
        try:
            while self.is_load_more_displayed():
                load_more_button = self.driver.find_element(
                    By.XPATH,
                    '//button[@class="ctaButton ctaButton--lightBorder loadMoreShelvesProducts"]',
                )
                load_more_button.click()
                self.driver.implicitly_wait(10)
            return self.driver.page_source
        except AttributeError:
            print("Could not locate more items for product site: {}".format(url))
            return self.driver.page_source

    def scroll_to_bottom(self, url):
        '''Solves infinite scroll problem if it is necessary.'''
        self.driver.get(url)
        self.driver.implicitly_wait(2)
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to the bottom of the page
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )

            # Wait for new content to load
            self.driver.implicitly_wait(5)

            # Calculate the new page height and check if it has changed
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                # Stop scrolling if the page height hasn't changed
                break
            else:
                # Update the last height to the new height
                last_height = new_height

        return self.driver.page_source

    def wait(self, duration):
        '''Driver waits for specified duration'''
        self.driver.implicitly_wait(duration)

    def delete_cookies(self):
        self.driver.delete_all_cookies()

    def close(self):
        self.driver.close()
