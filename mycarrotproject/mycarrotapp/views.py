
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomLoginForm, CustomRegistrationForm, PostForm
from .models import Post, UserInfo, ChatRoom
from django.conf import settings
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Q

# Create your views here.

# 메인페이지
def main(request):
    posts = Post.objects.filter(product_sold='N').order_by('-view_num')[:4]
    return render(request, "main.html", {'posts':posts})


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
# @login_required
def write(request):
    try:
        user_profile = UserInfo.objects.get(user_name=request.user)
        
        if user_profile.region_cert == 'Y':
            return render(request, 'mycarrotapp/write.html')
        else:
            return redirect('mycarrotapp:alert', alert_message='동네인증이 필요합니다.')
    except UserInfo.DoesNotExist:
        return redirect('mycarrotapp:main')
    #     return redirect('mycarrotapp:alert', alert_message='동네인증이 필요합니다.')


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
# @login_required
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

# 로그인
def user_login(request):
    if request.user.is_authenticated:
        return redirect('mycarrotapp:main')
    
    else:
        form = CustomLoginForm(data=request.POST or None)
        if request.method == "POST":

            # 입력정보가 유효한 경우 각 필드 정보 가져옴
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                # 위 정보로 사용자 인증(authenticate사용하여 superuser로 로그인 가능)
                user = authenticate(request, username=username, password=password)

                # 로그인이 성공한 경우
                if user is not None:
                    login(request, user) # 로그인 처리 및 세션에 사용자 정보 저장
                    return redirect('mycarrotapp:main')  # 리다이렉션
    return render(request,'login.html',{'form':form})

# 로그아웃
def user_logout(request):
    logout(request)
    return redirect('mycarrotapp:main')


# 회원가입
def register(request):
    error_message = ''
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        username = request.POST.get('username')
        nickname = request.POST.get('nickname')
        if User.objects.filter(username=username).exists():
            error_message = "이미 존재하는 아이디입니다."
        elif form.is_valid():
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']

            # 비밀번호 일치 여부를 확인 후 유저 생성 (UserInfo에도 같이 저장)
            if password1 == password2:
                # 새로운 유저를 생성
                user = User.objects.create_user(username=username, password=password1)
                user_info = UserInfo(user_name=username,nickname = nickname)
                user_info.save()

                return redirect('mycarrotapp:login')
            else:
                # form.add_error('password2', 'Passwords do not match')
                error_message = "비밀번호가 일치하지 않습니다."
    else:
        form = CustomRegistrationForm()

    return render(request, 'register.html', {'form':form, 'error_message': error_message})

