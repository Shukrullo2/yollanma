from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project, Tag
from django.contrib import messages
from .forms import ProjectForm, ReviewForm
from .utils import searchProject, paginateProjects
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def projects(request):
    projects, search_query = searchProject(request)
    custom_range, projects = paginateProjects(request, projects, 6)
    context = {'pl': projects, 'search_query':search_query, 'custom_range':custom_range}
    return render(request, 'projects.html', context)


def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner =request.user.profile
        review.save()

        projectObj.getVoteCount

        messages.success(request, 'Review added')
        return redirect('project', pk=projectObj.id)

    tags = projectObj.tags.all()
    return render(request, 'single-project.html', {'project': projectObj, 'tags': tags, 'form': form })

@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm(request.POST)
    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', ' ').split()
        if form.is_valid():
            form = ProjectForm(request.POST, request.FILES)
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            form.save_m2m()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('projects')
        else:
            return HttpResponse('wrong')

    context = {'form': form,}
    return render(request, 'project_form.html', context)
@login_required(login_url="login")
def updateProject(request, pk):
    profile = request.user.profile
    projectObj = profile.project_set.get(id=pk)
    form = ProjectForm(instance=projectObj)

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', ' ').split()



        print(request.POST)
        form = ProjectForm(request.POST, request.FILES, instance=projectObj)
        if form.is_valid():
            projectObj = form.save(commit=False)
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                projectObj.tags.add(tag)
            projectObj.save()
            return redirect('account', )
    context = {'form': form, }
    return render(request, 'project_form.html', context)


@login_required(login_url="login")
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    context = {'project': project, }
    if request.method == 'POST':
            project.delete()
            return redirect('projects')
    return render(request, 'delete_object.html', context)
