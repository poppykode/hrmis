from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from hrmis.utils import send_board_messages

from .forms import BoardForm
from . import models

# Create your views here.
@login_required
def boards(request):
    template_name = 'boards.html'
    qs =  models.Board.objects.all()
    return render(request,template_name,{'obj':qs})

@login_required
def board_details(request,pk):
    template_name = 'board_details.html'
    qs =  get_object_or_404(models.Board,pk=pk)
    return render(request,template_name,{'obj':qs})

@login_required
def add_board(request):
    template_name = 'add_board.html'
    if request.method == 'POST':
        form = BoardForm(request.POST)
        print(form.errors.as_data())
        if form.is_valid():
            form.save()
            messages.success(request, 'Board successfully created.')
            send_board_messages(request.POST.get('title'))
            return redirect('boards:boards')
    form = BoardForm()
    return render(request, template_name, {'form': form,'type':'create'})

@login_required
def board_update(request, pk):
    template_name = 'add_board.html'
    qs = get_object_or_404(models.Board, pk=pk)
    if request.method == 'POST':
        form = BoardForm(request.POST,instance=qs)
        if form.is_valid():
            form.save()
            messages.success(request, 'Board successfully updated!')
            return redirect('boards:boards')
    else:
        context = {'form': BoardForm(instance=qs), 'obj': qs,'type':'update'}
    return render(request, template_name, context)

@login_required
def board_delete(request, pk):
    template_name = 'board_delete.html'
    qs = get_object_or_404(models.Board, pk=pk)
    if request.method == 'POST':
        qs.delete()
        messages.success(request, 'Board has been successfully deleted!')
        return redirect('boards:boards')
    return render(request, template_name, {'obj': qs})