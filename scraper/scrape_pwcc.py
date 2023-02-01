import numpy as np

import time
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.options import Options

import requests
import json

def get_rapid_api_proxy() -> object:
    url = 'https://ephemeral-proxies.p.rapidapi.com/v2/datacenter/proxy'

    headers = {
        'X-RapidAPI-Key': '',
        'X-RapidAPI-Host': 'ephemeral-proxies.p.rapidapi.com'
    }

    response = requests.request('GET', url, headers = headers)
    response_dict = json.loads(response.text)

    hostname = response_dict['proxy']['host']
    port = response_dict['proxy']['port']

    proxy_ip_port = fr'{hostname}:{port}'

    proxy = Proxy()
    proxy.proxy_type = ProxyType.MANUAL
    proxy.http_proxy = proxy_ip_port
    proxy.ssl_proxy = proxy_ip_port

    capabilities = webdriver.DesiredCapabilities.CHROME
    proxy.add_to_capabilities(capabilities)

    return capabilities

def proxy_crawl_proxy(
    url : str,
    javascript_token : str = ''
):
    proxy_crawl_url = f'https://api.crawlbase.com/?token={javascript_token}&url={url}&format=json'
    return proxy_crawl_url

def get_hrefs(
    url : str,
    sleep_time : int = 10,
    proxy_type : str = 'proxy_crawl' #rapid_api
) -> list:
    '''
    get_hrefs():
        Given a URL, this function returns a list of URLs for all `a` elements that have an `data-testid` attribute
        equal to 'item-title' in the HTML of the page at the given URL.
    '''
    assert sleep_time >= 0
    assert proxy_type in ['proxy_crawl', 'rapid_api', 'no_proxy', None]

    if proxy_type == 'rapid_api':
        driver = webdriver.Chrome(desired_capabilities = get_rapid_api_proxy())
        driver.get(url)
    elif proxy_type == 'proxy_crawl':
        driver = webdriver.Chrome()
        driver.get(proxy_crawl_proxy(url))
    elif proxy_type in ['no_proxy', None]:
        driver = webdriver.Chrome()
        driver.get(url)

    time.sleep(sleep_time)

    links = driver.find_elements('xpath', "//a[@data-testid='item-title']")
    hrefs = []
    for link in links:
        hrefs.append(link.get_attribute('href'))

    driver.quit()

    return hrefs

def get_all_img_hrefs(
    base_url : str,
    sample_limit : int = 125,
    sleep_time : int = 10
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
