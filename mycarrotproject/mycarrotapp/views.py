from django.shortcuts import render
from .forms import CustomLoginForm, CustomRegistrationForm

# Create your views here.

# 메인페이지
def main(request):
    return render(request, "main.html")

def chat(request):
    return render(request, "chat/chat.html")

def room(request, room_name):
    context = {
        "room_name": room_name,
    }
    return render(request, "chat/room.html", context)

# 로그인
def login(request):
    form = CustomLoginForm(data=request.POST or None)
    return render(request,'login.html',{'form':form})

# 회원가입
def register(request):
    form = CustomRegistrationForm(request.POST)
    return render(request, 'register.html', {'form':form})
