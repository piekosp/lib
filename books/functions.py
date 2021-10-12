import requests

from .models import Book, Author

def get_query(key_word='', title='', author='', isbn=''):

    query = f"https://www.googleapis.com/books/v1/volumes?q={key_word}"

    if len(title):
        query += f'+intitle:{title}'

    if len(author):
        query += f'+inauthor:{author}'

    if len(isbn):
        query += f'+isbn:{isbn}'

    return query


def validate_title(info):
    if 'title' in info:
        return info['title']


def validate_authors(info):
    authors_list = []
    if 'authors' in info:
        for author in info['authors']:
            authors_list.append(author)
    return authors_list


def validate_date(info):
    if 'publishedDate' in info:
        date = info['publishedDate']
        if len(date) == 10:
            return date
        elif len(date) == 7:
            return date + '-01'
        else:
            return date + '-01-01'


def validate_isbn(info):
    if 'industryIdentifiers' in info:
        identifier = ''
        for id in info['industryIdentifiers']:
            if len(id['identifier']) > len(identifier) and 'ISBN' in id['type']:
                identifier = id['identifier']
        try:
            return int(identifier)
        except ValueError:
            return None


def validate_language(info):
    if 'language' in info:
        return info['language']


def validate_image_url(info):
    if 'imageLinks' in info:
        if 'thumbnail' in info['imageLinks']:
            return info['imageLinks']['thumbnail']
        elif 'smallThumbnail' in info['imageLinks']:
            return info['imageLinks']['smallThumbnail']


def validate_pages(info):
    if 'pageCount' in info:
        return info['pageCount']
    

def get_books_from_google(query):

    r = requests.get(query)
    response = r.json()
    imported_books = 0

    if response['totalItems']:
        for item in response['items']:
            item_info = item['volumeInfo']
            title = validate_title(item_info)
            date = validate_date(item_info)
            authors_list = validate_authors(item_info)
            isbn = validate_isbn(item_info)
            language = validate_language(item_info)
            image_url = validate_image_url(item_info)
            pages = validate_pages(item_info)
            
            if isbn is not None and title is not None:
                if not Book.objects.filter(isbn=isbn).exists():
                    book = Book.objects.create(
                        title=title,
                        publication_date=date,
                        isbn=isbn,
                        pages=pages,
                        image_url=image_url,
                        language=language
                    )                  
                    book.save()

                    imported_books += 1

                    for author_name in authors_list:
                        try:
                            author = Author.objects.get(name=author_name)
                        except Author.DoesNotExist:
                            author = Author.objects.create(name=author_name)

                        book.author.add(author)
                    book.save()
    return imported_books