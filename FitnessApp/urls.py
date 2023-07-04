from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
urlpatterns = [
    path("", views.index, name='index'),
    path("delete/<int:id>/", views.delete_food, name='delete'),
    path('bmi/', views.home, name='bmi'),
    # # path("user/", views.greeting_view, name='user'),
    # # path('bmis/', views.bmi_measurement),
    # path('bmi/', views.bmi_measurement),
    # # path('measurement/', views.bmi_measurement),
    # path('measurements/', views.measurements, name="all_measurements"),
    # path('measurements/<int:id>/', views.measurement, name="delete_measurement"),
    # # path('login/', views.LoginView(), name='login'),

]