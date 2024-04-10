from django.shortcuts import render, redirect
from django.contrib.auth import  login
from .forms import CustomLoginForm
from .forms import  SignUpForm
from .forms import ProfileUpdateForm
from django.contrib import messages
from django.urls import reverse
from .models import CustomUser

def firstpage(request):
    return render(request, 'firstpage.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "가입이 성공적으로 완료되었습니다. 로그인 해주세요.")
            return redirect(reverse('firstpage') + '?signup_success=true')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            user = form.authenticate_user()  
            if user is not None:
                login(request, user)
                return redirect('home')  
            else:
                messages.error(request, "로그인 실패. 다시 시도해주세요.")
        else:
            messages.error(request, "로그인 폼에 오류가 있습니다. 다시 확인해주세요.")
    else:
        form = CustomLoginForm()
    return render(request, 'login_view.html', {'form': form})

def home(request):
    return render(request, 'home.html')


def signup_success(request, pk=None):
    if request.user.is_authenticated:  
        user = request.user
        if pk:
            updated_user = CustomUser.objects.get(pk=pk)

            context = {
                'id': updated_user.id,
                'name': updated_user.name,
                'email': updated_user.email,
                'major': updated_user.major,
                'nickname': updated_user.nickname,
                'phone_number':updated_user.phone_number,
                'age':updated_user.age,
                'hobbies':updated_user.hobbies,
                'photo':updated_user.photo,
            }
       
        else:
            context = {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'major': user.major,
                'nickname': user.nickname,
                'phone_number':user.phone_number,
            }

        return render(request, 'signup_success.html', context)
    else:
        return redirect('login_view') 

def profile_update_view(request):
    if not request.user.is_authenticated:
        return redirect('login_view')  

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            updated_user = CustomUser.objects.get(pk=request.user.pk)
            return redirect('signup_success', pk=updated_user.pk) 
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'profile_update.html', {'form': form})