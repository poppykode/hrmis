from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import BlockedSiteForm
from . import models

# Create your views here.
@login_required
def blocked_sites(request):
    template_name = 'blocked_sites/blocked_sites.html'
    qs =  models.BlockedSite.objects.all()
    return render(request,template_name,{'obj':qs})

@login_required
def add_site_to_block_list(request):
    template_name = 'blocked_sites/add_site_to_block_list.html'
    if request.method == 'POST':
        form = BlockedSiteForm(request.POST, request.FILES)
        print(form.errors.as_data())
        if form.is_valid():
            form.save()
            messages.success(request, 'Site successfully added to block list.')
            return redirect('app_settings:blocked_sites')
    form = BlockedSiteForm()
    return render(request, template_name, {'form': form,'type':'create'})

@login_required
def blocked_site_update(request, pk):
    template_name = 'blocked_sites/add_site_to_block_list.html'
    qs = get_object_or_404(models.BlockedSite, pk=pk)
    if request.method == 'POST':
        form = BlockedSiteForm(request.POST,instance=qs)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blocked site successfully updated!')
            return redirect('app_settings:blocked_sites')
    else:
        context = {'form': BlockedSiteForm(instance=qs), 'obj': qs,'type':'update'}
    return render(request, template_name, context)

@login_required
def blocked_site_delete(request, pk):
    template_name = 'blocked_sites/blocked_site_delete.html'
    qs = get_object_or_404(models.BlockedSite, pk=pk)
    if request.method == 'POST':
        qs.delete()
        messages.success(request, 'Blocked site has been successfully deleted!')
        return redirect('app_settings:blocked_sites')
    return render(request, template_name, {'obj': qs})