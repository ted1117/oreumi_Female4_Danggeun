
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import CustomLoginForm, CustomRegistrationForm, PostForm
from .models import Post, UserInfo, ChatRoom, Chat
from django.conf import settings
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Q

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

# 거래글쓰기 화면
@login_required
def write(request):
    try:
        user_profile = UserInfo.objects.get(user=request.user_name)
        
        if user_profile.region_cert == 'Y':
            return render(request, 'mycarrotapp/write.html')
        else:
            return redirect('mycarrotapp:alert', alert_message='동네인증이 필요합니다.')
    except UserInfo.DoesNotExist:
        return redirect('mycarrotapp:alert', alert_message='동네인증이 필요합니다.')


# 거래글수정 화면
def edit(request, id):
    post = get_object_or_404(Post, id=id)
    if post:
        post.description = post.description.strip()
    if request.method == "POST":
        post.title = request.POST['title']
        post.price = request.POST['price']
        post.description = request.POST['description']
        post.location = request.POST['location']
        if 'images' in request.FILES:
            post.images = request.FILES['images']
        post.save()
        return redirect('mycarrotapp:trade_post', pk=id)

    return render(request, 'mycarrotapp/write.html', {'post': post})

# 포스트 검색
def search(request):
    query = request.GET.get('search')
    if query:
        results = Post.objects.filter(Q(title__icontains=query) | Q(location__icontains=query))
    else:
        results = Post.objects.all()
    
    return render(request, 'mycarrotapp/search.html', {'posts': results})

# 동네인증 화면
@login_required
def location(request):
    try:
        user_profile = UserInfo.objects.get(user_id=request.user_name)
        region = user_profile.region
    except UserInfo.DoesNotExist:
        region = None

    return render(request, 'mycarrotapp/location.html', {'region': region})

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
    user = request.user.id
    rooms = ChatRoom.objects.filter(Q(buyer=user) | Q(seller=user)).order_by("-updated_at")
    context = { "rooms": rooms }
    return render(request, "chat/chat.html", context)

# @login_required
def room(request, room_name, user_name):
    user, created = User.objects.get_or_create(username=user_name)
    # login(request, user)

    context = {
        "room_name": room_name,
        "user_name": user_name,
    }
    return render(request, "chat/room.html", context)

def mark_as_read(request, message_id):
    message = get_object_or_404(Chat, id=message_id)

    message.is_read = True
    message.save()

    return JsonResponse({"status": "success"})

# 로그인
def login(request):
    form = CustomLoginForm(data=request.POST or None)
    return render(request,'login.html',{'form':form})

# 회원가입
def register(request):
    form = CustomRegistrationForm(request.POST)
    return render(request, 'register.html', {'form':form})

