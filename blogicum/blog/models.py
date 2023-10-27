from django.db import models
from django.contrib.auth import get_user_model

from . import model_constants as const

User = get_user_model()


class BaseModel(models.Model):
    is_published = models.BooleanField(
        default=True,
        verbose_name=const.IS_PUBLISHED_VERBOSE_NAME,
        help_text=const.IS_PUBLISHED_HELP_TEXT
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=const.CREATED_AT_VERBOSE_NAME
    )

    class Meta:
        abstract = True


class TitleModel(models.Model):
    title = models.CharField(
        max_length=const.MAX_LENGTH,
        verbose_name=const.TITLE_VERBOSE_NAME
    )

    class Meta:
        abstract = True


class Location(BaseModel):
    name = models.CharField(
        max_length=const.MAX_LENGTH,
        verbose_name=const.LOCATION_NAME_VERBOSE_NAME
    )

    class Meta:
        verbose_name = const.LOCATION_VERBOSE_NAME
        verbose_name_plural = const.LOCATION_VERBOSE_NAME_PLURAL

    def __str__(self):
        return self.name


class Category(BaseModel, TitleModel):
    description = models.TextField(
        verbose_name=const.CATEGORY_DESCR_VERBOSE_NAME
    )
    slug = models.SlugField(
        unique=True,
        verbose_name=const.CATEGORY_SLUG_VERBOSE_NAME,
        help_text=const.CATEGORY_SLUG_HELP_TEXT
    )

    class Meta:
        verbose_name = const.CATEGORY_VERBOSE_NAME
        verbose_name_plural = const.CATEGORY_VERBOSE_NAME_PLURAL

    def __str__(self):
        return self.title


class Post(BaseModel, TitleModel):
    text = models.TextField(
        verbose_name=const.POST_TEXT_VERBOSE_NAME
    )

    pub_date = models.DateTimeField(
        verbose_name=const.POST_PUB_DATE_VERBOSE_NAME,
        help_text=const.POST_PUB_DATE_HELP_TEXT
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name=const.POST_AUTHOR_VERBOSE_NAME
    )

    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=const.POST_LOCATION_VERBOSE_NAME

    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts',
        verbose_name=const.POST_CATEGORY_VERBOSE_NAME
    )

    image = models.ImageField(
        upload_to=const.POST_IMAGE_DIR_NAME,
        verbose_name=const.POST_IMAGE_VERBOSE_NAME,
        blank=True
    )

    class Meta:
        verbose_name = const.POST_VERBOSE_NAME
        verbose_name_plural = const.POST_VERBOSE_NAME_PLURAL
        ordering = const.POST_ORDERING

    def comment_count(self):
        return self.comments.count()

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField()

    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=const.CREATED_AT_VERBOSE_NAME
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    class Meta:
        verbose_name = const.COMMENT_VERBOSE_NAME
        verbose_name_plural = const.COMMENT_VERBOSE_NAME_PLURAL

    def __str__(self):
        return self.author
