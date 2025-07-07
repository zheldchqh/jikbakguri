# pybo/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify # Hashtag 모델의 save 메서드를 위해 추가 (필요 시)


class Question(models.Model):
    # 첫 번째 Question 모델의 내용 유지
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    subject = models.CharField(max_length=200) # subject 필드 유지
    content = models.TextField()
    image = models.ImageField(upload_to="question_images/", null=True, blank=True)
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_question')

    # 두 번째 Question 모델에서 가져온 hashtags 필드 추가
    hashtags = models.ManyToManyField('Hashtag', blank=True, related_name='questions') # related_name 추가 권장

    def __str__(self):
        return self.subject

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='answer_images/', blank=True, null=True)
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_answer')
    is_accepted = models.BooleanField(default=False)

class Comment(models.Model):
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(null=True, blank=True)

class Hashtag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    # slug 필드 추가 (URL 친화적 이름을 위해 강력히 권장)
    slug = models.SlugField(max_length=50, unique=True, allow_unicode=True) 

    def save(self, *args, **kwargs):
        # slugify를 사용하여 name으로부터 slug 자동 생성
        self.slug = slugify(self.name, allow_unicode=True) 
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name