from django.urls import path
from chat import views


urlpatterns = [
    path('', views.index, name='home'),
    path('create/', views.create_view, name='create_room'),
    path('room/<slug:slug>/', views.room_view, name='room'),
]