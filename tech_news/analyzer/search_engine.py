from tech_news.database import search_news
import datetime


# Requisito 6
def search_by_title(title):
    search = search_news(
        {
            "title": {"$regex": title, "$options": "i"},
        }
    )
    result = []

    for item in search:
        result.append((item["title"], item["url"]))

    return result


# Requisito 7
def search_by_date(date):
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")

        isoformat = datetime.date.fromisoformat(date)

        newdate = isoformat.strftime("%d/%m/%Y")

        search = search_news({"timestamp": newdate})

        result = []

        for item in search:
            result.append((item["title"], item["url"]))

        return result
    except ValueError:
        raise ValueError("Data inválida")


# Requisito 8
def search_by_tag(tag):
    search = search_news(
        {
            "tags": tag,
        }
    )

    result = []

    for item in search:
        result.append((item["title"], item["url"]))

    return result


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
