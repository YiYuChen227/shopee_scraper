# import libraries
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from time import sleep
from random import randint
from time import time
from IPython.core.display import clear_output
from warnings import warn
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from tqdm import tqdm
from selenium.common.exceptions import TimeoutException
from joblib import Parallel, delayed
import re
import unicodedata

df = pd.read_csv(r"C:\Users\120200\Desktop\shopee web scrape\shopee.csv")

urls_fullwidth = df['name'].unique().tolist()

df['name'].nunique()

urls = []
for i in urls_fullwidth:
    urls.append(unicodedata.normalize('NFKC',i))
urls = urls[1:4]
product_titles = []

for i in tqdm(urls): 
    # set up chrome webdriver
    driver = webdriver.Chrome()

    # reqeust
    url = 'https://shopee.tw/' + i + '?page=0&sortBy=sales'
    driver.get(url)

    # wait for page to load
    wait = WebDriverWait(driver, 10)
    try :
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "shop-page__all-products-section")))
    except TimeoutException:
        driver.close()
        continue

    pagesource = driver.page_source
    soup = BeautifulSoup(pagesource)
    product_container = soup.find(class_ = 'shop-page_product-list').find_all('div', class_ = '_1sRyv_ _2j2K92 _3j20V6')

    for i in product_container:
        product_titles.append(i.text)
    driver.close()
