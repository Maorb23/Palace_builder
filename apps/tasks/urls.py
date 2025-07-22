from django.urls import path
from .views import IndexView, TasksView, TaskCreateView, TaskCompleteView, TaskToggleCompleteView, TaskDeleteView, SubTaskEditView, RegistrationView, LoginView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('tasks/', TasksView.as_view(), name='dashboard'),
    path('add/', TaskCreateView.as_view(), name='add_task'),
    path('complete/<int:task_id>/', TaskCompleteView.as_view(), name='complete_task'),
    path('toggle_complete/<int:task_id>/', TaskToggleCompleteView.as_view(), name='toggle_task_complete'),
    path('tasks/<int:task_id>/delete/', TaskDeleteView.as_view(), name='delete_task'),
    path('subtask/<int:subtask_id>/edit/', SubTaskEditView.as_view(), name='edit_subtask'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
] 