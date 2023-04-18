from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from hrmis.utils import send_task_messages

from .forms import TaskForm,TaskUpdateForEmployeeForm
from . import models
from accounts.models import User

# Create your views here.
@login_required
def create_task(request,project_id):
    template_name = 'create_task.html'
    qs=get_object_or_404(models.Project,pk=project_id)
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        resource = request.POST.get('resource')
        title =  request.POST.get('title')
        qs_user =get_object_or_404(User,pk=resource)
        form = TaskForm(request.POST) 
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.project = qs
            new_form.save()
            messages.success(request, 'Task successfully created.')
            dates = start_date + ' - '+ end_date
            send_task_messages(qs.name,title, dates,qs_user.email,'Task '+ title + ' has been assingned to you.')
            return redirect('projects:project_details', qs.pk)
    form = TaskForm()
    return render(request, template_name, {'form': form,'type':'create','obj':qs})

@login_required
def task_update(request, pk):
    template_name = 'create_task.html'
    qs = get_object_or_404(models.Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST,instance=qs)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task successfully updated!')
            return redirect('projects:project_details', qs.project.pk)
    else:
        context = {'form': TaskForm(instance=qs), 'obj': qs,'type':'update'}
    return render(request, template_name, context)

@login_required
def task_update_for_employee(request, pk):
    template_name = 'task_update_for_employee.html'
    qs = get_object_or_404(models.Task, pk=pk)
    context = {'form': TaskUpdateForEmployeeForm(instance=qs), 'obj': qs}
    if request.method == 'POST':   
        if int(request.POST.get('percentage_complition')) > 100:
            messages.error(request, 'Percentage can not be greater than 100%')
            return render(request, template_name, context)
           
        form = TaskUpdateForEmployeeForm(request.POST,instance=qs)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task successfully updated!')
            dates = str(qs.start_date) + ' - '+ str(qs.end_date)
            send_task_messages(qs.project.name,qs.title, dates,qs.resource.email,'Task '+ qs.title + ' has been updated')
            return redirect('tasks:employee_tasks', qs.resource.pk)
    
    return render(request, template_name, context)

@login_required
def task_delete(request, pk):
    template_name = 'task_delete.html'
    qs = get_object_or_404(models.Task, pk=pk)
    if request.method == 'POST':
        qs.delete()
        messages.success(request, 'Task has been successfully deleted!')
        dates = str(qs.start_date) + ' - '+ str(qs.end_date) 
        send_task_messages(qs.project.name,qs.title, dates,qs.resource.email,'Task '+ qs.title + ' has been removed.')
        return redirect('projects:project_details', qs.project.pk)
    return render(request, template_name, {'obj': qs})

@login_required
def employee_tasks(request,employee_id):
    template_name = 'employee_tasks.html'
    qs_user = get_object_or_404(User,pk=employee_id)
    qs_tasks = models.Task.objects.filter(resource = qs_user)
    context = {'obj':qs_tasks,'qs_user':qs_user}
    return render(request,template_name,context)