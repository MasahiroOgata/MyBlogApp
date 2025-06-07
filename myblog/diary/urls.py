from django.urls import path
from . import views

app_name = 'diary'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<str:username>/', views.UserIndexView.as_view(), name='user_index'),
    path('<str:username>/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<str:username>/create/', views.CreateView.as_view(), name='create'),
    path('<str:username>/<int:pk>/update/', views.UpdateView.as_view(), name='update'),
    path('<str:username>/<int:pk>/delete/', views.DeleteView.as_view(), name='delete'),    
]