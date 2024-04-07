from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Job, Contract
from .forms import JobForm, ContractForm
from projects.models import Tag
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import Profile
from users.views import createMessage
from .utils import generate_contract_pdf, searchJobs, paginateProfiles
from users.models import Message
from users.forms import MessageForm
# Create your views here.


def jobs(request):
    jobObj1, search_query = searchJobs(request)
    jobObj = tuple(x for x in jobObj1 if not x.is_assigned and x.is_active)
    custom_range, jobObj = paginateProfiles(request, jobObj, 3)
    return render(request, 'jobs.html',
                  {'jobs': jobObj, 'search_query': search_query, 'custom_range': custom_range})
   


    

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
def createContract(request, pk, sk):
    profile = request.user.profile
    freelancer = Profile.objects.get(id=pk)
    job = Job.objects.get(id=sk)
    form = ContractForm(request.POST)
    if request.method == 'POST':
        form = ContractForm(request.POST, request.FILES)
        if form.is_valid():
            contract = form.save(commit=False)
            contract.client = job.owner
            contract.freelancer = freelancer
            contract.job = job
            contract.save()
            # return generate_contract_pdf(request, contract.id)
            createTaskMessage(request, freelancer.id, contract.id)
            return generate_contract_pdf(request, contract.id)
            # return redirect('contract', contract.id)
        else:
            return HttpResponse('wrong')
    else:
        # If it's a GET request, pre-fill the form with job data
        initial_data = {
            'job': job,
            'freelancer': freelancer,
            'client': job.owner,
            'title': job.title,
            'budget': job.budget,
            'duration': job.duration,
            'featured_image': job.featured_image,
            'description': job.description,
        }

        form = ContractForm(initial=initial_data)

    context = {'form': form,}
    return render(request, 'contract_form.html', context)

def createTaskMessage(request, pk, sk):
    contract = Contract.objects.get(id=sk)
    recipient = Profile.objects.get(id=pk)
    sender = request.user.profile
    form = MessageForm({
        'subject': 'Contract Assignment',
        'body': f'Dear {recipient.name}, I have created a contract that we have recently agreed for this <a href="http://127.0.0.1:8000/jobs/job/{contract.job.id}">task</a>. \n Budget is {contract.budget} soums and you can finish it in {contract.duration}. Please find and download the contract <a href="http://127.0.0.1:8000/jobs/contract/{contract.id}">here</a>. Once you sign, the task will be assigned to you'
    }
    )
    if form.is_valid:
        form1=form.save(commit=False)
        form1.recipient = recipient
        form1.sender = sender
        form1.save()
    else:
        messages.error(request, "Please fill all the fields accordingly")

def contract(request, pk):
    contract = Contract.objects.get(id=pk)
    if request.method == "POST":
        print(request.POST)
        combined = request.POST['combined_vars']
        contract_id, freelancer_id = combined.split('_')
        print(contract_id, freelancer_id)
        # freelancer_id = request.POST['freelancer_id']
        contract = Contract.objects.get(id=contract_id)
        contract.job.assigned = Profile.objects.get(id=freelancer_id)
        contract.job.save()
        return generate_contract_pdf(request, contract.id )
    context ={'contract': contract}
    return render(request, 'contract.html', context=context)


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
    name = profile.name
    job.assigned = profile
    job.is_assigned = True
    job.save()
    messages.success(request, 'The job is now assigned to ', name)
    return redirect('clicks', pk)


login_required(login_url="login")
def changeJobStatus(request, pk):
    profile = request.user.profile
    job = Job.objects.get(id=pk)
    if job.is_active:
        job.is_active = False
        job.clicked.clear()
        job.assigned = None
        job.click_total = 0
        job.save()
    else:
        job.is_active = True
        job.save()
    return redirect('account')

