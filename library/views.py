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

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(title__icontains=query)
        else:
            object_list = self.model.objects.all()
        return object_list


class BookDetails(DetailView):
    model = Book
    template_name = 'books/book_details.html'


