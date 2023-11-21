from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Job
from .forms import JobForm
from projects.models import Tag
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import Profile
# Create your views here.


def jobs(request):
    jobs = Job.objects.filter(is_active=True)
    context = {'jobs': jobs}
    return render(request, 'jobs.html', context)


def job(request, pk):
    job = Job.objects.get(id=pk)
    tags = job.tags.all()
    context = {'job': job, 'tags': tags}
    return render(request, 'job.html', context)


@login_required(login_url="login")
def createJob(request):
    profile = request.user.profile
    form = JobForm(request.POST)
    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', ' ').split()
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save(commit=False)
            job.owner = profile
            job.save()
            form.save_m2m()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                job.tags.add(tag)
            return redirect('account')
        else:
            return HttpResponse('wrong')

    context = {'form': form,}
    return render(request, 'job_form.html', context)


@login_required(login_url="login")
def updateJob(request, pk):
    profile = request.user.profile
    job = profile.job_set.get(id=pk)
    form = JobForm(instance=job)
    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', ' ').split()
        form = JobForm(request.POST, request.FILES,  instance=job)
        if form.is_valid():
            job = form.save(commit=False)
            job.owner = profile
            job.save()
            form.save_m2m()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                job.tags.add(tag)
            return redirect('account')
        else:
            return HttpResponse('wrong')
    context = {'form': form, }
    return render(request, 'job_form.html', context)

@login_required(login_url="login")
def deleteJob(request, pk):
    job = Job.objects.get(id=pk)
    if request.method == 'POST':
        job.delete()
        return redirect('account')
    context = {'job': job}
    return render(request, 'delete-job.html', context)


@login_required(login_url="login")
def addClick(request, pk):
    job = Job.objects.get(id=pk)
    if request.method == 'POST':
        profile = request.user.profile
        if profile not in job.clicked.all():
            job.click_total = job.click_total + 1
            job.clicked.add(profile)
            job.save()
            messages.success(request, 'Your click has been added')
        else:
            messages.warning(request, 'You have already clicked')

    return redirect('job', job.id)


@login_required(login_url="login")
def clicks(request, pk):
    job = Job.objects.get(id=pk)
    clicks = job.clicked.all()
    context = {'clicks': clicks, 'jobid': pk, 'job': job}
    return render(request, 'clicks.html', context)


def assignJob(request, pk, sk):
    job=Job.objects.get(id=pk)
    profile = Profile.objects.get(id=sk)
    job.assigned = profile
    job.is_assigned = True
    job.save()
    messages.success(request, 'The job is now assigned to ', profile.name)
    return redirect('clicks', pk)


login_required(login_url="login")
def changeJobStatus(request, pk):
    profile = request.user.profile
    job = Job.objects.get(id=pk)
    if job.is_active:
        job.is_active = False
        job.save()
    else:
        job.is_active = True
        job.save()
    return redirect('account')