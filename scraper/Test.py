import unittest
import Book
import Author


class TestCalc(unittest.TestCase):

    # Tests for getting the information of the authors.
    def test_author_name(self):
        author_info = Author.get_author_info("45372")
        self.assertEqual(author_info['author_id'], "45372")
        
    def test_author_url(self):
        author_info = Author.get_author_info("45372")
        self.assertEqual(author_info['author_url'], "https://www.goodreads.com/author/show/45372")

    def test_author_id(self):
        author_info = Author.get_author_info("45372")
        self.assertEqual(author_info['author_id'], "45372")

    def test_author_rating(self):
        author_info = Author.get_author_info("45372")
        self.assertEqual(author_info['rating'], "4.34")

    def test_author_rating_count(self):
        author_info = Author.get_author_info("45372")
        self.assertEqual(author_info['rating_count'], "27069")

    def test_author_review_count(self):
        author_info = Author.get_author_info("45372")
        self.assertEqual(author_info['review_count'], "1767")

    def test_author_image_url(self):
        author_info = Author.get_author_info("45372")
        self.assertEqual(author_info['image_url'], "https://images.gr-assets.com/authors/1490470967p5/45372.jpg")

    def test_author_related_authors(self):
        author_info = Author.get_author_info("45372")
        self.assertEqual(author_info['related_authors'][0], "2815")

    def test_author_author_books(self):
        author_info = Author.get_author_info("45372")
        self.assertEqual(author_info['author_books'][0], "3735293")

    # Tests for getting the information of the books.
    def test_book_url(self):
        book_info = Book.get_book_info("3735293")
        self.assertEqual(book_info['book_url'], "https://www.goodreads.com/book/show/3735293")

    def test_book_title(self):
        book_info = Book.get_book_info("3735293")
        self.assertEqual(book_info['title'], "Clean Code: A Handbook of Agile Software Craftsmanship (Robert C. Martin Series)")

    def test_book_id(self):
        book_info = Book.get_book_info("3735293")
        self.assertEqual(book_info['book_id'], "3735293")

    def test_book_ISBN(self):
        book_info = Book.get_book_info("3735293")
        self.assertEqual(book_info['ISBN'], "0132350882")

    def test_book_rating(self):
        book_info = Book.get_book_info("3735293")
        self.assertEqual(book_info['rating'], "4.40")

    def test_book_rating_count(self):
        book_info = Book.get_book_info("3735293")
        self.assertEqual(book_info['rating_count'], "14922")

    def test_book_review_count(self):
        book_info = Book.get_book_info("3735293")
        self.assertEqual(book_info['review_count'], "877")

    def test_book_image_url(self):
        book_info = Book.get_book_info("3735293")
        self.assertEqual(book_info['image_url'], "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1436202607l/3735293._SX318_.jpg")

    def test_book_similar_books(self):
        book_info = Book.get_book_info("3735293")
        self.assertEqual(book_info['similar_books'][0], "85009")


if __name__ == '__main__':
    unittest.main()
