from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import auth
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from hrmis.utils import (
    generate_employee_id, 
    generate_password,
    send_password_and_username
    )
from . import models
from board.models import Board
from tasks.models import Task
from . import forms

# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return redirect('accounts:redirect_logged')
    template_name = 'registration/login.html'
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if not user.is_active:
                messages.error(
                    request, 'Your account has been deactivate, please contact HRMIS.')
                return render(request, template_name)
            auth.login(request, user)
            messages.success(request, 'You have successfully logged in.')
            return redirect(reverse('accounts:redirect_logged'))
        messages.error(request, 'Invalid username or password.')
    return render(request, template_name)

@login_required
def redirect_logged(request):
    user = request.user
    if user.is_admin:
        return redirect('accounts:admin_dash')
    return redirect('accounts:employee_dash')

@login_required
def admin_dash(request):
    template_name = 'admin_dash.html'
    qs_users = models.User.objects.all()
    qs_board = Board.objects.all()
    context = {
        'admins':qs_users.filter(designation='admin').count(),
        'employees':qs_users.filter(designation='employee').count(),
        'active':qs_users.filter(is_active=True).count(),
        'in_active':qs_users.filter(is_active=False).count(),
        'total':qs_users.count(),
        'qs_board':qs_board
    }
    return render(request,template_name,context)

@login_required
def employee_dash(request):
    template_name = 'employee_dash.html'
    qs_board = Board.objects.all()
    number_of_tasks = Task.objects.filter(resource = request.user)
    context ={
        'qs_board':qs_board,
        'number_of_tasks':number_of_tasks.count()
        }
    return render(request,template_name, context)

@login_required
def users(request,filter = None):
    template_name = 'users.html'
    qs = ''
    qs_ =  models.User.objects.all().exclude(id=request.user.id)
    if filter is not None:
        qs_ =  models.User.objects.all().exclude(id=request.user.id)
        if filter == 'true':
            qs =  qs_.filter(is_active = True)
        elif filter == 'false':
            qs =  qs_.filter(is_active = False)
        else:
            qs =  qs_.filter(designation = filter)
        return render(request,template_name,{'obj':qs})
    qs =  qs_
    print('filter')
    print(filter)
    return render(request,template_name,{'obj':qs,'filter':filter})

@login_required
def sign_up(request):
    template_name = 'registration/sign_up.html'
    if request.method == 'POST':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            gender = request.POST.get('gender')
            address = request.POST.get('address')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number')
            designation = request.POST.get('designation')
            is_admin = False
            is_employee = False
            if designation == 'admin':
                is_admin = True
            else:
                is_employee = True
            employee_id=generate_employee_id()
            new_password = generate_password()
            new_user = models.User.objects.create(
                username = employee_id,
                first_name = first_name,
                last_name = last_name,
                is_admin = is_admin,
                is_employee = is_employee,
                designation = designation,
                email = email,
                phone_number = phone_number,
                gender = gender,
                address = address
            )
            if new_user.id:
                new_user.set_password(new_password)
                new_user.save()
                send_password_and_username(employee_id, email, new_password)
                messages.success(request,'User with %s has been successfully created' % (employee_id))
                return redirect('accounts:users')
    context = {
        'form':forms.SignUpForm()
    }
    return render(request,template_name, context)


@login_required
def toggle_user_status(request, pk):
    qs = get_object_or_404(models.User, pk=pk)
    print('users')
    print(qs.is_active)
    if qs.is_active == True:
        qs.is_active = False
        qs.save()
        messages.warning(request, 'Status successfully deacivated.')
        return redirect(reverse('accounts:users'))
    else:
        qs.is_active = True
        qs.save()
        messages.success(request, 'Status successfully activated.')
        return redirect(reverse('accounts:users'))

    
@login_required
def edit_profile_admin(request, pk):
    user_qs = get_object_or_404(models.User, pk=pk)
    if request.method == 'POST':
        form = forms.EditProfileAdminForm(request.POST, instance=user_qs)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile successfully updated.')
    return redirect('accounts:profile',user_qs.pk)

    
@login_required
def profile(request,pk):
    template_name = 'profile.html'
    qs = get_object_or_404(models.User,pk=pk)
    form = forms.EditProfileAdminForm(instance=qs)
    form_change_password = PasswordChangeForm(user=qs)
    context = {
        'obj':qs,
        'form':form,
        'form_change_password':form_change_password
    }
    return render (request,template_name,context)

@login_required
def change_password(request, pk):
    user_qs = get_object_or_404(models.User, pk=pk)
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=user_qs)
        print(form.errors)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password succefully changed.')
        else:
            messages.error(request, form.errors)
        return redirect('accounts:profile',user_qs.pk)

