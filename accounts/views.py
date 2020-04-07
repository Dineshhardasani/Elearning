from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
@csrf_exempt
def login(request):
    if request.method=='POST':
        username=request.POST['Email']
        password=request.POST['Password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            print("Dinesh")
            messages.info(request,'invalid credentials')
            return redirect('login')
    else:
        return render(request,'login.html')

def signup(request):
    if request.method=='POST':
        first_name=request.POST['firstname']
        last_name=request.POST['lastname']
        username=request.POST['email']
        password1=request.POST['password']
        password2=request.POST['confirmpassword']
        email=request.POST['email']
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username taken')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.infor(request,'email taken')
                return redirect('signup')
            else:
                user=User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
                user.save();
                return redirect('login')

        else:
            print('password not matching..')
        return redirect('/')
    else:
        return render(request,'signup.html')
