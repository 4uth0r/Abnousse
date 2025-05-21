from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from django_ckeditor_5.fields import CKEditor5Field


class Category(models.Model):
    title = models.CharField(_('عنوان'), max_length=200)
    slug = models.SlugField(_('نامک'), max_length=200, unique=True, allow_unicode=True)
    photo = models.ImageField(_('نگاره'), upload_to='uploads/category', blank=True, null=True)
    created = models.DateField(_('تاریخ ایجاد'), auto_now_add=True)
    updated = models.DateField(_('تاریخ ویرایش'), auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = _('دسته')
        verbose_name_plural = _('دسته‌ها')
    
    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(_('عنوان'), max_length=200)
    slug = models.SlugField(_('نامک'), max_length=200, unique=True, allow_unicode=True)
    created = models.DateField(_('تاریخ ایجاد'), auto_now_add=True)
    updated = models.DateField(_('تاریخ ویرایش'), auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = _('برچسب')
        verbose_name_plural = _('برچسب‌ها')
    
    def __str__(self):
        return self.title


class Post(models.Model):
    class Language(models.TextChoices):
        PERSIAN = 'fa', _('پارسی')
        FRENCH = 'fr', _('فرانسوی')

    class Publish(models.TextChoices):
        PUBLISHED = 'p', _('منتشر')
        DRAFT = 'd', _('پیش‌نویس')
    
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts', verbose_name=_('نویسنده'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts', verbose_name=_('دسته'))
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='posts', verbose_name=_('برچسب'))
    title = models.CharField(_('عنوان'), max_length=200)
    slug = models.SlugField(_('نامک'), max_length=200, unique=True, allow_unicode=True)
    abstract = models.TextField(_('چکیده'), blank=True, null=True)
    content = CKEditor5Field(_('محتوا'), config_name='extends')
    photo = models.ImageField(_('نگاره'), upload_to='uploads/post', blank=True, null=True)
    publish = models.CharField(_('وضعیت انتشار'), max_length=1, choices=Publish, default=Publish.DRAFT)
    language = models.CharField(_('زبان'), max_length=2, choices=Language, default=Language.PERSIAN)
    view_count = models.PositiveIntegerField(_('بازدید'), default=0)
    created = models.DateField(_('تاریخ ایجاد'), auto_now_add=True)
    updated = models.DateField(_('تاریخ ویرایش'), auto_now=True)
    
    class Meta:
        ordering = ('-created',)
        verbose_name = _('نوشته')
        verbose_name_plural = _('نوشته‌ها')

    def __str__(self):
        return self.title
    
    def total_likes(self):
        return self.likes.count()
    
    def is_liked_by(self, session_key):
        return self.likes.filter(session_key=session_key).exists()


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes', verbose_name=_('نوشته'))
    session_key = models.CharField(max_length=40)
    created = models.DateField(_('تاریخ ایجاد'), auto_now_add=True)    
    updated = models.DateField(_('تاریخ ویرایش'), auto_now=True)

    class Meta:
        ordering = ('created',)
        verbose_name = _('پسند')
        verbose_name_plural = _('پسندها')
        unique_together = ('session_key', 'post')
    
    def __str__(self):
        return f"{self.session_key} {_('پسندها')} {self.post}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name=_('نوشته'))
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_('کاربر'))
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies', verbose_name=_("پاسخ به"))
    content = models.TextField(_('دیدگاه'))
    approved = models.BooleanField(_('تایید شده؟'), default=False)
    created = models.DateField(_('تاریخ ایجاد'), auto_now_add=True)
    updated = models.DateField(_('تاریخ ویرایش'), auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = _('دیدگاه')
        verbose_name_plural = _('دیدگاه‌ها')

    def __str__(self):
        return self.author.username
    
    def is_reply(self):
        return self.parent is not None
