from rest_framework import generics

from django.shortcuts import redirect, render
from django.views.generic.edit import DeleteView, CreateView
from django.urls import reverse_lazy

from books.models import Book, Author
from books.forms import BookForm, AuthorFormset, GoogleApiForm
from books.forms import AuthorForm
from books.functions import get_query, get_books_from_google
from books.filters import BookFilter, ApiBookFilter
from books.serializers import BookSerializer


def book_list(request):
    filter = BookFilter(request.GET, queryset=Book.objects.all().prefetch_related('author'))
    books = filter.qs
    context = {'filter': filter, 'books': books}
    return render(request, 'books/book_list.html', context)


def book_add(request):
    
    if request.method == 'GET':
        form = BookForm()
        formset = AuthorFormset()

    elif request.method == 'POST':
        form = BookForm(request.POST)
        formset = AuthorFormset(request.POST)

        print(form.is_valid())
        print(formset.is_valid())
        if form.is_valid() and formset.is_valid():
            book = form.save()
            for inline_form in formset:
                if inline_form.cleaned_data:
                    if len(inline_form.cleaned_data['name']) > 0:
                        author = inline_form.save()
                        book.author.add(author)

            book.save()

            return redirect('book_list')

    context = {'form': form, 'formset': formset}
    return render(request, 'books/book_add.html', context)


def book_edit(request, pk):

    book = Book.objects.get(id=pk)
    initial = [{'name': author.name} for author in book.author.all()]

    if request.method == 'GET':
        form = BookForm(instance=book)
        formset = AuthorFormset(initial=initial)

    elif request.method == 'POST': 
        form = BookForm(request.POST, instance=book)
        formset = AuthorFormset(request.POST, initial=initial)

        if form.is_valid() and formset.is_valid():
            book = form.save()
            book.author.clear()
            for inline_form in formset:
                if inline_form.cleaned_data:
                    if len(inline_form.cleaned_data['name']) > 0:
                        author = inline_form.save()
                        book.author.add(author)

            book.save()
            
            return redirect('book_list')

    context = {'form': form, 'formset': formset}
    return render(request, 'books/book_edit.html', context)


class BookDeleteView(DeleteView):
    model = Book
    success_url = reverse_lazy('book_list')


def book_import(request):

    if request.method == 'GET':
        form = GoogleApiForm()

    elif request.method == 'POST':
        form = GoogleApiForm(request.POST)
        if form.is_valid():
            query = get_query(**form.cleaned_data)
            get_books_from_google(query)
        return redirect('book_list')

    return render(request, 'books/book_import.html', {'form': form})


class AuthorCreateView(CreateView):
    model = Author
    template_name_suffix = '_add'
    form_class = AuthorForm
    success_url = reverse_lazy('book_list')


class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filterset_class = ApiBookFilter
