from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date

class Genre(models.Model):
    name = models.CharField(max_length=20, help_text = "Введите жанр книги", verbose_name="Жанр книги")

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=20, help_text="Введите язык книги", verbose_name="Язык книги")

    def __str__(self):
        return self.name

class Author(models.Model):
    first_name = models.CharField(max_length=100, help_text="Введите имя автора", verbose_name="Имя автора")
    last_name = models.CharField(max_length=100, help_text="Введите фамилию автора", verbose_name="Фамилия автора")
    date_of_birth = models.DateField(help_text="Введите дату рождения", verbose_name="Дата рождения", null=True, blank=True)
    date_of_death = models.DateField(help_text="Введите дату смерти", verbose_name="Дата смерти", null=True, blank=True)

    def __str__(self):
        return self.last_name

class Book(models.Model):
    title = models.CharField(max_length=200, help_text="Введите название книги", verbose_name="Название книги")
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE, max_length=30, help_text="Введите название жанра для книги", verbose_name="Название жанра", null=True)
    language = models.ForeignKey('language', on_delete=models.CASCADE, help_text="Введите язык книги", verbose_name="Язык книги", null=True)
    author = models.ManyToManyField('Author', help_text="Введите автора книги", verbose_name="Автор книги")
    summary = models.TextField(max_length=100, help_text="Введите краткое содержание книги", verbose_name="Описание книги")
    isbn = models.CharField(max_length=13, help_text="Введите ISBN книги", verbose_name="ISBN книги!")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def display_author(self):
        return ', '.join([author.last_name for author in self.author.all()])

    display_author.short_description = 'Авторы'

class Status(models.Model):
    name = models.CharField(max_length=20, help_text="Введите статус книги", verbose_name="Статус книги")

    def __str__(self):
        return self.name

class BookInstance(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, null=True)
    inv_nom = models.CharField(max_length=20, null=True, help_text="Введите инвентарный номер экземпляра", verbose_name="Инвентарный номер")
    imprint = models.CharField(max_length=200, help_text="Введите издательство и год выпуска", verbose_name="Издательство")
    status = models.ForeignKey('Status', on_delete=models.CASCADE, null=True, help_text="Изменить статус экземпляра книги", verbose_name="Статус экземпляра книги")
    due_back = models.DateField(null=True, blank=True, help_text="Введите конец срока статуса", verbose_name="Дата окончания статуса")
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Заказчик", help_text="Выберите заказчика книги")

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    def __str__(self):
        return '%s %s %s' % (self.inv_nom, self.book, self.status)
