from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic import \
    ListView, DetailView
from .models import Book, Category
from django.db.models import Q


class BookList(ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'books/book_lists.html'
    paginate_by = 12
    extra_context = {
        'category_list': Category.objects.all(),
    }
    ordering = ['-published']

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(
                Q(title__icontains=query) |
                Q(author__first_name__contains=query) |
                Q(category__name__icontains=query)
            )
        else:
            object_list = self.model.objects.all()
        return object_list

    # def get_context_data(self, **kwargs):
    #     context = super(BookList, self).get_context_data(**kwargs)
    #     books = Book.objects.all() # show all by default
    #     # Check if the request had a GET query parameter with name 'cat'
    #     cat = self.request.GET.get('cat', None)
    #     if cat:
    #         # yes, then show only that given categories products
    #         books = books.filter(category=cat)
    #         return books


class SingleCategoryView(DetailView):
    model = Category
    template_name = 'books/single_category.html'
    extra_context = {
        'category_list': Category.objects.all(),
        #'book_lists': DetailView(Book),
    }


class BookDetails(DetailView):
    model = Book
    template_name = 'books/book_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


