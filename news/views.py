from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy


class PostList(ListView):
    model = Post
    ordering = '-date_time'
    template_name = 'post_list.html'
    context_object_name = 'post_list'
    paginate_by = 10

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    # Просто чтобы в urls, указать не pk а id
    pk_url_kwarg = 'id'


class PostSearch(PostList):
    template_name = 'search.html'


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    initial = {'type_news': 'NE'}

    # def form_valid(self, form):
    #     post = form.save(commit=False)
    #     post.type_news = 'AR' if 'articles' in self.request.path else 'NE'
    #     post.save()
    #     return super().form_valid(form)


class ArticleCreate(PostCreate):
    initial = {'type_news': 'AR'}


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')