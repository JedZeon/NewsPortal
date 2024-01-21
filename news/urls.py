from django.urls import path
from .views import PostList, PostDetail, PostSearch, PostCreate, ArticleCreate, PostUpdate, PostDelete


urlpatterns = [
   path('', PostList.as_view()),
   path('news/', PostList.as_view(), name="post_list"),
   path('news/<int:id>', PostDetail.as_view(), name="post_detail"),
   path('news/search/', PostSearch.as_view(), name="post_search"),
   path('news/create/', PostCreate.as_view(), name='post_create'),
   path('news/<int:pk>/edit/', PostUpdate.as_view(), name='post_edit'),
   path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('articles/create/', ArticleCreate.as_view(), name='article_create'),
   path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='article_edit'),
   path('articles/<int:pk>/delete/', PostDelete.as_view(), name='article_delete'),
]