from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from titles.models import Title

User = get_user_model()


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        verbose_name='Обозреваемое наименование', related_name='reviews'
    )
    text = models.TextField(max_length=10000, verbose_name='Текст обзора')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор обзора')
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Рейтинг обзора'
    )
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата публикации обзора')

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, verbose_name='Обзор',
        related_name='comments'
    )
    text = models.TextField(max_length=1000, verbose_name='Текст коментария')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор коментария')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата коментария')

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
