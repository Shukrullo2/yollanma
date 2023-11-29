from django.shortcuts import render, redirect
from .models import Profile, Skill, Message
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm, CustomProfileForm
from django.contrib import messages
from .utils import searchProfiles, paginateProfiles
from django.contrib.auth.models import User
from django.db.models import Q


# Create your views here.

def loginUser(request):
    page = 'login'
    context = {'page': page}

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "username doesnot exist")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("redirect")
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request, "username doesnot exist")
    return render(request, 'login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'User account is created')
            login(request, user)
            return redirect('set-type')
        else:
            messages.error(request, "An error has occured")
    context = {'page': page, 'form': form}
    return render(request, 'login_register.html', context)


def setProfileType(request):
    profile = request.user.profile
    form = CustomProfileForm(instance=profile)
    if request.method == 'POST':
        form = CustomProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user_type = request.POST.get('user_type')
            profile.save()
            return redirect('edit-account')
    context = {'form': form}
    return render(request, 'profile_type_form.html', context)


def profiles(request):
    profileObj1, search_query = searchProfiles(request)
    profileObj = tuple(x for x in profileObj1 if x.user_type == 'freelance')
    custom_range, profileObj = paginateProfiles(request, profileObj, 3)
    return render(request, 'profiles.html',
                  {'profiles': profileObj, 'search_query': search_query, 'custom_range': custom_range})


def companies(request):
    companiesObj1, search_query = searchProfiles(request)
    companiesObj = tuple(x for x in companiesObj1 if x.user_type == 'company')
    custom_range, profileObj = paginateProfiles(request, companiesObj, 3)
    return render(request, 'companies.html',
                  {'profiles': companiesObj, 'search_query': search_query, 'custom_range': custom_range})


def user_profile(request, pk):
    profileObj = Profile.objects.get(id=pk)

    topskill = profileObj.skill_set.exclude(description__exact="")
    otherskill = profileObj.skill_set.filter(description="")

    return render(request, 'user-profile.html', {'profile': profileObj, 'topskill': topskill,
                                                 'otherskill': otherskill})


@login_required()
def userAccount(request):
    profile = request.user.profile
    skill = profile.skill_set.all()
    projects = profile.project_set.all()
    jobs = profile.job_set.all()

    try:
        assigned = profile.assigned
    except:
        assigned = False

    context = {'profile': profile, 'skills': skill, 'projects': projects, 'jobs': jobs, 'assigned_job': assigned}
    return render(request, 'account.html', context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form': form}
    return render(request, 'profile_form.html', context)


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
            return redirect('account')
    context = {'form': form}
    return render(request, 'skill_form.html', context)


@login_required(login_url="login")
def deleteSkill(request, pk):
    skill = Skill.objects.get(id=pk)
    skill.delete()
    messages.success(request, 'Skill is deleted')
    return redirect('account')


def editSkill(request, pk):
    skill = Skill.objects.get(id=pk)
    form = SkillForm(instance=skill)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form': form}
    return render(request, 'skill_form.html', context)


@login_required(login_url="login")
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    my_messages = []

    uniqueSenders = []
    unreadSender = []
    sent_by_me = []

    for message in Message.objects.filter(sender=profile):
        if message.recipient not in uniqueSenders:
            uniqueSenders.append(message.recipient)

    for message in messageRequests:
        if message.sender not in uniqueSenders:
            uniqueSenders.append(message.sender)

    for message in messageRequests:
        if not message.is_read:
            unreadSender.append(message.sender)

    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'unreadSenders': unreadSender, 'unReadCount': unreadCount, 'senders': uniqueSenders}
    return render(request, 'inbox.html', context)


@login_required(login_url="login")
def viewMessage(request, pk):
    sender = Profile.objects.get(id=pk)
    recipient = request.user.profile
    form = MessageForm()
    if request.method == 'POST':
        form = MessageForm(request.POST)

        if form.is_valid():
            messageObj = form.save(commit=False)
            messageObj.recipient = sender
            messageObj.sender = recipient
            if sender:
                # messageObj.name = sender.name
                messageObj.email = recipient.email
            messageObj.save()
            messages.success(request, 'Message is Sent')
            return redirect(request.path, pk)

    messageRequest = Message.objects.filter(
        Q(sender=sender, recipient=recipient) | Q(sender=recipient, recipient=sender))
    for item in messageRequest:
        if not item.is_read:
            item.is_read = True
            item.save()
    context = {'messageRequest': messageRequest, 'form': form}
    return render(request, 'message.html', context)


def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    sender = request.user.profile
    form = MessageForm()
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)

        if form.is_valid():
            messageObj = form.save(commit=False)
            messageObj.recipient = recipient
            messageObj.sender = sender
            if sender:
                # messageObj.name = sender.name
                messageObj.email = sender.email
            messageObj.save()
            messages.success(request, 'Message is Sent')
            return redirect('user_profile', pk)

    context = {'form': form, 'recipient': pk}
    return render(request, 'message_form.html', context)


def noUser(request, pk):
    messageRequest = Message.objects.get(id=pk)
    context = {'msg': messageRequest}
    return render(request, 'no_user.html', context)


