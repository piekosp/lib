import django_filters

from django import forms

from .models import Book, Author


class BookFilter(django_filters.FilterSet):

    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control me-2', 'placeholder': 'Title'})
    )
    author = django_filters.ModelChoiceFilter(
        field_name='author__name',
        to_field_name='name',
        queryset=Author.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    language = django_filters.CharFilter(
        field_name='language',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control me-2', 'placeholder': 'Language'})
    )
    publication_date__gt = django_filters.DateFilter(
        field_name='publication_date',
        lookup_expr='gt',
        widget=forms.TextInput(attrs={'class': 'form-control me-2', 'placeholder': 'Published after'})
    )
    publication_date__lt = django_filters.DateFilter(
        field_name='publication_date',
        lookup_expr='lt',
        widget=forms.TextInput(attrs={'class': 'form-control me-2', 'placeholder': 'Published before'})
    )

    class Meta:
        model = Book
        fields = [
            'title',
            'author',
            'language',
            'publication_date'
        ]


class ApiBookFilter(django_filters.rest_framework.FilterSet):

    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains'
    )
    author = django_filters.ModelChoiceFilter(
        field_name='author__name',
        to_field_name='name',
        queryset=Author.objects.all()
    )
    language = django_filters.CharFilter(
        field_name='language',
        lookup_expr='icontains'
    )
    publication_date__gt = django_filters.DateFilter(
        field_name='publication_date',
        lookup_expr='gt'
    )
    publication_date__lt = django_filters.DateFilter(
        field_name='publication_date',
        lookup_expr='lt'
    )

    class Meta:
        model = Book
        fields = [
            'title',
            'author',
            'language',
            'publication_date'
        ]
