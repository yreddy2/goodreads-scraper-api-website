import time
import json
import random
import Book
import Author

# Holds the data of the books that have been traversed
traversed_books = dict()

# Holds the data of the authors that have been traversed
traversed_authors = dict()

# Holds the number of pages that have been traversed
traversal_count = 0

# Holds the number of pages that need to be traversed
traversal_limit = int(input("Enter Number of Pages to Crawl: "))

# Holds the book that is currently being traversed
# book_id = int(input("Enter Starting Book ID: "))
book_id = '3735293'

# Holds the author that is currently being traversed
author_id = ''

# While loop to continuously traverse through pages
while traversal_count < 5:
    try:
        if book_id not in traversed_books:
            book_info = Book.get_book_info(book_id)
            traversed_books[book_id] = book_info
            author_id = book_info['author']
            if author_id not in traversed_authors:
                author_info = Author.get_author_info(author_id)
                traversed_authors[author_id] = author_info
    except Exception as e:
        print("Could Not Scrape Page")
    finally:
        try:
            similar_book_ids = random.choice(list(traversed_books.values()))['similar_books'] + random.choice(list(traversed_authors.values()))['author_books']
            book_id = similar_book_ids[random.randint(0, len(similar_book_ids))]
        except Exception as e:
            print("Could Not Find Valid Book")
        finally:
            print("Pages Crawled:" + str(traversal_count))
            traversal_count = traversal_count + 1
            time.sleep(random.randint(1, 5))

# Storing the information into a json file
with open('C:/Users/Work/Desktop/CS242/books.json', 'w') as f:
    json.dump(traversed_books, f, indent=2)

with open('C:/Users/Work/Desktop/CS242/authors.json', 'w') as a:
    json.dump(traversed_authors, a, indent=4)

