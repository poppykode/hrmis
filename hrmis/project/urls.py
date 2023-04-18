from django.urls import path
from . import views

app_name = 'projects'
urlpatterns = [
    path('all',views.projects, name='projects'),
    path('project-details/<int:pk>',views.project_details, name='project_details'),
    path('create-project',views.create_project, name='create_project'),
    path('project-update/<int:pk>',views.project_update, name='project_update'),
    path('project-delete/<int:pk>',views.project_delete, name='project_delete'),
    path('gantt-chart/<int:project_id>',views.gantt_chart,name='gantt_chart')

]
