# This file contains the unit tests for the API
import unittest

import api

import requests

url = 'http://127.0.0.1:5000'


class TestCalc(unittest.TestCase):

    # Tests for checking if url is parsed correctly
    def test_simple_get_record(self):
        specifier = 'title="test"'
        self.assertEqual(api.get_record(specifier), {'title': {'$options': 'i', '$regex': 'test'}})

    def test_or_get_record(self):
        specifier = 'title="test"|title="here"'
        self.assertEqual(api.get_record(specifier), {'$or': [{'title': {'$options': 'i', '$regex': 'test'}},
                                                             {'title': {'$options': 'i', '$regex': 'here'}}]})

    def test_and_get_record(self):
        specifier = 'title="test"&title="here"'
        self.assertEqual(api.get_record(specifier), {'$and': [{'title': {'$options': 'i', '$regex': 'test'}},
                                                              {'title': {'$options': 'i', '$regex': 'here'}}]})

    # Tests for checking if get functions properly
    def test_simple_get_books(self):
        api_request = requests.get(url + '/get/books/' + 'title="clean"').json()
        self.assertEqual(api_request[0]['title'],
                         "Clean Code: A Handbook of Agile Software Craftsmanship (Robert C. Martin Series)")

    def test_simple_get_authors(self):
        api_request = requests.get(url + '/get/authors/' + 'name="rob"').json()
        self.assertEqual(api_request[0]['name'], "Robert C. Martin")

    def test_harder_get_books(self):
        api_request = requests.get(url + '/get/books/' + 'title="the"&title="d"').json()
        self.assertEqual(api_request[0]['title'],
                         "Enterprise Integration Patterns: Designing, Building, and Deploying Messaging Solutions (The Addison-Wesley Signature Series)")

    def test_harder_get_authors(self):
        api_request = requests.get(url + '/get/authors/' + 'name="mal"|name="grant"').json()
        self.assertEqual(api_request[0]['name'], "Adam M. Grant")

    # Tests for checking if the queries and visualizations work
    def test_query1(self):
        api_request = requests.get(url + '/query1').json()
        self.assertEqual(api_request[0][0]['name'], "Robert C. Martin")

    def test_vis1(self):
        api_request = requests.get(url + '/vis1').json()
        self.assertEqual(api_request[0], {'_id': 'Chris Voss', 'rating': 4.4})

    def test_vis2(self):
        api_request = requests.get(url + '/vis2').json()
        self.assertEqual(api_request[0], {'_id':
                                          'I Am Malala: The Girl Who Stood Up for Education and Was Shot by the Taliban',
                                          'review_count': 20651.0})


if __name__ == '__main__':
    unittest.main()