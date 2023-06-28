from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name='index'),
    path("delete/<int:id>/", views.delete_food, name='delete'),

]