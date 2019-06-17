from django.urls import path

from . import views

app_name = 'time_entries'
urlpatterns = [
    path('', views.index, name='spent_time')
]
