from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomLoginForm, SignUpForm, ProfileUpdateForm, TodoItemForm, GuestbookForm
from .models import CustomUser, Guestbook, TodoItem
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

def guestbook_list(request):
    guestbook_messages = Guestbook.objects.all().order_by('-created_at')
    return render(request, 'guestbook_list.html', {'messages': guestbook_messages})

def add_message(request):
    if request.method == "POST":
        form = GuestbookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('guestbook_list')
    else:
        form = GuestbookForm()
    return render(request, 'add_message.html', {'form': form})

def todo_list(request):
    if not request.user.is_authenticated:
        return redirect('login_view')
    todo_items = TodoItem.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'todo_list.html', {'todo_items': todo_items})

def add_todo_item(request):
    if not request.user.is_authenticated:
        return redirect('login_view')
    if request.method == "POST":
        form = TodoItemForm(request.POST)
        if form.is_valid():
            todo_item = form.save(commit=False)
            todo_item.user = request.user
            todo_item.save()
            return redirect('todo_list')
    else:
        form = TodoItemForm()
    return render(request, 'add_todo_item.html', {'form': form})

def toggle_todo_item_completed(request, item_id):
    if not request.user.is_authenticated:
        return redirect('login_view')
    todo_item = TodoItem.objects.get(id=item_id)
    if request.user == todo_item.user:
        todo_item.completed = not todo_item.completed
        todo_item.save()
    return redirect('todo_list')
