
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import CustomLoginForm, CustomRegistrationForm, PostForm
from .models import Post, UserInfo
from django.conf import settings

# Create your views here.

# 메인페이지
def main(request):
    return render(request, "main.html")


# 중고거래 화면
def trade(request):
    top_views_posts = Post.objects.filter(product_sold='N').order_by('-view_num')
    return render(request, 'mycarrotapp/trade.html', {'posts': top_views_posts})

# 중고거래상세정보(각 포스트) 화면
def trade_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    
    # 조회수 증가
    if request.user.is_authenticated:
        if request.user != post.user:
            post.view_num += 1
            post.save()
    else:
        post.view_num += 1
        post.save()

    try:
        user_profile = UserInfo.objects.get(user=post.user)
    except UserInfo.DoesNotExist:
            user_profile = None

    context = {
        'post': post,
        'user_profile': user_profile,
    }

    return render(request, 'dangun_app/trade_post.html', context)

def write(request):
    return render(request, 'mycarrotapp/write.html')

# 포스트 업로드
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)  # 임시 저장
            post.user = request.user  # 작성자 정보 추가 (이 부분을 수정했습니다)
            post.save()  # 최종 저장
            return redirect('mycarrotapp:trade_post', pk=post.pk)  # 저장 후 상세 페이지로 이동
    else:
        form = PostForm()
    return render(request, 'mycarrotapp/trade_post.html', {'form': form})


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

