from django.views.generic import ListView, DetailView
from .models import Post


class PostList(ListView):
    model = Post            # Указываем модель, объекты которой мы будем выводить
    ordering = '-date_time'  # Поле, которое будет использоваться для сортировки объектов
    template_name = 'post_list.html'
    context_object_name = 'post_list'


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    # Просто чтобы в urls, указать не pk а id
    pk_url_kwarg = 'id'