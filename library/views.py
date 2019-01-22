from django.shortcuts import render
from django.views.generic import \
    ListView, DetailView
from .models import Book, Category
from django.db.models import Q


class BookList(ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'books/book_lists.html'
    paginate_by = 12
    # extra_context = {
    #     'category_list': Category.objects.all(),
    # }
    ordering = ['-published']

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(
                Q(title__icontains=query) |
                Q(author__first_name__contains=query) |
                #Q(author__last_name__icontains=query) |
                Q(category__name__icontains=query)
            )
        else:
            object_list = self.model.objects.all()
        return object_list

    # def get(self, request, *args, **kwargs):
    #     category = Category.objects.filter(book__category__exact=request.GET.get('name'))
    #     return category


class BookDetails(DetailView):
    model = Book
    template_name = 'books/book_details.html'


