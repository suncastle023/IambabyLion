from django.shortcuts import render, redirect
from django.contrib.auth import  login
from .forms import CustomLoginForm
from .forms import SignUpForm
from django.contrib import messages
from django.urls import reverse

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
                return redirect('signup_success')  
            else:
                messages.error(request, "로그인 실패. 다시 시도해주세요.")
        else:
            messages.error(request, "로그인 폼에 오류가 있습니다. 다시 확인해주세요.")
    else:
        form = CustomLoginForm()
    return render(request, 'login_view.html', {'form': form})


def signup_success(request):
    if request.user.is_authenticated:  
        user = request.user

        context = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'major': user.major,
            'nickname': user.nickname,
        }

        return render(request, 'signup_success.html', context)
    else:
        return redirect('login_view') 
