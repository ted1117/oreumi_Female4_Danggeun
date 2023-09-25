from django.shortcuts import render, redirect, get_object_or_404
from .models import DanggeunPost
from django.conf import settings

# Create your views here.
def main(request):
    return render(request, "main.html")

def trade_list(request, category=None):
    if category:
        trades = DanggeunPost.objects.filter(category=category, publish='Y').order_by('-views')

    else:
        trades = DanggeunPost.objects.filter(publish='Y').order_by('-views')
    return render(request, 'trade_list.html', {'trades': trades})

def trade_post(request):
    return render(request, 'trade_post.html')


# 포스트 업로드, 업데이트, 삭제
def create_or_update_post(request, post_id=None):
    # 글수정 페이지의 경우
    if post_id:
        post = get_object_or_404(DanggeunPost, id=post_id)
    
    # 글쓰기 페이지의 경우, 임시저장한 글이 있는지 검색 
    else:
        post = DanggeunPost.objects.filter(author_id=request.user.username, publish='N').order_by('-created_at').first()

    # 업로드/수정 버튼 눌렀을 떄
    if request.method == 'POST':
        form = DanggeunPost(request.POST, instance=post) # 폼 초기화
        if form.is_valid():
            post = form.save(commit=False)

            # 게시물 삭제
            if 'delete-button' in request.POST:
                post.delete() 
                return redirect('trade_list.html') 

            if not form.cleaned_data.get('category'):
                post.topic = '전체'
            
            # 임시저장 여부 설정
            if 'temp-save-button' in request.POST:
                post.publish = 'N'
            else:
                post.publish = 'Y'

            # 글쓴이 설정
            post.author_id = request.user.username

            post.save()
            return redirect('trade_post.html', post_id=post.id) # 업로드/수정한 페이지로 리다이렉트
    
    # 수정할 게시물 정보를 가지고 있는 객체를 사용해 폼을 초기화함
    else:
        form = DanggeunPost(instance=post)

    template = 'write.html'
    context = {'form': form, 'post': post, 'edit_mode': post_id is not None, 'MEDIA_URL': settings.MEDIA_URL,} #edit_mode: 글 수정 모드여부

    return render(request, template, context)

def chat(request):
    return render(request, "chat/chat.html")

def room(request, room_name):
    context = {
        "room_name": room_name,
    }
    return render(request, "chat/room.html", context)

