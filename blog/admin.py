from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Category, Tag, Post, Comment


class ReplyInline(admin.StackedInline):
    model = Comment
    fields = ['content', 'approved']
    extra = 0
    fk_name = 'parent'
    verbose_name = _('پاسخ')
    verbose_name_plural = _('پاسخ‌ها')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'created', 'updated']
    search_fields = ['title']
    prepopulated_fields = {
        'slug': ('title',)
    }


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'created', 'updated']
    search_fields = ['title']
    prepopulated_fields = {
        'slug': ('title',)
    }


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['language', 'title', 'category', 'tag', 'publish', 'created', 'updated']
    autocomplete_fields = ['category', 'tag']
    list_filter = ['language', 'publish']
    list_display_links = ['language', 'title']
    list_editable = ['publish']
    exclude = ['author']
    search_fields = ['title']
    prepopulated_fields = {
        'slug': ('title',)
    }

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'approved', 'created', 'updated']
    list_filter = ['approved']
    list_editable = ['approved']
    exclude = ['author', 'parent']
    inlines = [ReplyInline]
    autocomplete_fields = ['post', 'author']

    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        parent = form.instance  # دیدگاه اصلی

        for formset in formsets:
            instances = formset.save(commit=False)
            for obj in instances:
                obj.post = parent.post  # از دیدگاه اصلی بگیر
                obj.parent = parent
                if not obj.author_id:
                    obj.author = request.user
                obj.save()
            formset.save_m2m()
        super().save_related(request, form, formsets, change)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(parent__isnull=True)
