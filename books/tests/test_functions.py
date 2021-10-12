from django.test import TestCase

from books.functions import get_query, get_books_from_google
from books.functions import validate_pages, validate_image_url
from books.functions import validate_authors, validate_date
from books.functions import validate_isbn, validate_language
from books.functions import validate_title
from books.models import Book


class TestPagesValidator(TestCase):

    def test_no_pages_in_response(self):
        info = {}
        self.assertEqual(validate_pages(info), None)

    def test_pages_in_response(self):
        info = {'pageCount': 20}
        self.assertEqual(validate_pages(info), 20)


class TestImageUrlValidator(TestCase):

    def test_no_image_url_in_response(self):
        info = {}
        self.assertEqual(validate_image_url(info), None)

    def test_small_thumbnail_in_response(self):
        info = {
            'imageLinks':
            {
                'smallThumbnail': 'small_image',
            },
        }
        self.assertEqual(validate_image_url(info), 'small_image')

    def test_thumbnail_in_respone(self):
        info = {
            'imageLinks':
            {
                'thumbnail': 'image',
            },
        }
        self.assertEqual(validate_image_url(info), 'image')

    def test_both_images_in_response(self):
        info = {
            'imageLinks':
            {
                'thumbnail': 'image',
                'smallThumbnail': 'small_image',
            },
        }
        self.assertEqual(validate_image_url(info), 'image')


class TestAuthorValidator(TestCase):

    def test_no_authors_in_response(self):
        info = {}
        self.assertEqual(validate_authors(info), [])

    def test_authors_in_response(self):
        info = {
            'authors': ['J. K. Rownling', 'Dan Brown']
        }
        self.assertEqual(
            validate_authors(info),
            ['J. K. Rownling', 'Dan Brown']
        )


class TestDateValidator(TestCase):

    def test_no_date_in_response(self):
        info = {}
        self.assertEqual(validate_date(info), None)

    def test_full_date_in_response(self):
        info = {
            'publishedDate': '2020-05-07'
        }
        self.assertEqual(validate_date(info), '2020-05-07')

    def test_year_and_month_in_response(self):
        info = {
            'publishedDate': '2020-05'
        }
        self.assertEqual(validate_date(info), '2020-05-01')

    def test_year_in_response(self):
        info = {
            'publishedDate': '2020'
        }
        self.assertEqual(validate_date(info), '2020-01-01')


class TestISBNValidator(TestCase):

    def test_no_isbn_in_response(self):
        info = {}
        self.assertEqual(validate_isbn(info), None)

    def test_skip_non_isbn_identifier(self):
        info = {
            'industryIdentifiers':
            [
                {
                    'type': 'UPIC',
                    'identifier': '2837469'
                }
            ]
        }
        self.assertEqual(validate_isbn(info), None)

    def test_two_types_of_isbn_in_respone(self):
        info = {
            'industryIdentifiers':
            [
                {
                    'type': 'ISBN-10',
                    'identifier': '1234567890'
                },
                {
                    'type': 'ISBN-13',
                    'identifier': '1234567890123'
                }
            ]
        }
        self.assertEqual(validate_isbn(info), 1234567890123)

    def test_non_numerical_isbn(self):
        info = {
            'industryIdentifiers':
            [
                {
                    'type': 'ISBN-13',
                    'identifier': 'AB34567890123'
                }
            ]
        }
        self.assertEqual(validate_isbn(info), None)


class TestLanguageValidator(TestCase):

    def test_no_language_in_response(self):
        info = {}
        self.assertEqual(validate_language(info), None)

    def test_language_in_response(self):
        info = {
            'language': 'en'
        }
        self.assertEqual(validate_language(info), 'en')


class TestTitleValidator(TestCase):

    def test_no_title_in_response(self):
        info = {}
        self.assertEqual(validate_title(info), None)

    def test_title_in_response(self):
        info = {
            'title': 'Harry Potter And The Goblet Of Fire'
        }
        self.assertEqual(
            validate_title(info),
            'Harry Potter And The Goblet Of Fire'
        )


class TestQueryBuilder(TestCase):

    def test_queries(self):
        self.assertEqual(
            get_query(
                key_word='A',
                title='B',
                author='C',
                isbn='D'
            ),
            'https://www.googleapis.com/books/v1/volumes?q=' +
            'A+intitle:B+inauthor:C+isbn:D'
        )
        self.assertEqual(
            get_query(
                key_word='',
                title='B',
                author='C',
                isbn='D'
            ),
            'https://www.googleapis.com/books/v1/volumes?q=' +
            '+intitle:B+inauthor:C+isbn:D'
        )
        self.assertEqual(
            get_query(
                key_word='A',
                title='',
                author='C',
                isbn='D'
            ),
            'https://www.googleapis.com/books/v1/volumes?q=' +
            'A+inauthor:C+isbn:D'
        )
        self.assertEqual(
            get_query(
                key_word='A',
                title='B',
                author='',
                isbn='D'
            ),
            'https://www.googleapis.com/books/v1/volumes?q=' +
            'A+intitle:B+isbn:D'
        )
        self.assertEqual(
            get_query(
                key_word='A',
                title='B',
                author='C',
                isbn=''
            ),
            'https://www.googleapis.com/books/v1/volumes?q=' +
            'A+intitle:B+inauthor:C'
        )


class TestBookImport(TestCase):

    def setUp(self):
        self.query = (
            'https://www.googleapis.com/books/v1/' +
            'volumes?q=Harry Potter'   
        )
  
    def test_books_imported(self):
        imported_books = get_books_from_google(self.query)
        created_books = Book.objects.all().count()
        self.assertEqual(imported_books, created_books)