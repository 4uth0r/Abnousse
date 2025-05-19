from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from django_ckeditor_5.fields import CKEditor5Field


class CustomUser(AbstractUser):
    pass

    def __str__(self):
        return self.get_full_name()


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, verbose_name=_('کاربر'))
    bio = CKEditor5Field(verbose_name = _('معرفی'), max_length=500, config_name='extends', blank=True)
    avatar = models.ImageField(verbose_name = _('نگاره'), upload_to='uploads/profile', blank=True, null=True)
    created = models.DateTimeField(verbose_name = _('تاریخ ایجاد'), auto_now_add=True)
    updated = models.DateTimeField(verbose_name = _('تاریخ ویرایش'), auto_now=True)

    class Meta:
        verbose_name = _('نمایه کاربر')
        verbose_name_plural = _('نمایه کاربرها')

    def __str__(self):
        return self.user.get_full_name()


@receiver(post_save, sender=CustomUser)
def create_or_update_profile(sender, instance, created, **kwargs):
    Profile.objects.get_or_create(user=instance)
