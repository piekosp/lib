from django import forms
from django.core.exceptions import ValidationError
from .models import Book, Author


class BookForm(forms.ModelForm):

    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Title'}))
    publication_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'input', 'placeholder': 'Publication date'}), required=False)
    isbn = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'input', 'placeholder': 'ISBN'}), required=False)
    pages = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'input', 'placeholder': 'Pages'}), required=False)
    image_url = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Image URL'}), required=False)
    language = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Language'}), required=False)

    class Meta:
        model = Book
        fields = [
            'title',
            'publication_date',
            'isbn',
            'pages',
            'image_url',
            'language'
        ]


    def clean(self):
        cd = super().clean()
        if 'pages' in cd:
            if cd['pages'] is not None:
                if cd['pages'] < 0:
                    raise ValidationError({'pages': ['Pages number cannot be less then 0']})
        return cd


class AuthorForm(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Author name'}), label='', required=False)

    class Meta:
        model = Author
        fields = ['name']


AuthorFormset = forms.formset_factory(AuthorForm, extra=3, max_num=3)


class GoogleApiForm(forms.Form):
    key_word = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Key word'}), max_length=100, required=False)
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Title'}), max_length=100, required=False)
    author= forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Author'}), max_length=100, required=False)
    isbn = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'ISBN'}), max_length=13, required=False)

