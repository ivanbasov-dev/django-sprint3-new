from django.contrib.auth import get_user_model
from django.db import models

from .constants import NAME_MAX_LENGTH, STR_LENGTH_LIMIT, TITLE_MAX_LENGTH

User = get_user_model()


class IsPublishedCreatedAtAbstract(models.Model):
    """Абстрактная модель. Добавляет флаг публикации и время создания."""

    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.',
    )
    created_at = models.DateTimeField(
        'Добавлено',
        auto_now_add=True,
    )

    class Meta:
        abstract = True


class Category(IsPublishedCreatedAtAbstract):
    title = models.CharField('Заголовок', max_length=TITLE_MAX_LENGTH)
    description = models.TextField('Описание')
    slug = models.SlugField(
        'Идентификатор',
        unique=True,
        help_text=(
            'Идентификатор страницы для URL; разрешены символы латиницы, '
            'цифры, дефис и подчёркивание.'
        ),
    )

    class Meta(IsPublishedCreatedAtAbstract.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title[:STR_LENGTH_LIMIT]


class Location(IsPublishedCreatedAtAbstract):
    name = models.CharField('Название места', max_length=NAME_MAX_LENGTH)

    class Meta(IsPublishedCreatedAtAbstract.Meta):
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name[:STR_LENGTH_LIMIT]


class Post(IsPublishedCreatedAtAbstract):
    title = models.CharField('Заголовок', max_length=TITLE_MAX_LENGTH)
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем — '
            'можно делать отложенные публикации.'
        ),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
    )

    class Meta:
        default_related_name = 'posts'
        ordering = ('-pub_date',)
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title[:STR_LENGTH_LIMIT]
