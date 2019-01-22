from django.conf.urls import re_path
from .views import (
    BookList,
    BookDetails
)

#app_name = 'library'

urlpatterns = [
    re_path('^$', BookList.as_view(), name='book_list'),
    re_path('(?P<pk>\d+)', BookDetails.as_view(), name='book_details'),
    #re_path('category/(?P<slug>[\w\-]+)/$', views.category, name='category')
]