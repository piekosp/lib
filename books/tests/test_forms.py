from django.test import TestCase

from books.forms import AuthorForm, BookForm, GoogleApiForm, AuthorFormset
from books.models import Author


class AuthorFormTest(TestCase):

    def test_form_valid_data(self):
        form = AuthorForm(data={'name': 'J. K. Rowling'})
        self.assertTrue(form.is_valid())


class BookFormTest(TestCase):

    def setUp(self):
        self.data = {
            'title': 'Harry Potter And The Goblet Of Fire',
            'publication_date': '2000-07-08',
            'isbn': '9780439139595',
            'pages': '636',
            'image_url': ('https://media.libris.to/jacket/'
                          '02676349_harry-potter-and-the-goblet-of-fire.jpg'),
            'language': 'en'
        }

    # def test_form_valid_data(self):
    #     form = BookForm(data=self.data)
    #     self.assertTrue(form.is_valid())

    def test_form_invalid_title(self):
        self.data['title'] = ''
        form = BookForm(data=self.data)
        self.assertFalse(form.is_valid())

    def test_form_invalid_pub_date(self):
        self.data['publication_date'] = '2007'
        form = BookForm(data=self.data)
        self.assertFalse(form.is_valid())

    def test_form_invalid_isbn(self):
        self.data['isbn'] = '12345'
        form = BookForm(data=self.data)
        self.assertFalse(form.is_valid())

    def test_form_invalid_pages(self):
        self.data['pages'] = 'a'
        form = BookForm(data=self.data)
        self.assertFalse(form.is_valid())

    def test_form_invalid_image_url(self):
        self.data['image_url'] = (
            'jacket/02676349_harry-potter-and-the-goblet-of-fire.jpg'
        )
        form = BookForm(data=self.data)
        self.assertFalse(form.is_valid())


class BookEditFormTest(TestCase):

    def setUp(self):
        Author.objects.create(name='J. K. Rownling')
        Author.objects.create(name='Dan Brown')
        Author.objects.create(name='George R. R. Martin')
        self.data = {
            'title': 'Harry Potter And The Goblet Of Fire',
            'publication_date': '2000-07-08',
            'isbn': '9780439139595',
            'pages': '636',
            'image_url': ('https://media.libris.to/jacket/'
                          '02676349_harry-potter-and-the-goblet-of-fire.jpg'),
            'language': 'en'
        }

    def test_form_one_author(self):
        author = Author.objects.get(id=1)
        self.data['author'] = [author.pk]
        form = BookForm(self.data)
        self.assertTrue(form.is_valid())
     
    def test_form_multiple_authors(self):
        author_1 = Author.objects.get(id=1)
        author_2 = Author.objects.get(id=2)
        author_3 = Author.objects.get(id=3)
        self.data['author'] = [author_1.pk, author_2.pk, author_3.pk]
        form = BookForm(self.data)
        self.assertTrue(form.is_valid())


class AuthorFormsetTest(TestCase):

    def setUp(self):
        self.data = {
            'form-TOTAL_FORMS': '3',
            'form-INITIAL_FORMS': '0',
            'form-0-name': 'J. K. Rownling',
            'form-1-name': 'Dan Brown',
            'form-2-name': 'George R. R. Martin',
        }

    def test_from(self):
        formset = AuthorFormset(data=self.data)
        self.assertTrue(formset.is_valid())


class GoogleApiFormTest(TestCase):

    def setUp(self):
        self.data = {
            'key_word': 'Harry Potter',
            'title': 'Harry Potter And The Goblet Of Fire',
            'author': 'J. K. Rownling',
            'isbn': '9780439139595',
        }

    def test_form_is_valid(self):
        form = GoogleApiForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_from_no_key_word(self):
        self.data['key_word'] = ''
        form = GoogleApiForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_form_no_title(self):
        self.data['title'] = ''
        form = GoogleApiForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_form_no_author(self):
        self.data['author'] = ''
        form = GoogleApiForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_form_no_isbn(self):
        self.data['isbn'] = ''
        form = GoogleApiForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_form_fields_length(self):
        form = GoogleApiForm()
        self.assertEqual(form.fields['key_word'].max_length, 100)
        self.assertEqual(form.fields['title'].max_length, 100)
        self.assertEqual(form.fields['author'].max_length, 100)
        self.assertEqual(form.fields['isbn'].max_length, 13)