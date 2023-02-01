import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

def get_hrefs(
    url : str
) -> list:
    '''
    get_hrefs():
        Given a URL, this function returns a list of URLs for all `a` elements that have an `data-testid` attribute
        equal to 'item-title' in the HTML of the page at the given URL.
    '''
    driver = webdriver.Chrome()
    driver.get(url)

    time.sleep(10)

    links = driver.find_elements("xpath", "//a[@data-testid='item-title']")
    hrefs = []
    for link in links:
        hrefs.append(link.get_attribute('href'))

    return hrefs

def get_all_img_urls(
    base_url : str
) -> list:
    '''
    get_all_img_urls():
        Given a base URL, this function returns a list of URLs for all `img` elements that have an `alt` attribute
        ending with 'Back' in the HTML of all pages at the given URL and its paginated versions.
    '''
    urls = []
    page = 1
    while True:
        page_url = fr'{base_url}&page={str(page)}'
        page_img_urls = get_hrefs(page_url)
        if not page_img_urls:
            break
        urls += page_img_urls
        page += 1
    return urls

if __name__ == '__main__':
    base_url = 'https://www.pwccmarketplace.com/weekly-auction?q=pokemon+psa+6'
    result = get_all_img_urls(base_url)
    print(result)
