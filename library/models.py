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

    def __str__(self):
        return self.currency


class Language(models.Model):
    language = models.CharField(max_length=50)

    def __str__(self):
        return self.language


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    # def get_absolute_url(self):
    #     """Returns the url to access a particular author instance."""
    #     return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Book(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    image = models.ImageField(upload_to='book_photos/', blank=False, null=False)
    publisher = models.CharField(max_length=255)
    author = models.ManyToManyField(Author, help_text='Select Author name')
    translation = models.ManyToManyField(Language, related_name='languages', help_text='Select Language')
    edition = models.IntegerField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    copy = models.PositiveSmallIntegerField()
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    category = models.ManyToManyField(Category, help_text='Select category for this book')
    published = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField()
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    publish = models.BooleanField(default=True)
    objects = EntryQuerySet.as_manager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Book, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

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

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f'{self.id} ({self.book.title})'


