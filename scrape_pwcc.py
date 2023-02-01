import time
import requests
from bs4 import BeautifulSoup

def get_img_urls(
    url : str
) -> list:
    '''
    get_img_urls():
        Given a URL, this function returns a list of URLs for all `img` elements that have an `alt` attribute
        ending with 'Back' in the HTML of the page at the given URL.
    '''
    res = requests.get(url)

    time.sleep(10)

    soup = BeautifulSoup(res.text, 'html.parser')
    img_tags = soup.find_all('img')
    urls = [img['src'] for img in img_tags if img.has_attr('alt') and img['alt'].endswith('Back')]
    return urls

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
        page_img_urls = get_img_urls(page_url)
        if not page_img_urls:
            break
        urls.extend(page_img_urls)
        page += 1
    return urls

if __name__ == '__main__':
    base_url = 'https://www.pwccmarketplace.com/weekly-auction?q=pokemon+psa+6'
    result = get_all_img_urls(base_url)
    print(result)
