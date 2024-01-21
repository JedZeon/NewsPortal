from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import TemplateView, DetailView
from .models import BaseRegisterForm, ChangeForm, BasicSignupForm

from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/')


class BaseRegisterView(LoginRequiredMixin, CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class ProfileEdit(LoginRequiredMixin, UpdateView):
    form_class = ChangeForm
    model = User
    template_name = 'profile_edit.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context
