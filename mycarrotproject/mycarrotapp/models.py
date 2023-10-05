from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    price = models.IntegerField()
    description = models.TextField()
    location = models.CharField(max_length=100)
    images = models.ImageField(upload_to='post_images/') 
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, to_field='username')
    created_at = models.DateTimeField(auto_now_add=True, null=True) 

    product_reserved = models.CharField(max_length=1, default='N')  # 예약 여부
    product_sold = models.CharField(max_length=1, default='N')  # 판매 여부

    view_num = models.PositiveIntegerField(default=0)  # 조회 수
    chat_num = models.PositiveIntegerField(default=0)  # 채팅 수

    def save(self, *args, **kwargs):
        update_fields = kwargs.get("update_fields", None)

        if update_fields and "chat_num" not in update_fields:
            chat_num = ChatRoom.objects.filter(post_id=self.id).count()
            self.chat_num = chat_num

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']

class UserInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    user_name = models.CharField(max_length=20) # 이름
    nickname = models.CharField(max_length=100,null=True) # 닉네임
    region = models.CharField(max_length=200, null=True) # 지역
    manner_temp = models.FloatField(default=36.5, null=True) # 매너온도
    region_cert = models.CharField(max_length=1, default='N') # 지역인증 여부
    create_date =models.DateTimeField(auto_now_add=True) # 가입일
    # account_id = models.CharField() # 회원 계정 ID
    # password = models.CharField() # 비밀번호

    def __str__(self):
        return f'{self.user.username} Profile'
class ChatRoom(models.Model):
    """Summary
    채팅방 정보 모델

    Attributes:
        room_id (AutoField): _채팅방 식별자_
        post_id (FK): _게시물 id_
        seller (FK): _판매자 id_
        buyer (FK): _구매자 id_
        created_at (DateTimeField): _채팅방 생성 시각_
        updated_at (DateTimeField): _채팅방 최근 수정 시각_
        models (_type_): _description_

    Returns:
        _type_: _description_
    """
    room_id = models.AutoField(primary_key=True)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller_chatrooms")
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer_chatrooms", null=True)
    latest_chat = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.room_id
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.post_id:
            post = self.post_id
            post.chat_num = ChatRoom.objects.filter(post_id=post.id).count()
            post.save(update_fields=["chat_num"])

def post_delete_chatroom(sender, instance, **kwargs):
    if instance.post_id:
        post = instance.post_id
        post.chat_num = ChatRoom.objects.filter(post_id=post.id).count()
        post.save(update_fields=["chat_num"])

models.signals.post_delete.connect(post_delete_chatroom, sender=ChatRoom)
    
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
    room_id = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, null=True)
    from_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)

        if self.room_id:
            self.room_id.updated_at = self.sent_at
            self.room_id.latest_chat = self.content
            self.room_id.save(update_fields=["updated_at", "latest_chat"])      