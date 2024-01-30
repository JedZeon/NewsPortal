from django.contrib import admin
from django.urls import path, include
from sign.views import ProfileView, ProfileEdit

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('', include('news.urls'), name='home'),
    path('sign/', include('sign.urls')),
    path('accounts/', include('allauth.urls')),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/edit/', ProfileEdit.as_view(), name='profile_edit'),

]
