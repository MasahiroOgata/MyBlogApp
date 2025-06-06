from django.shortcuts import render
from django.views import generic
from .models import Article
from user.models import CustomUser

class IndexView(generic.ListView):
    def get_queryset(self):
        return Article.objects.order_by('-created_at')

class UserIndexView(generic.ListView):
    template_name = 'diary/user_index.html' 
    
    def get_queryset(self):
        username = self.kwargs['username']
        return Article.objects.filter(author__username=username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return get_diary_title(self, context)
        # context = super().get_context_data(**kwargs)
        # username = self.kwargs['username']
        # context['username'] = username
        # diary_owner = CustomUser.objects.get(username=username)
        # context['diary_title'] = diary_owner.diary_title
        # return context 

class DetailView(generic.DetailView):
    model = Article


def get_diary_title(self, context):    
    username = self.kwargs['username'] 
    context['username'] = username  
    diary_owner = CustomUser.objects.get(username=username)
    context['diary_title'] = diary_owner.diary_title
    return context 