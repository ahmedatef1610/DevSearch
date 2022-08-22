from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, Http404, JsonResponse
from django.urls import reverse
from django.template.loader import render_to_string

from django.views import View
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, CreateView

from django.db.models import Avg, Min, Max, Q
from .models import Project, Tag

from .forms import ProjectForm, ReviewForm

from django.contrib.auth.decorators import login_required

import json
from datetime import date

from .utils import searchProjects, paginationProjects

from django.contrib import messages


#############################################################################


# Create your views here.
def projects(request):
    
    # projects = Project.objects.all()
    projects, search_query = searchProjects(request)
    custom_range, projects = paginationProjects(request, projects , 6)

    context = {'projects':projects, 'search_query':search_query, 'custom_range': custom_range}
    return render(request,'projects/projects.html',context)


def project(request, pk):
    # projectObj = next((project for project in projectsList if project["id"] == pk), None)
    projectObj = Project.objects.get(id=pk)
    # tags = projectObj.tags.all()
    form = ReviewForm()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.project = projectObj
            review.owner = request.user.profile
            review.save()
            # Update project vote count
            projectObj.getVoteCount
            messages.success(request, 'Your review was successfully submitted!')
            return redirect('project', pk = projectObj.id)
    
    
    return render(request, 'projects/single-project.html', { 'project': projectObj, 'form':form })


@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(","," ").split()
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            # return redirect('projects')
            return redirect('account')
            
    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url="login")
def updateProject(request, pk):
    profile = request.user.profile
    # project = Project.objects.get(id=pk)
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)
    
    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(","," ").split()
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            
            # return redirect('projects')
            return redirect('account')
            
    context = {'form': form, 'project': project,}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url="login")
def deleteProject(request, pk):
    profile = request.user.profile
    # project = Project.objects.get(id=pk)
    project = profile.project_set.get(id=pk)
    
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    
    context = {'object': project}
    # return render(request, 'projects/delete_template.html', context)
    return render(request, 'delete_template.html', context)



###########################################################
@login_required(login_url="login")
def removeTag(request):
    
    if request.method == 'DELETE':
        tagId = json.loads(request.body)['tag']
        projectId = json.loads(request.body)['project']
        
        project = Project.objects.get(id=projectId)
        tag = Tag.objects.get(id=tagId)
        
        project.tags.remove(tag)
        
        return JsonResponse('Tag was Deleted!', safe=False)

    raise Http404()


###########################################################




