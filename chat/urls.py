from django.urls import path
from chat import views


urlpatterns = [
    path('', views.index, name='home'),
    path('create/', views.create_view, name='create_room'),
    path('room/<slug:slug>/', views.room_view, name='room'),
    path('private/', views.private_list_view, name='private_list'),
    path('private/<str:username>/', views.private_chat_view, name='private')
]