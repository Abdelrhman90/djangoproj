from django.shortcuts import render
from basicapp.forms import UserForm,UserProfileInfoForm
# Create your views here.

from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request,'basicapp/index.html')

def register(request):

    registered = False

    if request.method == 'POST':
        userform = UserForm(data=request.POST)
        profileform = UserProfileInfoForm(data=request.POST)

        if userform.is_valid() and profileform.is_valid():

            user = userform.save()
            user.set_password(user.password)
            user.save()

            profile = profileform.save(commit = False)
            profile.user = user

            if 'Profile_Pic' in request.FILES:
                profile.Profile_Pic = request.FILES['Profile_Pic']
            profile.save()

            registered = True
        else:
            print(userform.errors , profileform.errors)
    else:
        userform = UserForm()
        profileform = UserProfileInfoForm()

    return render(request,'basicapp/register.html',{'userform':userform,
                                                    'profileform':profileform,
                                                    'registered':registered})
def user_login(request):

    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active():
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('index'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'basicapp/login.html', {})
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
