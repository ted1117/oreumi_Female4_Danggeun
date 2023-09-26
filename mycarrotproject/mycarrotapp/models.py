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

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']

class UserInfo(models.Model):
    user_name = models.CharField(max_length=20) # 이름
    nickname = models.CharField(max_length=100) # 닉네임
    region = models.CharField() # 지역
    manner_temp = models.IntegerField() # 매너온도
    region_cert = models.CharField(max_length=1, default='N') # 지역인증 여부
    create_date =models.DateTimeField(auto_now_add=True) # 가입일
    # account_id = models.CharField() # 회원 계정 ID
    # password = models.CharField() # 비밀번호
    
