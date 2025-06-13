from django.views import generic
from django.urls import reverse_lazy
from .models import Article
from user.models import CustomUser
from django.core.exceptions import PermissionDenied

class DiaryOwnerMixin(generic.base.ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs['username']
        try:
            diary_owner = CustomUser.objects.get(username=username)
            context['diary_owner'] = diary_owner
            articles = Article.objects.filter(author__username=username).order_by('-created_at')
            context['diary_list'] = articles[:5]
            context['object_list'] = articles
        except CustomUser.DoesNotExist:
            context['diary_owner'] = None
        return context
        
class CollateAuthorAndPkMixin(generic.detail.SingleObjectMixin):
    model = Article
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        username = self.kwargs.get('username')
        return self.model.objects.filter(id=pk, author__username=username)
    
class CollateLoginUserMixin:
    def dispatch(self, request, *args, **kwargs):
        username = kwargs.get('username')
        if username != request.user.username:
            raise PermissionDenied('You do not have permission to access this page.')
        return super().dispatch(request, *args, **kwargs)

class IndexView(generic.ListView):
    def get_queryset(self):
        return Article.objects.order_by('-created_at')

class UserIndexView(DiaryOwnerMixin, generic.ListView):
    model = Article
    template_name = 'diary/user_index.html' 
        
class DetailView(DiaryOwnerMixin, CollateAuthorAndPkMixin, generic.DetailView):
    pass

class CreateView(DiaryOwnerMixin, CollateLoginUserMixin, generic.edit.CreateView):
    model = Article
    fields = ['title', 'content'] #'__all__'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreateView, self).form_valid(form)

class UpdateView(DiaryOwnerMixin, CollateAuthorAndPkMixin,
                CollateLoginUserMixin, generic.edit.UpdateView):
    fields = ['title', 'content'] #'__all__'

class DeleteView(DiaryOwnerMixin, CollateAuthorAndPkMixin, 
                CollateLoginUserMixin, generic.edit.DeleteView):
    def get_success_url(self):
        return reverse_lazy('diary:user_index', kwargs={'username': self.kwargs['username']})

