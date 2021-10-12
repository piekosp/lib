from django.test import TestCase
from django.urls import reverse

from books.models import Book, Author


class TestBookListView(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.book_1 = Book.objects.create(
            title = 'The Da Vinci Code',
        )
        cls.book_2 = Book.objects.create(
            title = 'Harry Potter And The Goblet Of Fire'
        )

    def test_view_url_exists(self):
        response = self.client.get('/books/list/')
        self.assertEqual(response.status_code, 200)

    def test_view_accesible_by_name(self):
        url = reverse('book_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        url = reverse('book_list')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'books/book_list.html')

    def test_view_list_all_books(self):
        url = reverse('book_list')
        response = self.client.get(url)
        self.assertIn(self.book_1, response.context['books'])
        self.assertIn(self.book_2, response.context['books'])

    def test_view_filters_books(self):
        url = reverse('book_list')
        response = self.client.get(url, {'title': 'Vinci'})
        self.assertIn(self.book_1, response.context['books'])
        self.assertNotIn(self.book_2, response.context['books'])


class TestBookAddView(TestCase):

    def test_view_url_exists(self):
        response = self.client.get('/books/add/')
        self.assertEqual(response.status_code, 200)

    def test_view_accesible_by_name(self):
        url = reverse('book_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        url = reverse('book_add')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'books/book_add.html')

    def test_view_adds_book_and_author(self):
        url = '/books/add/'
        data = {
            'form-TOTAL_FORMS': '3',
            'form-INITIAL_FORMS': '0',
            'form-0-name': 'Dan Brown',
            'title': 'The Da Vinci Code',
        }
        response = self.client.post(url, data)
        book = Book.objects.all()[0]
        author = Author.objects.get(pk=1)
        book_author = book.author.all()[0]
        self.assertEqual(book.title, 'The Da Vinci Code')
        self.assertEqual(author.name, 'Dan Brown')
        self.assertEqual(author, book_author)
        self.assertRedirects(response, reverse('book_list'))


class TestBookEditView(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.book = Book.objects.create(
            title = 'The Da Vinci Code',
        )    

    def test_view_url_exists(self):
        response = self.client.get(f'/books/edit/{self.book.pk}/')
        self.assertEqual(response.status_code, 200)

    def test_view_accesible_by_name(self):
        url = reverse('book_edit', kwargs={'pk': self.book.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        url = reverse('book_edit', kwargs={'pk': self.book.pk})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'books/book_edit.html')

    def test_view_edit_book(self):
        url = reverse('book_edit', kwargs={'pk': self.book.pk})
        data = {
            'form-TOTAL_FORMS': '3',
            'form-INITIAL_FORMS': '0',
            'form-0-name': 'J. K. Rownling',
            'title': 'Harry Potter'
        }
        response = self.client.post(url, data)
        edited_book = Book.objects.get(id=self.book.id)
        self.assertRedirects(response, reverse('book_list'))
        self.assertEqual(edited_book.title, 'Harry Potter')


class TestBookDeleteView(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.book = Book.objects.create(
            title = 'The Da Vinci Code',
        )

    def test_view_url_exists(self):
        response = self.client.get(f'/books/delete/{self.book.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Are you sure you want to delete')

    def test_view_accesible_by_name(self):
        url = reverse('book_delete', kwargs={'pk': self.book.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Are you sure you want to delete')

    def test_view_uses_correct_template(self):
        url = reverse('book_delete', kwargs={'pk': self.book.pk})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'books/book_confirm_delete.html')

    def test_view_delete_book(self):
        url = reverse('book_delete', kwargs={'pk': self.book.pk})
        self.client.post(url)
        self.assertEqual(Book.objects.count(), 0)


class TestBookImportView(TestCase):

    def test_view_url_exists(self):
        response = self.client.get(f'/books/import/')
        self.assertEqual(response.status_code, 200)

    def test_view_accesible_by_name(self):
        url = reverse('book_import')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        url = reverse('book_import')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'books/book_import.html')

    def test_view_creates_books(self):
        url = reverse('book_import')
        data = {
            'key_word': 'Da Vinci',
            'title': 'The Da Vinci Code'
        }
        self.client.post(url, data)
        self.assertGreater(Book.objects.count(), 0)

    def test_view_no_books_to_import(self):
        url = reverse('book_import')
        data = {
            'key_word': 'Da Vinci',
            'title': 'Goblet Of Fire',
            'author': 'George R. R. Martin',
            'isbn': '123254675423'
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('book_list'))


class TestAuthorCreateView(TestCase):

    def test_view_url_exists(self):
        response = self.client.get(f'/books/author/add')
        self.assertEqual(response.status_code, 200)

    def test_view_accesible_by_name(self):
        url = reverse('author_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        url = reverse('author_add')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'books/author_add.html')

    def test_view_author_create(self):
        url = reverse('author_add')
        data = {'name': 'Dan Brown'}
        response = self.client.post(url, data)
        author = Author.objects.get(pk=1)
        self.assertRedirects(response, reverse('book_list'))
        self.assertEqual(author.name, 'Dan Brown')