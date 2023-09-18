from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class BaseModel(models.Model):
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )

    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Добавлено')

    class Meta:
        abstract = True


class TitleModel(models.Model):
    title = models.CharField(max_length=256,
                             verbose_name='Заголовок')

    class Meta:
        abstract = True


class Location(BaseModel):
    name = models.CharField(max_length=256,
                            verbose_name='Название места')

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Category(BaseModel, TitleModel):
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text='Идентификатор страницы для URL; '
                  'разрешены символы латиницы, цифры, '
                  'дефис и подчёркивание.'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Post(BaseModel, TitleModel):
    text = models.TextField(verbose_name='Текст')

    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и время в будущем — '
                  'можно делать отложенные публикации.'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор публикации'
    )

    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение'

    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name='Категория'
    )

    image = models.ImageField(
        upload_to='posts/',
        verbose_name='Изображение',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    def comment_count(self):
        num_comments = self.comments.count()
        return num_comments

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"post_id": self.pk})


class Comment(models.Model):
    text = models.TextField()

    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
     )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('created_at',)

    def __str__(self):
        return f'Комментарий от {self.author.username}'
