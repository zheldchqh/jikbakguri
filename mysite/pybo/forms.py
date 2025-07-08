from django import forms
from pybo.models import Question, Answer, Comment


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject', 'content', 'image', 'is_anonymous']  # ← 익명 필드 포함
        labels = {
            'subject': '제목',
            'content': '내용',
            'image': '첨부 이미지',
            'is_anonymous': '익명으로 질문하시겠습니까?',
        }
        widgets = {
            'content': forms.Textarea(attrs={'id': 'markdown-editor'}),
            'is_anonymous': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content', 'image']
        labels = {
            'content': '답변 내용',
            'image': '첨부 이미지',
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows': 8, 'placeholder': '답변을 입력하세요...'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {'content': ''}
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'placeholder': '댓글을 입력하세요...'}),
        }
        labels = {
            'content': '',
        }

class DeleteAccountForm(forms.Form):
    password = forms.CharField(
        label="비밀번호 확인",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )