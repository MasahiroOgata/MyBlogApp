from django.shortcuts import get_object_or_404
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import generic
from .models import CustomUser
from .forms import CustomUserCreationForm
from diary.views import DiaryOwnerMixin

class SignUpView(generic.CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'user/signup.html'

class CustomLoginView(LoginView):
    def get_success_url(self):
        username = self.request.user.username
        return f'/diary/{username}/'
    
class UserUpdateView(DiaryOwnerMixin, generic.edit.UpdateView):
    template_name = 'user/update.html'
    model = CustomUser
    fields = ['diary_title', 'header_image', 'title_color']

    def get_success_url(self):
        return reverse_lazy('diary:user_index', kwargs={'username': self.kwargs['username']})
    
    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        return get_object_or_404(CustomUser, username=username)