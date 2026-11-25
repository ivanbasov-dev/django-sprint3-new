from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils.html import format_html

from .models import Category, Location, Post

User = get_user_model()

admin.site.unregister(User)
admin.site.unregister(Group)


def get_admin_link(obj):
    """Возвращает ссылку на страницу редактирования объекта в админке."""
    if obj is None:
        return None
    url = reverse(
        f'admin:{obj._meta.app_label}_{obj._meta.model_name}_change',
        args=(obj.pk,),
    )
    return format_html('<a href="{}">{}</a>', url, obj)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('is_published',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published', 'created_at')
    search_fields = ('name',)
    list_filter = ('is_published',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author_link',
        'category_link',
        'location_link',
        'pub_date',
        'is_published',
    )
    list_display_links = ('title', 'pub_date')
    search_fields = ('title', 'text')
    list_filter = ('is_published', 'category', 'location', 'author')

    @admin.display(description='Автор', ordering='author__username')
    def author_link(self, obj):
        return get_admin_link(obj.author)

    @admin.display(description='Категория', ordering='category__title')
    def category_link(self, obj):
        return get_admin_link(obj.category)

    @admin.display(description='Местоположение', ordering='location__name')
    def location_link(self, obj):
        return get_admin_link(obj.location)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = BaseUserAdmin.list_display + ('posts_count',)

    @admin.display(description='Кол-во постов')
    def posts_count(self, obj):
        return obj.posts.count()
