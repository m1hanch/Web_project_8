import requests
from bs4 import BeautifulSoup
import json


def get_news():
    url = "https://www.bbc.com/news/world"
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    video_player_image = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTQm42v1XDsudIs2WMM9yGupYi15ntu28Cg5w&usqp=CAU'
    articles = soup.find_all('div', {'data-testid': 'alaska-grid'})[0]
    articles_list = []
    for article in articles:
        title = article.find('h2', {'data-testid': 'card-headline'})
        title = title.text if title else 'Title not found'
        source = article.find('a', {'data-testid': 'internal-link'})
        if source is None:
            continue
        else:
            source = 'https://www.bbc.com/'+source['href']
        img = article.find('div', {'data-testid': 'card-media'}).find('img', class_='efFcac')
        img = img['src'] if img else video_player_image
        description = article.find('p', {'data-testid': 'card-description'})
        description = description.text if description else ''
        date = article.find('span', {'data-testid': 'card-metadata-lastupdated'})
        date = date.text if date else ''
        article_data = {
            'title': title,
            'source': source,
            'img_link': img,
            'text': description,
            'date': date
        }
        articles_list.append(article_data)

    return articles_list


def parse_articles(articles) -> list:
    article_list = []
    for article in articles:
        source = article.find('a', {'data-testid': 'internal-link'})
        if source is None:
            continue
        else:
            source = 'https://www.bbc.com' + source['href']
        title = article.find('h2', {'data-testid': 'card-headline'}).text
        img = article.find('div', {'data-testid': 'card-media'}).find('img', class_='efFcac')['src']
        published = article.find('span', {'data-testid': 'card-metadata-lastupdated'}).text
        article_data = {
            'title': title,
            'source': source,
            'img_link': img,
            'date': published
        }
        article_list.append(article_data)
    return article_list


def get_tech_news(section: str):
    url = f"https://www.bbc.com/{section}"
    response = requests.get(url)
    response.encoding = 'utf-8'
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    articles = soup.find_all('div', {'data-testid': 'nevada-grid-6'})[0]
    articles_list = parse_articles(articles)

    articles = soup.find_all('div', {'data-testid': 'nevada-grid-4'})[0]
    articles_list.extend(parse_articles(articles))

    articles = soup.find_all('div', {'data-testid': 'alaska-grid'})[0]
    articles_list.extend(parse_articles(articles))

    return articles_list


def get_environment_news(section: str):
    url = f"https://www.bbc.com/news/{section}"
    response = requests.get(url)
    response.encoding = 'utf-8'
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    articles = soup.find_all('ol', {'role': 'list'})[0]
    articles_list = []

    for article in articles.find_all('li', class_='ssrcss-qtbdxl-StyledListItem e1d6xluq3'):
        source = 'https://www.bbc.com/' + article.find('a', class_=lambda x: x and x.startswith('ssrcss-'))['href']
        title = article.find('span', {'role': 'text'}).text
        img = article.find('img')['src']
        published = article.find('span', class_='ssrcss-i6hqx6-Timestamp').text
        published = published if published else article.find('span', class_='ssrcss-d8d0g-LivePulse ev7eeod2').text
        article_data = {
            'title': title,
            'source': source,
            'img_link': img,
            'date': published
        }
        articles_list.append(article_data)

    return articles_list


def get_sport_news():
    url = "https://en.as.com/soccer/"
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    articles = soup.find_all('article', class_='s')
    articles_list = []
    for article in articles:
        source = article.find('a').get('href')
        img = article.find('img').get('src')
        title = article.find('h2', class_='s__tl').text
        description = article.find('p', class_='s__sum')
        description = description.text if description else ''
        day = article.find('span', class_='s__day')
        day = day.text if day else ""
        hour = article.find('span', class_='s__hour')
        hour = hour.text if hour else ""
        date = f'{day} {hour}'

        article_data = {
            'title': title,
            'source': source,
            'img_link': img,
            'text': description,
            'date': date
        }
        articles_list.append(article_data)
    return articles_list


def get_politics_news():
    url = "https://www.foxnews.com/politics"
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    articles = soup.find('section', class_='collection collection-article-list').find_all('article', class_='article')
    articles_list = []
    for article in articles:
        source = "https://www.foxnews.com"+article.find('a').get('href')
        img = article.find('img').get('src')
        title = article.find('h4', class_='title').text
        time = article.find('span', class_='time').text

        article_data = {
            'title': title,
            'source': source,
            'img_link': img,
            'date': time
        }
        articles_list.append(article_data)
    return articles_list


