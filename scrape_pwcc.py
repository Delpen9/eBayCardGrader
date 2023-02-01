import time
from bs4 import BeautifulSoup
from selenium import webdriver
import numpy as np

def get_hrefs(
    url : str,
    sleep_time : int = 10
) -> list:
    '''
    get_hrefs():
        Given a URL, this function returns a list of URLs for all `a` elements that have an `data-testid` attribute
        equal to 'item-title' in the HTML of the page at the given URL.
    '''
    driver = webdriver.Chrome()
    driver.get(url)

    time.sleep(sleep_time)

    links = driver.find_elements('xpath', "//a[@data-testid='item-title']")
    hrefs = []
    for link in links:
        hrefs.append(link.get_attribute('href'))

    return hrefs

def get_all_img_hrefs(
    base_url : str,
    sample_limit : int = 125,
    sleep_time : int = 120
) -> list:
    '''
    get_all_img_hrefs():
        Given a base URL, paginate and return a list of URLs
        for all `a` elements that have an `data-testid` attribute
        equal to 'item-title' in the HTML of the page at the given URL.
    '''
    urls = []
    page = 1
    while True:
        page_url = fr'{base_url}&page={str(page)}'

        time.sleep(sleep_time)

        page_img_hrefs = get_hrefs(page_url)

        if not page_img_hrefs:
            break

        urls += page_img_hrefs

        if len(urls) > sample_limit:
            break

        page += 1
    return urls

if __name__ == '__main__':
    psa_values = np.arange(2, 5, 1)

    FILENAME = 'pwcc_card_pages.csv'
    file = open(FILENAME, 'w')
    file.write('IMAGE_LOCATION|PSA_VALUE' + '\n')

    for psa_value in psa_values:
        base_url = fr'https://www.pwccmarketplace.com/weekly-auction?q=pokemon+psa+{psa_value}'
        result = get_all_img_hrefs(base_url)

        for item in result:
            file.write(fr'{item}|{psa_value}' + '\n')

    file.close()
