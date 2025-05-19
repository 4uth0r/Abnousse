from django.db import models
from django.utils.translation import gettext_lazy as _

from django_ckeditor_5.fields import CKEditor5Field


class Core(models.Model):
    title = models.CharField(_("عنوان"), max_length=255)
    subtitle = models.CharField(_("معرفی"), blank=True)
    phone = models.CharField(_("تلفن"), max_length=12, blank=True)
    mobile = models.CharField(_("همراه"), max_length=12, blank=True)
    email = models.EmailField(_("ایمیل"), blank=True)
    address = models.CharField(_("نشانی"), max_length=255, blank=True)
    logo = models.ImageField(_("لوگو"), upload_to='uploads/core', blank=True, null=True)
    favicon = models.ImageField(_("فاوآیکون"), upload_to='uploads/core', blank=True, null=True)
    about = CKEditor5Field(_("درباره ما"), config_name='extends', blank=True, null=True)
    contact = CKEditor5Field(_("تماس با ما"), config_name='extends', blank=True, null=True)
    created = models.DateField(_("تاریخ ایجاد"), auto_now_add=True)
    updated = models.DateField(_("تاریخ ویرایش"), auto_now=True)

    class Meta:
        verbose_name = _('پیکربندی')
        verbose_name_plural = _('پیکربندی')

    def __str__(self):
        return self.title


class Contact(models.Model):
    name = models.CharField(_("نام"), max_length=255)
    email = models.EmailField(_("ایمیل"), blank=True)
    subject = models.CharField(_('موضوع'), max_length=255)
    message = CKEditor5Field(_("متن پیام"), config_name='extends')
    status = models.BooleanField(_("وضعیت"), default=False) 
    created = models.DateField(_("تاریخ ایجاد"), auto_now_add=True)
    updated = models.DateField(_("تاریخ ویرایش"), auto_now=True)

    class Meta:
        verbose_name = _('پیام')
        verbose_name_plural = _('پیام‌ها')

    def __str__(self):
        return self.name
