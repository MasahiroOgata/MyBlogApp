from django.views import generic
from django.urls import reverse_lazy
from .models import Article
from user.models import CustomUser
from django.core.exceptions import PermissionDenied
# from django.core.paginator import Paginator

class DiaryOwnerMixin(generic.base.ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs['username']
        try:
            diary_owner = CustomUser.objects.get(username=username)
            context['diary_owner'] = diary_owner
            articles = Article.objects.filter(author__username=username).order_by('-created_at')
            context['diary_list'] = articles[:5]
            context['diary_list_all'] = articles
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
    paginate_by = 5

    def get_queryset(self):
        username = self.kwargs.get('username')
        return self.model.objects.filter(author__username=username).order_by('-created_at')
    
class EntryListView(DiaryOwnerMixin, generic.ListView):
    model = Article
    template_name = 'diary/entry_list.html'

    def get_queryset(self):
        username = self.kwargs.get('username')
        return self.model.objects.filter(author__username=username).order_by('-created_at')
        
class DetailView(DiaryOwnerMixin, CollateAuthorAndPkMixin, generic.DetailView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        article_list = list(context.get('diary_list_all', []))
        current_article = self.object

        prev_article = None
        next_article = None

        for i, article in enumerate(article_list):
            if article.pk == current_article.pk:
                if i > 0:
                    next_article = article_list[i - 1]
                if i < len(article_list) - 1:
                    prev_article = article_list[i + 1]
                break

        context['prev_article'] = prev_article
        context['next_article'] = next_article

        return context

class CreateView(DiaryOwnerMixin, CollateLoginUserMixin, generic.edit.CreateView):
    model = Article
    fields = ['title', 'content'] 

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreateView, self).form_valid(form)

class UpdateView(DiaryOwnerMixin, CollateAuthorAndPkMixin,
                CollateLoginUserMixin, generic.edit.UpdateView):
    fields = ['title', 'content'] 

class DeleteView(DiaryOwnerMixin, CollateAuthorAndPkMixin, 
                CollateLoginUserMixin, generic.edit.DeleteView):
    def get_success_url(self):
        return reverse_lazy('diary:user_index', kwargs={'username': self.kwargs['username']})

