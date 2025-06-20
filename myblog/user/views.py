from django.shortcuts import get_object_or_404
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import generic
from .models import CustomUser
from .forms import CustomUserCreationForm

class SignUpView(generic.CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'user/signup.html'

class CustomLoginView(LoginView):
    def get_success_url(self):
        username = self.request.user.username
        return f'/diary/{username}/'
    
class UserUpdateView(generic.UpdateView):
    template_name = 'user/update.html'
    model = CustomUser
    fields = ['username', 'diary_title']

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        return get_object_or_404(CustomUser, username=username)