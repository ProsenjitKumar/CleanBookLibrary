from django.conf.urls import re_path
from .views import (
    BookList,
    BookDetails,
    SingleCategoryView,
    SingleAuthorView,
    SingleLanguage,
    #AuthorDetailsView,
)

app_name = 'library'

urlpatterns = [
    re_path('^$', BookList.as_view(), name='book_list'),
    re_path('books/(?P<slug>[-\w]+)', BookDetails.as_view(), name='book_details'),
    re_path('category/(?P<slug>[-\w]+)', SingleCategoryView.as_view(), name='single_category_details'),
    re_path('author/(?P<slug>[-\w]+)', SingleAuthorView.as_view(), name='single_author_details'),
    re_path('language/(?P<slug>[-\w]+)', SingleLanguage.as_view(), name='single_language_list'),
    #re_path('author-detail/', AuthorDetailsView.as_view(), name='author_detail_view'),
]