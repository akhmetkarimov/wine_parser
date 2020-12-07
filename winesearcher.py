import time 
import csv
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

def wineParser(wine_name):
    items = []
    url = f"https://www.wine-searcher.com/find/{wine_name}"
    time.sleep(2)
    # options = webdriver.ChromeOptions()
    # options.add_argument("user-data-dir=/Users/_akhmetkarimov_/Library/Application Support/Google/Chrome/")
    # driver = webdriver.Chrome(executable_path='./chromedriver', chrome_options=options)
    driver = webdriver.Chrome(executable_path='./chromedriver')
    driver.get(url)
    cards = driver.find_elements_by_css_selector('.tab-prices-content div.offer-card ')
    if not cards:
        return []
    try: 
        for card in cards:
            link = card.find_element_by_css_selector('a.pb-0').get_attribute('href')
            title = card.find_element_by_css_selector('.offer-card__seller-name span').text
            address = card.find_element_by_css_selector('.offer-card__location-address').text
            price = card.find_element_by_css_selector('.price__detail_main').text
            items.append({
                'link': link,
                'title': title,
                'address': address,
                'price': price
            })
    except NoSuchElementException:
        print('No Such Elem')
    driver.close()
    return items

def to_csv(wine, items):
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    with open(f'./parsed/{wine}{current_time}.csv', 'w', encoding = 'utf-8') as file:
        a_pen = csv.writer(file)
        a_pen.writerow(('title', 'address', 'price', 'link'))
        for item in items:
            a_pen.writerow((item['title'],item['address'], item['price'], item['link']))


wine = input('\n--- Welcome to the wine-searcher.com, console application ---\n\nPlease Enter wine name for searching: ')

items = wineParser(wine)
if items:
    to_csv(wine, items)