# import requests
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# , TemplateView
from .models import Post, Category, UserCategory, Author
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from datetime import datetime


class PostList(ListView):
    model = Post
    ordering = '-date_time'
    template_name = 'post_list.html'
    context_object_name = 'post_list'
    paginate_by = 5

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict(параметры запроса(фильтрации))
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    # Просто чтобы в urls, указать не pk а id
    pk_url_kwarg = 'id'


class PostSearch(PostList):
    template_name = 'search.html'


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)

    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    initial = {'type_news': 'NE'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # author_ = Author.objects.get(user=self.request.user)
        author_ = Author.objects.filter(user=self.request.user).first()
        self.initial.update({'author': author_})

        if Post.objects.filter(author=author_, date_time__date=datetime.utcnow()).count() >= 3:
            self.template_name = 'stop.html'

        return context
        # if request.POST:
        #     return request.POST.get('max_posts')
        # else:
        #     return request.POST.get('max_posts')


class ArticleCreate(PostCreate):
    initial = {'type_news': 'AR'}


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)

    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class CategoryList(LoginRequiredMixin, ListView):
    model = Category
    ordering = 'id'
    template_name = 'category_list.html'
    context_object_name = 'category_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sub = []
        for cat_user in UserCategory.objects.all().filter(user=self.request.user):
            sub.append(cat_user.category)

        context['user_subscriber'] = sub
        return context

    def subscribe_user(request, pk, **kwargs):
        UserCategory.objects.create(user=request.user, category=Category.objects.get(id=pk))
        return redirect('/category/')

    def unsubscribe_user(request, pk, **kwargs):
        cat = UserCategory.objects.get(user=request.user, category=Category.objects.get(id=pk))
        cat.delete()
        return redirect('/category/')
