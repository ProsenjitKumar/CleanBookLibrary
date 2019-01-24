from django.contrib import admin
from .models import (
    Category,
    Author,
    Book,
    BookInstance,
    Currency,
    Language,
    Tag,
)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    prepopulated_fields = {'slug':('name',)}


admin.site.register(Category, CategoryAdmin)


class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'isbn', 'published', 'publisher']
    search_fields = ['title', 'isbn']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Book, BookAdmin)


class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ['id', 'imprint', 'due_back']
    prepopulated_fields = {'slug': ('imprint',)}


admin.site.register(BookInstance, BookInstanceAdmin)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name']
    search_fields = ['first_name', 'last_name']
    prepopulated_fields = {'slug': ('first_name', 'last_name',)}


admin.site.register(Author, AuthorAdmin)


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['currency']
    search_fields = ['currency']
    prepopulated_fields = {'slug': ('currency',)}


admin.site.register(Currency, CurrencyAdmin)


class LanguageAdmin(admin.ModelAdmin):
    list_display = ['language']
    search_fields = ['language']
    prepopulated_fields = {'slug': ('language',)}


admin.site.register(Language, LanguageAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Tag, TagAdmin)

