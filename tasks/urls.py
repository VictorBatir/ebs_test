from django.urls import path
from .views import MyTasksListView, add_comment_to_task, StartTaskTimerView, stop_task_timer, add_task_timer

urlpatterns = [
    path('my-tasks/', MyTasksListView.as_view(), name='my-tasks'),
    path('add_comment/', add_comment_to_task, name='add_comment_to_task'),
    path('tasks/<int:task_id>/start-timer/', StartTaskTimerView.as_view(), name='start-task-timer'),
    path('tasks/stop-timer/<int:task_id>/', stop_task_timer, name='stop-task-timer'),
    path('task_timer/add/', add_task_timer, name='add_task_timer'),
]
