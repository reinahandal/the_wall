from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_wall),
    path('post/', views.post_message),
    path('comment/', views.add_comment),
    path('delete_message/', views.delete_message),
]