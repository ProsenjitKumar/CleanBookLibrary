import uuid
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class EntryQuerySet(models.QuerySet):
    def published(self):
        return self.filter(publish=True)


class Category(models.Model):
    name = models.CharField(max_length=200, help_text='Enter a book Category (e.g. Science Fiction)')
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        # Uncomment if you don't want the slug to change every time the name changes
        # if self.id is None:
        # self.slug = slugify(self.name)
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Currency(models.Model):
    currency = models.CharField(max_length=10)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.currency)
        super(Currency, self).save(*args, **kwargs)

    def __str__(self):
        return self.currency


class Language(models.Model):
    language = models.CharField(max_length=50)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.language)
        super(Language, self).save(*args, **kwargs)

    def __str__(self):
        return self.language


class Editor(models.Model):
    editor = models.CharField(max_length=190)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.editor)
        super(Editor, self).save(*args, **kwargs)

    def __str__(self):
        return self.editor


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.first_name, self.last_name)
        super(Author, self).save(*args, **kwargs)

    class Meta:
        ordering = ['last_name', 'first_name']

    # def get_absolute_url(self):
    #     """Returns the url to access a particular author instance."""
    #     return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Book(models.Model):
    name_of_the_book = models.CharField(max_length=200)
    edition = models.CharField(max_length=13)
    author = models.ManyToManyField(Author, help_text='Select Author name')
    editor = models.ManyToManyField(Editor, help_text='Select Editor name')
    translator = models.ManyToManyField(Language, related_name='languages', help_text='Select Language')
    publisher = models.CharField(max_length=255)
    place = models.CharField(max_length=190)
    month = models.CharField(max_length=20)
    year = models.IntegerField()
    isbn = models.CharField('ISBN', max_length=13,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>',
                            blank=True, null=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    price = models.IntegerField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, help_text='Select category for this book')
    pages = models.IntegerField()
    copy = models.PositiveSmallIntegerField(blank=True, null=True)
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    image = models.ImageField(upload_to='book_photos/', blank=True, null=True)
    published = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField()
    publish = models.BooleanField(default=True)
    objects = EntryQuerySet.as_manager()

    class Meta:
        ordering = ["-published"]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name_of_the_book)
        super(Book, self).save(*args, **kwargs)

    def __str__(self):
        return self.name_of_the_book

    # def get_absolute_url(self):
    #     return "/book_list/%s/" %(self.id)

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book_details', args=[str(self.id)])


# Declare the ForeignKey with related_query_name
class Tag(models.Model):
    article = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="tags",
        related_query_name="tag",
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.imprint)
        super(BookInstance, self).save(*args, **kwargs)

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f'{self.id} ({self.book.title})'


