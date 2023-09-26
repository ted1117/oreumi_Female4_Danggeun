from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class DanggeunPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=200)
    price = models.IntegerField()
    status = models.CharField(max_length=1, default='N')
    views = models.IntegerField(default=0)
    chat = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    author_id = models.CharField(max_length=100, null=True, blank=True)
    post_id = models.CharField(max_length=100, null=True, blank=True)
    trading_location = models.CharField(max_length=100)
    publish = models.CharField(max_length=1, default='Y')

class ChatRoom(models.Model):
    """Summary
    채팅방 정보 모델

    Attributes:
        room_id (AutoField): _채팅방 식별자_
        post_id (FK): _게시물 id_
        seller (FK): _판매자 id_
        created_at (DateTimeField): _채팅방 생성 시각_
        updated_at (DateTimeField): _채팅방 최근 수정 시각_
        models (_type_): _description_

    Returns:
        _type_: _description_
    """
    room_id = models.AutoField(primary_key=True)
    post_id = models.ForeignKey(DanggeunPost, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.room_id
    
class Chat(models.Model):
    """_summary_
    채팅 메시지 내역 모델

    Attributes:
        room_id (FK): _ChatRoom의 room_id_
        from_id (FK): _메시지 발신자 id_
        content (TextField): _채팅 내용_
        is_read (BooleanField): _상대방의 메시지 읽음 여부_
        sent_at (DateTimeField): _메시지 전송 시각_
    """
    room_id = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    from_id = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now=True)