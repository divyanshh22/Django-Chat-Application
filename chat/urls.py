from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.home_view, name='home-view'),
    path('search/', views.search_view, name='search-view'),
    path('<str:username>/', views.conversation_view, name='conversation-view'),
]