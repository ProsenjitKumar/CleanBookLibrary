from django.shortcuts import render
from django.views.generic import \
    ListView, DetailView
from .models import (
    Category,
    BookInstance,
    Book,
    Author,
)


class BookList(ListView):
    model = Book
    template_name = 'books/book_lists.html'
    paginate_by = 12
    ordering = ['-published']


class BookDetails(DetailView):
    model = Book
    template_name = 'books/book_details.html'


