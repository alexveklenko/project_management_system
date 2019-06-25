from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('', views.index, name='users'),
    path('<int:id>', views.user_view, name='user'),
]
