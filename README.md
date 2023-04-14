# Mi Valentino
---

## Requirements
* Python 3.8.x

## Table of Content
* Overview
* Goals
* Usage
* Conclusion
* Afterword

## Overview
This project involves using Python, Beautiful Soup, Selenium, and Pandas to extract product information from the Valentino website. We will extract data such as product names, prices, descriptions, sizes, colors, and images, and then perform data analysis using pandas and matplotlib to gain insights into the trends and patterns of the products. Additionally, I use Tableau to create interactive visualizations to further explore and analyze the data. This project showcases the power of web scraping and data analysis using Python and its libraries, as well as the ability to present findings using Tableau.

## Goals
* Utilize `Selenium` Open a session to navigate through website.
* Utilize `BeatifulSoup` to extract product details such as product code, price, type of product, etc.
* Utilize `pandas` to store data into a dataframe and further process by removing duplicates and null items, then save to database or as `.csv`.

## Usage
To visualize how the algorithm works there are a few steps.

* Create a virtual environment:
    ```Bash
    python -m venv c:\path\to\environment
    ```
* Next install requirements using pip:
    ```Bash
    pip install -r requirements.txt
    ```
* Once all required packages are installed you can scrape the Velentino website for all it's products and details:
    ```Bash
    python3 valentino_scrape.py
    ```
## Conclusion
I was able to extract most of the products form the website, some items returned empty values.  I was able to extract ovr 3400 products and after processing I ended up with over 1100 products.  I then Utilized tableau to extract insights from all products such as top products costing over $10k, visualize most expensive products under each category (dress, shoes, shorts, etc.).

## Afterword
This algorithm was developed mainly for a client to help them quickly compare product rates within their inventory.