import requests
import time
from parsel import Selector


# Requisito 1
def fetch(url):
    try:
        time.sleep(1)
        response = requests.get(
            url, headers={"user-agent": "Fake user-agent"}, timeout=3
        )
        if response.status_code == 200:
            return response.text
        else:
            return None
    except requests.ReadTimeout:
        return None


# Requisito 2
def scrape_novidades(html_content):
    if "<!doctype html>" in html_content:
        selector = Selector(text=html_content)
        links = selector.css(".cs-overlay-link::attr(href)").getall()
        if links.__len__() == 0:
            return None
        else:
            return links
    else:
        return []


# Requisito 3
def scrape_next_page_link(html_content):
    if "<!doctype html>" in html_content:
        selector = Selector(text=html_content)
        next_page_link = selector.css(".next.page-numbers::attr(href)").get()
        if next_page_link.__len__() == 0:
            return None
        else:
            return next_page_link
    else:
        return None


html = fetch("https://blog.betrybe.com/")
print(scrape_next_page_link(html))


# Requisito 4
def scrape_noticia(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
