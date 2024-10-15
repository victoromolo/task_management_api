from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet
from . import views

#router = DefaultRouter()
#router.register(r'tasks', TaskViewSet, basename='task')

#urlpatterns = [
    #path('', include(router.urls)),
#] 

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('create/', views.task_create, name='task_create'),
    path('<int:pk>/', views.task_detail, name='task_detail'),
    path('<int:pk>/update/', views.task_update, name='task_update'),
    path('<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('<int:pk>/complete/', views.task_complete, name='task_complete'),
    path('<int:pk>/incomplete/', views.task_incomplete, name='task_incomplete'),
    path('completed/', views.completed_tasks, name='completed_tasks'),
]
