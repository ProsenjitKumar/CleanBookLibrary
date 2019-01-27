from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import SingleObjectMixin
from django.utils import timezone
from django.views.generic import \
    ListView, DetailView
from .models import (
    Book,
    Category,
    Author,
    Language,
    Currency,
    Tag,
)
from django.db.models import Q
from django.views.generic.base import TemplateView


class HomePageView(TemplateView):

    template_name = "books/book_lists.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_articles'] = Book.objects.all()[:5]


class BookList(ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'books/book_lists.html'
    paginate_by = 12
    extra_context = {
        'category_list': Category.objects.all(),
        'author_list': Author.objects.all(),
        'language_list': Language.objects.all(),
    }

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(
                Q(name_of_the_book__icontains=query) |
                Q(author__first_name__icontains=query) |
                Q(category__name__icontains=query)
            )
        else:
            object_list = self.model.objects.all()
        return object_list


class SingleCategoryView(DetailView):
    model = Category
    template_name = 'books/single_category.html'
    paginate_by = 12
    extra_context = {
        'category_list': Category.objects.all(),
        'author_list': Author.objects.all(),
        'language_list': Language.objects.all(),
    }


# class AuthorDetailsView(SingleObjectMixin, ListView):
#     template_name = 'books/author.html'
#     paginate_by = 2
#
#     def get(self, request, *args, **kwargs):
#         self.object = self.get_object(queryset=Author.objects.all())
#         return super().get(request, *args, **kwargs)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['author'] = self.object
#         return context
#
#     def get_queryset(self):
#         return self.object.book_set.all()


class SingleAuthorView(DetailView):
    model = Author
    template_name = 'books/single_author.html'
    extra_context = {
        'category_list': Category.objects.all(),
        'author_list': Author.objects.all(),
        'language_list': Language.objects.all(),
    }


class SingleLanguage(DetailView):
    model = Language
    template_name = 'books/single_language_list.html'
    extra_context = {
        'category_list': Category.objects.all(),
        'author_list': Author.objects.all(),
        'language_list': Language.objects.all(),
    }


class BookDetails(DetailView):
    model = Book
    template_name = 'books/book_details.html'
    # extra_context = {
    #     'category_list': Category.objects.all(),
    #     'author_list': Author.objects.all(),
    #     'language_list': Language.objects.all(),
    # }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context



