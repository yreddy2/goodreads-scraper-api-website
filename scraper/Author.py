import requests
from bs4 import BeautifulSoup

# Contains the base url to traverse to an author
AUTHOR_BASE_URL = 'https://www.goodreads.com/author/show'

# Functions to get the various pieces of information from the authors page


def get_author_name(soup):
    return soup.find('h1', class_='authorName').text.split('\n')[1]


def get_author_id(url):
    return url.split('/')[5].split('.')[0]


def get_author_rating(soup):
    return soup.find('span', class_='rating').find('span').text


def get_author_rating_count(soup):
    return soup.find('span', class_='votes').find('span')['content']


def get_author_review_count(soup):
    return soup.find('span', class_='count').find('span')['content']


def get_author_image_url(soup):
    return soup.find('div', class_='leftContainer authorLeftContainer').a.img['src']


def get_author_author_books(soup):
    author_books = list()
    soups = soup.find_all('a', class_='bookTitle')
    for i in range(0, len(soups) - 1):
        author_books.append(soups[i]['href'].split('/')[3].split('-')[0].split('.')[0])
    return author_books


def get_author_related_authors(soup):
    url = soup.find('div', class_='hreview-aggregate').find_all('a')[1]['href']

    start = 'https://www.goodreads.com' + url

    source = requests.get(start).text

    new_soup = BeautifulSoup(source, 'lxml')

    similar_authors = list()

    soups = new_soup.find_all('a', class_='gr-h3 gr-h3--serif gr-h3--noMargin')
    for i in range(1, len(soups)):
        similar_authors.append(soups[i]['href'].split('/')[5].split('.')[0])
    return similar_authors


def get_author_info(id_):
    """
    :param id_: the id of the author that the info relates to
    :return: dictionary containing all the information about the author
    """

    author_info = dict()

    url = AUTHOR_BASE_URL + '/' + id_
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    author_info['name'] = get_author_name(soup)
    author_info['author_url'] = url
    author_info['author_id'] = get_author_id(url)
    author_info['rating'] = get_author_rating(soup)
    author_info['rating_count'] = get_author_rating_count(soup)
    author_info['review_count'] = get_author_review_count(soup)
    author_info['image_url'] = get_author_image_url(soup)
    author_info['related_authors'] = get_author_related_authors(soup)
    author_info['author_books'] = get_author_author_books(soup)
    return author_info

