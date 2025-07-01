from django.urls import path
from . import views
urlpatterns = [
    path('create-card/', views.create_card, name='create_card'),
    path('my-cards/', views.my_card, name='my_card'),
]