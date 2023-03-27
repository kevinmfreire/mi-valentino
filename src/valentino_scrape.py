'''
This script automates the process of extracting all the products from the Valentino
website.
'''

import pandas as pd

from utils import ChromeDriver, ValentinoScrape


def valentino_menu_items():
    '''
    This function automates the process in extracting all
    items from menu bar of the valentino webpage home page.
    It saves it into a .csv file.
    '''
    soup = valentino.request_(can_valentino_url)
    menu_items = valentino.nav_menu(soup)
    prod_df = valentino.extract_product_links(menu_items)
    prod_df.to_csv(csv_file_menu, index=False)
    print(prod_df)


def get_valentino_products(prod_df):
    '''
    Extract products from each link saved from the
    'valentino_menu_items()' function.  It then structures
    the data and saves it into a .csv file.
    '''
    for i in range(len(prod_df)):
        page_source = driver.find_elements(prod_df.links[i])
        soup = valentino.bs_(page_source)
        product_list.update(
            valentino.extract_products(soup, product_list, prod_df.product_category[i])
        )
        driver.delete_cookies()
        driver.wait(2)
    df = pd.DataFrame.from_dict(product_list)
    df.to_csv(valentino_prod_file, index=False)
    print(df)
    driver.close()


def clean_data(source, des):
    '''
    Cleans data by removing duplicates and restructering data
    for a product analysis with Tableau.
    '''
    v_df = pd.read_csv(source)
    v_df = v_df.drop_duplicates(
        subset=v_df.columns.difference(["product_type"])
    ).reset_index(drop=True)
    v_df[["Currency", "Value"]] = v_df.price.str.split("$", expand=True)
    v_df["Value"] = v_df["Value"].apply(
        lambda x: x.replace(",", "") if not None else None
    )
    v_df = v_df[
        [
            "product_id",
            "product_code",
            "product_type",
            "item_name",
            "color",
            "Currency",
            "Value",
        ]
    ]
    v_df.to_csv(des, index=False)


if __name__ == "__main__":
    csv_file_menu = "../data/valentino/csv_files/menu_items.csv"
    valentino_prod_file = "../data/valentino/csv_files/valentino_products.csv"
    valentino_clean_data = "../data/valentino/csv_files/valentino_data.csv"
    valentino_database = "../data/valentino/database"
    can_valentino_url = "https://www.valentino.com/en-ca"

    product_list = {
        "product_id": [],
        "product_code": [],
        "product_type": [],
        "item_name": [],
        "color": [],
        "price": [],
        "image_url": [],
    }

    """Extracting all items in navigation menu of Valentino Landing page"""
    valentino = ValentinoScrape()
    valentino_menu_items()

    driver = ChromeDriver()
    df = pd.read_csv(csv_file_menu)
    get_valentino_products(df)

    clean_data(valentino_prod_file, valentino_clean_data)
