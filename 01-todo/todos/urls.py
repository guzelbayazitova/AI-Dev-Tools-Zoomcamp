from django.urls import path
from . import views

urlpatterns = [
    path('', views.TodoListView.as_view(), name='todo_list'),
    path('create/', views.todo_create, name='todo_create'),
    path('<int:pk>/edit/', views.todo_update, name='todo_update'),
    path('<int:pk>/delete/', views.todo_delete, name='todo_delete'),
    path('<int:pk>/toggle/', views.todo_toggle_complete, name='todo_toggle_complete'),
]