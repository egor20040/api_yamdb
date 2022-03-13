from django.db import models

from reviews.validators import validate_year
from reviews.validators import validate_score
from users.models import User


class Category(models.Model):
    name = models.CharField(
        verbose_name='Категория',
        help_text='Название категории',
        max_length=128,
        unique=True
    )
    slug = models.SlugField(
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Жанр',
        help_text='Название жанра',
        max_length=128,
        unique=True
    )
    slug = models.SlugField(
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)


class Title(models.Model):
    name = models.CharField(
        verbose_name='Наименование',
        help_text='Наименование произведения',
        max_length=128
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        help_text='Жанр произведения',
        related_name='titles',
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        help_text='Категория выбранного произведения',
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True
    )
    year = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        db_index=True,
        validators=(validate_year,),
        verbose_name='Дата публикации'
    )
    description = models.CharField(
        verbose_name='Описание',
        help_text='Описание произведения',
        max_length=256,
        blank=True,
    )

    rating = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        help_text='Рейтинг произведения',
        null=True,
        validators=(validate_score,),
        blank=True,
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        help_text='Произведение к которому относится отзыв',
        related_name='review',
        verbose_name='Произведение'
    )
    score = models.PositiveSmallIntegerField(
        help_text='Новая оценка',
        verbose_name='Оценка произведения',
        validators=(validate_score,),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='review'
    )
    text = models.TextField(
        help_text='Текст нового отзывы',
        verbose_name='Текст отзыва'
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ('score',)
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='uniq_author',
            ),
        )

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        help_text='Произведение к которому относится коментарий',
        related_name='comments',
        verbose_name='Произведение'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
        help_text='Автор который оставил коментарий',
    )
    text = models.TextField(
        help_text='Текст нового коментария',
        verbose_name='Коментарий'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text='Дата добавления нового коментария',
        verbose_name='Дата'
    )

    class Meta:
        ordering = ('pub_date',)

    def __str__(self):
        return self.text[:15]
