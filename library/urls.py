from django.conf.urls import re_path
from .views import (
    BookList,
    BookDetails,
    SingleCategoryView,
)

#app_name = 'library'

urlpatterns = [
    re_path('^$', BookList.as_view(), name='book_list'),
    re_path('(?P<pk>\d+)/', BookDetails.as_view(), name='book_details'),
    re_path('(?P<pk>\d+)$', SingleCategoryView.as_view(), name='single_category_details'),
    #re_path(<slug:slug>'category/(?P<slug>[\w\-]+)/$', views.category, name='category')
]