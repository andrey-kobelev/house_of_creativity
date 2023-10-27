
MAX_LENGTH = 256

IS_PUBLISHED_VERBOSE_NAME = 'Опубликовано'
IS_PUBLISHED_HELP_TEXT = 'Снимите галочку, чтобы скрыть публикацию.'

CREATED_AT_VERBOSE_NAME = 'Добавлено'

TITLE_VERBOSE_NAME = 'Заголовок'

LOCATION_NAME_VERBOSE_NAME = 'Название места'
LOCATION_VERBOSE_NAME = 'местоположение'
LOCATION_VERBOSE_NAME_PLURAL = 'Местоположения'

CATEGORY_DESCR_VERBOSE_NAME = 'Описание'
CATEGORY_SLUG_VERBOSE_NAME = 'Идентификатор'
CATEGORY_VERBOSE_NAME = 'категория'
CATEGORY_VERBOSE_NAME_PLURAL = 'Категории'
CATEGORY_SLUG_HELP_TEXT = (
    'Идентификатор страницы для URL; '
    'разрешены символы латиницы, цифры, '
    'дефис и подчёркивание.'
)

POST_TEXT_VERBOSE_NAME = 'Текст'
POST_PUB_DATE_VERBOSE_NAME = 'Дата и время публикации'
POST_PUB_DATE_HELP_TEXT = (
    'Если установить дату и время в будущем — '
    'можно делать отложенные публикации.'
)
POST_AUTHOR_VERBOSE_NAME = 'Автор публикации'
POST_LOCATION_VERBOSE_NAME = 'Местоположение'
POST_CATEGORY_VERBOSE_NAME = 'Категория'
POST_IMAGE_VERBOSE_NAME = 'Изображение'
POST_IMAGE_DIR_NAME = 'posts/'
POST_VERBOSE_NAME = 'публикация'
POST_VERBOSE_NAME_PLURAL = 'Публикации'
POST_ORDERING = ('-pub_date',)

COMMENT_VERBOSE_NAME = 'комментарий'
COMMENT_VERBOSE_NAME_PLURAL = 'Комментарии'
