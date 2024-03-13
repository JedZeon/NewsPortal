from django.contrib import admin
from .models import Post, Category


class PostAdmin(admin.ModelAdmin):
    list_display = ('date_time', 'title', 'author', 'rate')
    list_filter = ('date_time', 'author', 'rate')  # добавляем примитивные фильтры в нашу админку
    search_fields = ('title', )


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
