from django import forms
from .models import Question, Answer, Comment, Hashtag
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.text import slugify
import re

class QuestionForm(forms.ModelForm):
    hashtags_input = forms.CharField(
        label='해시태그 (쉼표로 구분)',
        max_length=255,
        required=False,
        help_text='예: #수학, #물리, #화학',
        widget=forms.TextInput(attrs={'placeholder': '해시태그를 입력하세요...', 'class': 'form-control'})
    )
    is_anonymous = forms.BooleanField(
        label='익명으로 질문하기',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Question
        fields = ['subject', 'content', 'image', 'is_anonymous', 'hashtags_input']
        labels = {
            'subject': '제목',
            'content': '내용',
            'image': '첨부 이미지',
        }
        widgets = {
            'content': forms.Textarea(attrs={'id': 'markdown-editor'})
        }

    def save(self, commit=True, **kwargs):
        question = super().save(commit=False)
        delete_image_flag = kwargs.get('delete_image_flag', False)
        if delete_image_flag and question.image:
            question.image.delete(save=False)
            question.image = None
        if commit:
            question.save()
            question.hashtags.clear()
            hashtags_data = self.cleaned_data.get('hashtags_input')
            if hashtags_data:
                processed_hashtags = hashtags_data.replace(",", " ")
                processed_hashtags = re.sub(r'\s+', ' ', processed_hashtags).strip()
                hashtag_names = [
                    tag.replace("#", "").strip()
                    for tag in processed_hashtags.split()
                    if tag.replace("#", "").strip()
                ]
                for tag_name in hashtag_names:
                    tag_slug = slugify(tag_name, allow_unicode=True)
                    
                    try:
                        hashtag = Hashtag.objects.get(slug=tag_slug)
                    except Hashtag.DoesNotExist:
                        hashtag = Hashtag.objects.create(name=tag_name, slug=tag_slug)

                    question.hashtags.add(hashtag)
        return question


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content', 'image']
        labels = {
            'content': '답변 내용',
            'image': '첨부 이미지',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'placeholder': '댓글을 입력하세요...'})
        }
        labels = {
            'content': '',
        }

class CustomPasswordChange(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['old_password'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '현재 비밀번호를 입력하세요...'
        })
        self.fields['old_password'].label = '현재 비밀번호'

        # 'new_password1' 필드 스타일 적용
        self.fields['new_password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '새 비밀번호를 입력하세요...'
        })
        self.fields['new_password1'].label = '새 비밀번호'

        # 'new_password2' 필드 스타일 적용
        self.fields['new_password2'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '새 비밀번호를 다시 입력하세요...'
        })
        self.fields['new_password2'].label = '새 비밀번호 확인'