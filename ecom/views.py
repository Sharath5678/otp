from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from codes.forms import CodeForm
from django.contrib.auth import login, logout
from users.models import CustomUser
from .utils import send_sms
from django.contrib import messages


def index_view(request):
    return render(request, 'index.html', {})

def auth_view(request):
    form = AuthenticationForm
    if request.method == 'POST':
        username= request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            request.session['pk'] = user.pk
            return redirect('verify-view')
        
    return render (request, 'auth.html', {'form':form})

def verify_view(request):
    form = CodeForm(request.POST or None)
    pk = request.session.get('pk')
    if pk:
        user = CustomUser.objects.get(pk=pk)
        code = user.code
        code_user = f"{user.username} : {user.code}"
        if not request.POST:
            send_sms(code_user, user.phone_number)
        if form.is_valid():
            num = form.cleaned_data.get('number')

            if str(code) == num:
                code.save()
                login(request, user)
                return redirect('index-view')
            else:
                return redirect('login-view')
    return render(request, 'verify.html', {'form':form})

def logout_view(request):
    logout(request)
    return redirect('/')

def register_view(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        phone_number=request.POST['phone_number']
        if CustomUser.objects.filter(username=username).exists():
                messages.info(request, 'username is taken')
                return redirect('register-view')
        else:
                    user = CustomUser.objects.create_user(username=username, phone_number = phone_number, password=password)

                    user.save();                
                    return redirect('login-view')     
    return render(request,'register.html') 
