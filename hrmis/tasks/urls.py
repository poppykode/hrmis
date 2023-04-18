from django.urls import path
from . import views

app_name = 'tasks'
urlpatterns = [
    path('create-task/<int:project_id>',views.create_task, name='create_task'),
    path('task-update/<int:pk>',views.task_update, name='task_update'),
    path('task-update-for-employee/<int:pk>',views.task_update_for_employee, name='task_update_for_employee'),
    path('task-delete/<int:pk>',views.task_delete, name='task_delete'),
    path('employee-tasks/<int:employee_id>',views.employee_tasks, name='employee_tasks'),

]
