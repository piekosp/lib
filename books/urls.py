from django.urls import path

from books import views


urlpatterns = [
    path('list/', views.book_list, name='book_list'),
    path('edit/<uuid:pk>/', views.book_edit, name='book_edit'),
    path('delete/<uuid:pk>/', views.BookDeleteView.as_view(), name='book_delete'),
    path('import/', views.book_import, name='book_import'),
    path('add/', views.book_add, name='book_add'),
    path('author/add', views.AuthorCreateView.as_view(), name='author_add'),
    path('api/', views.BookList.as_view(), name='BookList')
]