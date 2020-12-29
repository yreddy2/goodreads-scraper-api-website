# This file contains the methods that connect with the api and render the pages

from django.http import HttpResponseRedirect

from django.shortcuts import render

import requests

from .models import PassValAttr, PassValAttrId, PassAll

# The base url of the api
url = 'http://127.0.0.1:5000'


# Method names follow the convention of being named the same as the html page they correspond with.

# Renders the home page
def home(request):
    return render(request, 'home.html')


# Renders the books page
def books(request):
    passed_strings = PassValAttr(attribute=request.POST['attribute'], value=request.POST['value'])
    api_request = requests.get(url + '/get/books/' + passed_strings.attribute + '="' + passed_strings.value + '"').json()
    all_books = []
    for book in api_request:
        book_info = []
        for attribute in book:
            book_info.append(book[attribute])
        book_info.append("/book/" + book_info[0] + '/')
        all_books.append(book_info)
    return render(request, 'books.html', {'all_books': all_books})


# Renders the authors page
def authors(request):
    passed_strings = PassValAttr(attribute=request.POST['attribute'], value=request.POST['value'])
    api_request = requests.get(url + '/get/authors/' + passed_strings.attribute + '="' + passed_strings.value + '"').json()
    all_authors = []
    for author in api_request:
        author_info = []
        for attribute in author:
            author_info.append(author[attribute])
        author_info.append("/author/" + author_info[0] + '/')
        all_authors.append(author_info)
    return render(request, 'authors.html', {'all_authors': all_authors})


# Renders a specific books page
def book_detailed(request, _id):
    api_request = requests.get(url + '/get/books/' + '_id' + '="' + _id + '"').json()
    book_info = []
    for attribute in api_request[0]:
        book_info.append([attribute + ":", api_request[0][attribute]])
    return render(request, 'book_detailed.html', {'book_info': book_info})


# Renders a specific authors page
def author_detailed(request, _id):
    api_request = requests.get(url + '/get/authors/' + '_id' + '="' + _id + '"').json()
    author_info = []
    for attribute in api_request[0]:
        author_info.append([attribute + ":", api_request[0][attribute]])
    return render(request, 'author_detailed.html', {'author_info': author_info})


# Method allows books to be updated
def book_update(request):
    passed_strings = PassValAttrId(attribute=request.POST['attribute'], value=request.POST['value'], ident=request.POST['ident'])
    pass_object = {passed_strings.attribute: passed_strings.value}
    val = requests.put(url=url + '/update/book/' + '_id' + '="' + passed_strings.ident + '"', data=pass_object)
    return HttpResponseRedirect('/book/' + passed_strings.ident)


# Method allows authors to be updated
def author_update(request):
    passed_strings = PassValAttrId(attribute=request.POST['attribute'], value=request.POST['value'], ident=request.POST['ident'])
    pass_o = {passed_strings.attribute: passed_strings.value}
    val = requests.put(url=url + '/update/author/' + '_id' + '="' + passed_strings.ident + '"', data=pass_o)
    return HttpResponseRedirect('/author/' + passed_strings.ident)


# Renders the add book form
def add_book_form(request):
    return render(request, 'add_book_form.html')


# Renders the add author form
def add_author_form(request):
    return render(request, 'add_author_form.html')


# Method to add a book to the db
def add_book(request):
    passed_strings = PassAll(ident=request.POST['ident'], book_url=request.POST['book_url'], title=request.POST['title'],
                             ISBN=request.POST['ISBN'], author=request.POST['author'],
                             author_url=request.POST['author_url'], rating=request.POST['rating'],
                             rating_count=request.POST['rating_count'], review_count=request.POST['review_count'],
                             image_url=request.POST['image_url'], similar_books=request.POST['similar_books'])
    book_info = {"_id": PassAll.ident, "book_url": PassAll.book_url, "title": PassAll.title, "ISBN": PassAll.ISBN,
                 "author": PassAll.author, "author_url": PassAll.author_url, "rating": PassAll.rating,
                 "rating_count": PassAll.rating_count, "review_count": PassAll.review_count,
                 "image_url": PassAll.image_url, "similar_books": PassAll.similar_books}
    val = requests.post(url=url + '/add/book', data=book_info)
    return HttpResponseRedirect('/home/')


# Method to delete a book from the db
def delete_book(request, _id):
    requests.delete(url + '/delete/book/' + '_id' + '="' + _id + '"')
    return HttpResponseRedirect('/home/')


# Method to delete an author from the db
def delete_author(request, _id):
    requests.delete(url + '/delete/author/' + '_id' + '="' + _id + '"')
    return HttpResponseRedirect('/home/')


# Method to render the page that contains query 1
def query1(request):
    api_request = requests.get(url + '/query1/').json()
    author_info = []
    for attribute in api_request[0][0]:
        author_info.append([attribute + ":", api_request[0][0][attribute]])
    return render(request, 'most-book-authors.html', {"author_info": author_info})


# Method to render the page that contains visualization 1
def vis1(request):
    api_request = requests.get(url + '/vis1/').json()
    all_authors = []
    for author in api_request:
        all_authors.append(author['_id'] + ": " + str(author['rating']))
    return render(request, 'rank-authors.html', {'all_authors': all_authors})


# Method to render the page that contains visualization 2
def vis2(request):
    api_request = requests.get(url + '/vis2/').json()
    all_books = []
    for book in api_request:
        all_books.append(book['_id'] + ": " + str(book['review_count']))
    return render(request, 'rank-books.html', {'all_books': all_books})