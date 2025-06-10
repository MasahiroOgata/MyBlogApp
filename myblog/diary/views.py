from django.views import generic
from django.urls import reverse_lazy
from .models import Article
from user.models import CustomUser

class DiaryOwnerMixin(generic.base.ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs['username']
        try:
            diary_owner = CustomUser.objects.get(username=username)
            context['diary_owner'] = diary_owner
        except CustomUser.DoesNotExist:
            context['diary_owner'] = None
        return context
    
class CollateAuthorAndPkMixin(generic.detail.SingleObjectMixin):
    model = Article

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        username = self.kwargs.get('username')
        return self.model.objects.filter(id=pk, author__username=username)

    # def get_queryset(self):
    #     if not self.model:
    #         raise ImproperlyConfigured("CollateAuthorAndPkMixin requires a model.")
    #     pk = self.kwargs.get('pk')
    #     username = self.kwargs.get('username')
    #     return self.model.objects.filter(id=pk, author__username=username)

class IndexView(generic.ListView):
    def get_queryset(self):
        return Article.objects.order_by('-created_at')

class UserIndexView(DiaryOwnerMixin, generic.ListView):
    template_name = 'diary/user_index.html' 
    
    def get_queryset(self):
        username = self.kwargs['username']        
        return Article.objects.filter(author__username=username).order_by('-created_at')
    
class DetailView(DiaryOwnerMixin, generic.DetailView):
    def get_queryset(self):
        pk = self.kwargs['pk']
        username = self.kwargs['username']
        return Article.objects.filter(id=pk, author__username=username)

class CreateView(DiaryOwnerMixin, generic.edit.CreateView):
    model = Article
    fields = '__all__'

class UpdateView(DiaryOwnerMixin, generic.edit.UpdateView):
    model = Article
    fields = '__all__'

class DeleteView(DiaryOwnerMixin, generic.edit.DeleteView):
    model = Article 
     
    def get_success_url(self):
        return reverse_lazy('diary:user_index', kwargs={'username': self.kwargs['username']})

# def get_diary_owner(self, context):    
#     username = self.kwargs['username']  
#     diary_owner = CustomUser.objects.get(username=username)
#     context['diary_owner'] = diary_owner
#     return context 

# def get_diary_owner_context(self, **kwargs):
#     context = self.super().get_context_data(**kwargs)
#     username = self.kwargs['username']  
#     diary_owner = CustomUser.objects.get(username=username)
#     context['diary_owner'] = diary_owner
#     return context 


