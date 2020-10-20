from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name='index_view'),
    path('recipe', views.single_recipe, name='single_recipe'),
    path('adduser', views.add_user, name='add_user'),
    path('addrecipe', views.add_recipe, name='add_recipe'),
    path('editrecipe', views.edit_recipe, name='edit_recipe'),
    path('logs', views.logs_view, name='logs_view'),
    path('comment', views.comment, name='comment'),
]
