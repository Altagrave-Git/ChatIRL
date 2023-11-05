from django.urls import path
from users import views


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('u/<str:username>/', views.profile_view, name="profile")
]