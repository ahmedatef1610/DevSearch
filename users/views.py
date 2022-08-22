from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, Http404
from django.urls import reverse
from django.template.loader import render_to_string

from django.views import View
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, CreateView

from django.db.models import Avg, Min, Max, Q
from .models import Profile, Skill

from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from django.contrib import messages

import json
from datetime import date

from .utils import searchProfiles, paginationProfiles

#############################################################################

def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('profiles')
         
    
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']
        
        try:
            user = User.objects.get(username=username)
        except Exception as err:
            messages.error(request, 'Username does not exist')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # return redirect('profiles')
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request, 'Username OR Password is incorrect')
            
    
    return render(request,'users/login_register.html')

def logoutUser(request):
    logout(request)
    messages.error(request, 'User was logged out!')
    return redirect('login')
    

def registerUser(request):
    page = "register"
    form = CustomUserCreationForm()
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            
            messages.success(request, 'User account was created!')
            login(request, user)
            # return redirect('profiles')
            return redirect('edit-account')
        
        else: 
            messages.success(request, 'An error has occurred during registration')
        
    context= {'page': page, 'form':form}
    return render(request,'users/login_register.html', context)


###################################

def profiles(request):
    
    # profiles = Profile.objects.all()
    profiles, search_query = searchProfiles(request)
    custom_range, profiles = paginationProfiles(request, profiles, 6)
    context = {'profiles': profiles, 'search_query':search_query, 'custom_range':custom_range}
    return render(request,'users/profiles.html', context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    
    topSkill = profile.skill_set.exclude(description__exact="")
    otherSkill = profile.skill_set.filter(description="")
    
    context = {'profile': profile, 'topSkill':topSkill, 'otherSkill':otherSkill}
    return render(request,'users/user-profile.html', context)

###################################

@login_required(login_url="login")
def UserAccount(request):
    
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    
    context = {'profile': profile, 'skills':skills, 'projects':projects}
    return render(request,'users/account.html', context)


@login_required(login_url="login")
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'User account was edited!')
            return redirect('account')
    
    context = {'form':form}
    return render(request,'users/profile_form.html', context)
    
###################################

@login_required(login_url="login")
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()
    
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'skill was added successfully')
            return redirect('account')
    
    context = {'form':form}
    return render(request,'users/skill_form.html', context)


@login_required(login_url="login")
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)
    
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'skill was updated successfully')
            return redirect('account')
    
    context = {'form':form}
    return render(request,'users/skill_form.html', context)


@login_required(login_url="login")
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'skill was deleted successfully')
        return redirect('account')
    
    context = {'object': skill}
    return render(request, 'delete_template.html', context)

###################################

@login_required(login_url="login")
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests':messageRequests, 'unreadCount':unreadCount, }
    return render(request, 'users/inbox.html', context)


@login_required(login_url="login")
def viewMessage(request, pk):
    
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    
    if message.is_read == False: 
        message.is_read = True
        message.save()
        
    context = {'message':message}
    return render(request, 'users/message.html', context)


def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    
    try:
        sender = request.user.profile
        form = MessageForm(initial={'name': sender.name,'email': sender.email })
    except:
        sender = None
        form = MessageForm()
    
    
    if request.method == 'POST':
        
        form = MessageForm(request.POST)
        
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            
            if sender:
                message.name = sender.name
                message.email = sender.email
            
            message.save()
            
            messages.success(request, 'Your message was successfully sent!')
            
            return redirect('user-profile', pk=recipient.id)
                
    
    context = {'recipient':recipient, 'form':form}
    return render(request, 'users/message_form.html', context)

###################################