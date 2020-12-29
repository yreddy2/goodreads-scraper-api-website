# This file contains the API that communicates with the database(db)
from flask import Flask

from pymongo import MongoClient

from bson.json_util import dumps

from flask import jsonify, request

# Uses flask to connect the database to the api
app = Flask(__name__)
client = MongoClient('INSERT_DATABASE_HERE')
db = client.get_database('goodreads')

# set of book documents
book_collection = db.books

# set of author documents
author_collection = db.authors


# Methods to send signals or errors for the different API calls
def send_ok():
    resp = jsonify("200 OK")
    resp.status_code = 200
    return resp


def send_created():
    resp = jsonify("201 CREATED")
    resp.status_code = 201
    return resp


def send_bad_request():
    resp = jsonify("400 Bad Request")
    resp.status_code = 400
    return resp


def send_unsupported_media_type():
    resp = jsonify("415 Unsupported Media Type")
    resp.status_code = 415
    return resp


def get_record(specifier):
    """
    Method to parse the search parameters
    :param specifier: the given input from the users api call
    :return: the record that the db needs to search for
    """
    if '&' in specifier or '|' in specifier:
        if '&' in specifier:
            split_char = '&'
            operation = "$and"
        elif '|' in specifier:
            split_char = '|'
            operation = "$or"
        specifier1 = specifier.split(split_char)[0]
        specifier2 = specifier.split(split_char)[1]
        attr1 = specifier1.split('=')[0]
        attr2 = specifier2.split('=')[0]
        val1 = specifier1.split('=')[1][1:-1]
        val2 = specifier2.split('=')[1][1:-1]
        record = {operation: [{attr1: {"$regex": val1, "$options": 'i'}}, {attr2: {"$regex": val2, "$options": 'i'}}]}
    else:
        attr = specifier.split('=')[0]
        val = specifier.split('=')[1][1:-1]
        record = {attr: {"$regex": val, "$options": 'i'}}
    return record


def update_query(specifier, collection):
    """
    Method to update a document in the db
    :param specifier: search parameter
    :param collection: set of documents
    :return: response
    """
    try:
        updates = request.json
    except Exception as e:
        return send_bad_request()
    else:
        for key in updates:
            if collection.find({key: {"$exists": True}}).count() == 0:
                return send_unsupported_media_type()
            collection.update_one(get_record(specifier), {"$set": {key: updates[key]}})
        return send_ok()


def get_query(specifier, collection):
    """
    Method to get documents from the db
    :param specifier: search parameter
    :param collection: set of documents
    :return: set of documents that fit the search parameter
    """
    try:
        record = get_record(specifier)
    except Exception as e:
        return send_bad_request()
    else:
        return dumps(collection.find(record))


def add_query_to_db(collection, info):
    """
    Helper to add a document to the db
    :param collection: set of documents
    :param info: information that the document must contain
    :return: response
    """
    for key in info:
        if collection.find({key: {"$exists": True}}).count() == 0:
            return send_unsupported_media_type()
    collection.insert(info)
    return send_created()


def add_query(collection):
    """
    Method to one document to the db
    :param collection: set of documents
    :return: response
    """
    try:
        info = request.json
    except Exception as e:
        return send_bad_request()
    else:
        return add_query_to_db(collection, info)


def add_multiple_query(collection):
    """
    Method to multiple documents to the db
    :param collection: set of documents
    :return: response
    """
    try:
        infos = request.json
    except Exception as e:
        return send_bad_request()
    else:
        for element in infos:
            if add_query_to_db(collection, infos[element]).status_code == 415:
                return send_unsupported_media_type()
    return send_created()


def delete_query(specifier, collection):
    """
    Method to delete a document from the db
    :param specifier: search parameter
    :param collection: set of documents
    :return: response
    """
    try:
        record = get_record(specifier)
    except Exception as e:
        return send_bad_request()
    else:
        collection.delete_one(record)
        return send_ok()


# The following methods establish the api urls and call the appropriate methods depending on the task
@app.route('/get/books/<specifier>')
def get_books(specifier):
    return get_query(specifier, book_collection)


@app.route('/update/book/<specifier>', methods=['PUT'])
def update_book(specifier):
    return update_query(specifier, book_collection)


@app.route('/add/book', methods=['POST'])
def add_book():
    return add_query(db.books)


@app.route('/add/books', methods=['POST'])
def add_books():
    return add_multiple_query(book_collection)


@app.route('/delete/book/<specifier>', methods=['DELETE'])
def delete_book(specifier):
    return delete_query(specifier, book_collection)


@app.route('/get/authors/<specifier>')
def get_authors(specifier):
    return get_query(specifier, author_collection)


@app.route('/update/author/<specifier>', methods=['PUT'])
def update_author(specifier):
    return update_query(specifier, author_collection)


@app.route('/add/author', methods=['POST'])
def add_author():
    return add_query(db.books)


@app.route('/add/author', methods=['POST'])
def add_authors():
    return add_multiple_query(author_collection)


@app.route('/delete/author/<specifier>', methods=['DELETE'])
def delete_author(specifier):
    return delete_query(specifier, author_collection)


@app.route('/query1/')
def most_book_authors():
    """
    Queries the database and finds the author with the most books in the db
    :return: author with the most books
    """
    ranking = book_collection.aggregate(
        [
            {"$match": {}},
            {"$group": {"_id": "$author", "total": {"$sum": 1}}},
            {'$sort': {"total": -1}}
        ]
    )
    author_id = list(ranking)[0]['_id']
    return dumps({author_collection.find({"_id": author_id})})


@app.route('/vis1/')
def highest_rating():
    """
    Queries the database and returns the authors in order of ratings
    :return: authors in order of ratings
    """
    ranking = author_collection.aggregate(
        [
            {"$match": {}},
            {"$group": {"_id": "$name", "rating": {"$sum": {"$toDouble": "$rating"}}}},
            {'$sort': {"rating": -1}}
        ]
    )
    return dumps(ranking)


@app.route('/vis2/')
def highest_review_count():
    """
    Queries the database and returns the books in order of reviews
    :return: books in order of reviews
    """
    ranking = book_collection.aggregate(
        [
            {"$match": {}},
            {"$group": {"_id": "$title", "review_count": {"$sum": {"$toDouble": "$review_count"}}}},
            {'$sort': {"review_count": -1}}
        ]
    )
    return dumps(ranking)


if __name__ == "__main__":
    app.run(debug=True)