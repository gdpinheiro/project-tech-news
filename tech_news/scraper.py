import requests
import time
from parsel import Selector
from tech_news.database import create_news


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


# Requisito 4
def scrape_noticia(html_content):
    if "<!doctype html>" in html_content:
        selector = Selector(text=html_content)

        url = selector.css("head link[rel=canonical]::attr(href)").get()
        title = selector.css(".entry-title::text").get().strip()
        timestamp = selector.css(".meta-date::text").get()
        writer = selector.css(".author a::text").get()
        try:
            comments_count = selector.css(
                ".post-comments .title-block::text"
            ).re(r"\d comments")[0][0]
        except Exception:
            comments_count = 0
        summary = "".join(
            selector.css(".entry-content > p:nth-of-type(1) *::text").getall()
        ).strip()
        tags = selector.css(".post-tags li a::text").getall()
        category = selector.css(".category-style .label::text").get()

        return {
            "url": url,
            "title": title,
            "timestamp": timestamp,
            "writer": writer,
            "comments_count": int(comments_count),
            "summary": summary,
            "tags": tags,
            "category": category,
        }
    else:
        return None


# Requisito 5
def get_tech_news(amount):
    news_links = []
    url = "https://blog.betrybe.com/"

    while news_links.__len__() < amount:
        for news in scrape_novidades(fetch(url)):
            news_links.append(news)
        url = scrape_next_page_link(fetch(url))

    del news_links[amount:]

    news_pages = []

    for news in news_links:
        page = scrape_noticia(fetch(news))
        news_pages.append(page)

    create_news(news_pages)

    return news_pages
