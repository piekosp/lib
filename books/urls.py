from django.urls import path

from books import views


urlpatterns = [
    path('', views.home_view, name='home_view'),
    path('books/list/', views.book_list, name='book_list'),
    path('books/edit/<uuid:pk>/', views.book_edit, name='book_edit'),
    path('books/delete/<uuid:pk>/', views.BookDeleteView.as_view(), name='book_delete'),
    path('books/import/', views.book_import, name='book_import'),
    path('books/add/', views.book_add, name='book_add'),
    path('books/author/add', views.AuthorCreateView.as_view(), name='author_add'),
    path('api/', views.BookList.as_view(), name='BookList')
]