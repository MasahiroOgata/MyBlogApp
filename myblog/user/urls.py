from django.urls import path
from django.contrib.auth.views import LogoutView
from. import views

app_name = 'user'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('<str:username>/', views.UserUpdateView.as_view(), name='update'),
]