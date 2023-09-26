from django.db import models

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

class UserInfo(models.Model):
    user_name = models.CharField(max_length=20) # 이름
    nickname = models.CharField(max_length=100) # 닉네임
    region = models.CharField() # 지역
    manner_temp = models.IntegerField() # 매너온도
    region_cert = models.CharField(max_length=1, default='N') # 지역인증 여부
    create_date =models.DateTimeField(auto_now_add=True) # 가입일
    # account_id = models.CharField() # 회원 계정 ID
    # password = models.CharField() # 비밀번호
