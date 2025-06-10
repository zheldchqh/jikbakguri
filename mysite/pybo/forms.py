# pybo/forms.py (혹은 questions/forms.py, 프로젝트 구조에 따라 다름)

from django import forms
from pybo.models import Question, Answer, Comment


class QuestionForm(forms.ModelForm):
    # 여기에 is_anonymous 필드를 추가하세요
    is_anonymous = forms.BooleanField(
        label='익명으로 질문하기',
        required=False, # 필수가 아님 (체크하지 않아도 됨)
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}) # 부트스트랩 스타일 적용
    )

    class Meta:
        model = Question
        fields = ['subject', 'content', 'image', 'is_anonymous'] # 필드에 'is_anonymous' 추가
        labels = {
            'subject': '제목',
            'content': '내용',
            'image': '첨부 이미지',
        }
        widgets = {
            'content': forms.Textarea(attrs={'id': 'markdown-editor'})
        }

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