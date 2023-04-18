from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import pandas as pd
from plotly.offline import plot
import plotly.express as px

from .forms import ProjectForm
from . import models
from tasks.models import Task

# Create your views here.
@login_required
def projects(request):
    template_name = 'projects.html'
    qs =  models.Project.objects.all()
    return render(request,template_name,{'obj':qs})

@login_required
def project_details(request,pk):
    template_name = 'project_details.html'
    qs =  get_object_or_404(models.Project,pk=pk)
    total = 0
    number_of_tasks = 0
    percentage_complition = 0
    for progress in qs.task_project.all():
        total = total + progress.percentage_complition
    number_of_tasks=len(qs.task_project.all())
    if number_of_tasks == 0:
        percentage_complition =0
    else:
        percentage_complition = total/ number_of_tasks
    return render(request,template_name,{'obj':qs,'percentage_complition':percentage_complition})

@login_required
def create_project(request):
    template_name = 'create_project.html'
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        print(form.errors.as_data())
        if form.is_valid():
            form.save()
            messages.success(request, 'Project successfully created.')
            return redirect('projects:projects')
    form = ProjectForm()
    return render(request, template_name, {'form': form,'type':'create'})

@login_required
def project_update(request, pk):
    template_name = 'create_project.html'
    qs = get_object_or_404(models.Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST,instance=qs)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project successfully updated!')
            return redirect('projects:projects')
    else:
        context = {'form': ProjectForm(instance=qs), 'obj': qs,'type':'update'}
    return render(request, template_name, context)

@login_required
def project_delete(request, pk):
    template_name = 'project_delete.html'
    qs = get_object_or_404(models.Project, pk=pk)
    if request.method == 'POST':
        qs.delete()
        messages.success(request, 'Project has been successfully deleted!')
        return redirect('projects:projects')
    return render(request, template_name, {'obj': qs})

@login_required
def gantt_chart(request,project_id):
    qs = get_object_or_404(models.Project,pk=project_id)
    project_data = []
    for task in qs.task_project.all():
        project_data.append(
            {        
            'Task Name': task.title.title(),
            'Start Date': task.start_date,
            'End Date': task.end_date,
            'Resources': task.resource.get_full_name().title()
            } 
        )
    df = pd.DataFrame(project_data)
    fig = px.timeline(
        df, x_start="Start Date", x_end="End Date", y="Task Name", color="Resources"
    )
    fig.update_yaxes(autorange="reversed")
    gantt_plot = plot(fig, output_type="div")
    context = {'plot_div': gantt_plot,'obj':qs}
    return render(request, 'gantt_chart.html', context)


