from bs4 import BeautifulSoup
import requests

# Contains the base url to traverse to a book
BOOK_BASE_URL = 'https://www.goodreads.com/book/show'


# Functions to get the various pieces of information from the books page

def get_book_image_url(soup):
    return soup.find('div', class_="leftContainer").find('a').find('img')['src']


def get_book_title(soup):
    # return soup.find('h1', class_="gr-h1 gr-h1--serif").text
    return soup.find('div', class_="infoBoxRowItem").text


def get_book_id(url):
    return url.split('/')[5].split('-')[0].split('.')[0]


def get_book_isbn(soup):
    return soup.find('div', class_="infoBoxRowItem").find_next().find('div', class_="infoBoxRowItem").text.split(' ')[18].split('\n')[0]


def get_book_author_url(soup):
    return 'https://goodreads.com' + soup.find('div', class_='bookAuthorProfile__name').a['href']


def get_book_author(soup):
    # return soup.find('div', class_='bookAuthorProfile__name').a.text.split('\n')[0]
    return soup.find('div', class_='bookAuthorProfile__name').a['href'].split('/')[3].split('.')[0]


def get_book_rating(soup):
    return soup.find('div', class_='uitext stacked').find_all('span')[6].text.split(' ')[2].split('\n')[0]


def get_book_rating_count(soup):
    return soup.find('div', class_='uitext stacked').find_all('a')[1].meta['content']


def get_book_review_count(soup):
    return soup.find('div', class_='uitext stacked').find_all('a')[2].meta['content']


def get_book_similar_books(soup):
    similar_books = list()
    soups = soup.find('div', class_='carouselRow').find_all('li')
    for i in range(1, len(soups)):
        similar_books.append(soups[i]['id'].split('_')[1])
    return similar_books


def get_book_info(id_):
    """
    :param id_: the id of the author that the info relates to
    :return: dictionary containing all the information about the author
    """

    book_info = dict()
    url = BOOK_BASE_URL + '/' + id_
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    book_info['book_url'] = url
    book_info['title'] = get_book_title(soup)
    book_info['book_id'] = get_book_id(url)
    book_info['ISBN'] = get_book_isbn(soup)
    book_info['author'] = get_book_author(soup)
    book_info['author_url'] = get_book_author_url(soup)
    book_info['rating'] = get_book_rating(soup)
    book_info['rating_count'] = get_book_rating_count(soup)
    book_info['review_count'] = get_book_review_count(soup)
    book_info['image_url'] = get_book_image_url(soup)
    book_info['similar_books'] = get_book_similar_books(soup)
    return book_info


