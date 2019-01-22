from django.shortcuts import render
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
    # extra_context = {
    #     'category_list': Category.objects.all(),
    # }
    ordering = ['published']

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

    # def get(self, request, *args, **kwargs):
    #     # Create a context dictionary which we can pass to the template rendering engine.
    #     context_dict = {}
    #     try:
    #         # Can we find a category name slug with the given name?
    #         # If we can't, the .get() method raises a DoesNotExist exception.
    #         # So the .get() method returns one model instance or raises an exception.
    #         category = Category.objects.get(slug=self)
    #         context_dict['category_name'] = category.name
    #         context_dict['category'] = category
    #     except Category.DoesNotExist:
    #         # We get here if we didn't find the specified category.
    #         # Don't do anything - the template displays the "no category" message for us.
    #         pass
    #     # Go render the response and return it to the client.
    #     return render(request, 'books/book_lists.html', context_dict)


class BookDetails(DetailView):
    model = Book
    template_name = 'books/book_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


