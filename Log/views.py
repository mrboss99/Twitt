# from django.http import HttpResponse
from django.shortcuts import render
# from django.contrib.auth import authenticate, login
from Log.forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import Profile

"""
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user:
                login(request, user)
                return HttpResponse('Authenticated successfully')

            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'Log/login.html', {'form': form})
"""


@login_required
def dashboard(request):
    return render(request,
                  'Log/dashboard.html',
                  {
                      'section': 'dashboard'})  # We also define a section variable. We will use this variable to track the s
    # ite's section that the user is browsing. Multiple views maycorrespond to the same section. This is a simple way to define the section that each view corresponds to.


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()

            # Create the user profile
            # When users register on our site, we will create an empty profileassociated with them. You should create a
            # Profile object manually  using the administration site for the users you created before.
            Profile.objects.create(user=new_user)
            return render(request,
                          'Log/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'Log/register.html',
                  {'user_form': user_form})


@login_required  # We use the login_required decorator because users have to be authenticated to edit their profile
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(
                                    instance=request.user.profile)
    return render(request,
                  'Log/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})
