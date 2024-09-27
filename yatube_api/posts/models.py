from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField('Название группы', max_length=200)
    slug = models.SlugField('Слаг группы', unique=True)
    description = models.TextField('Описание группы')

    def __str__(self):
        return self.title


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followers')
    following = models.CharField(max_length=200)
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        unique_together = ('user', 'following')


class Post(models.Model):
    text = models.TextField('Текст публикации')
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
    )
    image = models.ImageField(
        'Изображение публикации',
        upload_to='posts/',
        null=True,
        blank=True
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Название группы',
    )
    follow = models.ForeignKey(
        Follow,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Сообщество публикации',
    )

    class Meta:
        default_related_name = 'posts'

    def __str__(self):
        return self.text[:30]


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Публикация',
    )
    text = models.TextField('Текст комментария')
    created = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        default_related_name = 'comments'

    def __str__(self):
        return f'{self.text}, {self.post}, {self.author}'
