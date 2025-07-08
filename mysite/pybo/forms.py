from django import forms
from pybo.models import Question, Answer, Comment, Hashtag


class QuestionForm(forms.ModelForm):
    # 이 필드는 모델의 실제 필드가 아닙니다.
    # 사용자의 해시태그 입력을 받기 위한 폼 전용 필드입니다.
    hashtags_input = forms.CharField(
        label='해시태그 (쉼표로 구분)',
        max_length=255,
        required=False, # 필수로 입력하지 않아도 되도록 설정
        help_text='예: #수학, #물리, #화학',
        widget=forms.TextInput(attrs={'placeholder': '#태그1, #태그2'})
    )

    class Meta:
        # 이 부분이 중요합니다. class Meta는 QuestionForm 내에 딱 한 번만 정의되어야 합니다.
        model = Question
        fields = ['subject', 'content', 'image', 'is_anonymous']  # ← 익명 필드 포함
        # Question 모델에 있는 실제 필드들을 나열합니다.
        # 'hashtags_input'은 모델 필드가 아니므로 여기에 포함하지 않습니다.
        fields = ['subject', 'content', 'image']
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
    def save(self, commit=True):
        question = super().save(commit=False)

        if commit:
            question.save()
            # 이는 질문을 '수정'할 때, 기존 태그를 새로운 입력으로 덮어쓰기 위함입니다.
            # 만약 기존 태그는 유지하고 새로운 태그만 추가하고 싶다면 이 줄을 제거하세요.
            question.hashtags.clear()
            # hashtags_input 필드에서 사용자가 입력한 데이터를 가져옵니다.
            hashtags_data = self.cleaned_data.get('hashtags_input')
            if hashtags_data:
                # 입력된 문자열을 쉼표 또는 공백을 기준으로 분리하고,
                # 각 해시태그 이름에서 '#', 공백을 제거합니다.
                hashtag_names = [
                    tag.strip().replace('#', '')
                    for tag in hashtags_data.replace(',', ' ').split()
                    if tag.strip() # 비어있는 태그 이름은 제외합니다.
                ]
                # 각 해시태그 이름을 순회하며 처리합니다.
                for tag_name in hashtag_names:
                    # 해당 이름의 Hashtag 객체가 이미 존재하면 가져오고, 없으면 새로 생성합니다.
                    hashtag, created = Hashtag.objects.get_or_create(name=tag_name)
                    # 현재 질문 객체에 이 해시태그를 연결합니다.
                    question.hashtags.add(hashtag)
        return question


    def save(self, commit=True):
        question = super().save(commit=False)

        if commit:
            question.save()
            # 이는 질문을 '수정'할 때, 기존 태그를 새로운 입력으로 덮어쓰기 위함입니다.
            # 만약 기존 태그는 유지하고 새로운 태그만 추가하고 싶다면 이 줄을 제거하세요.
            question.hashtags.clear()
            # hashtags_input 필드에서 사용자가 입력한 데이터를 가져옵니다.
            hashtags_data = self.cleaned_data.get('hashtags_input')
            if hashtags_data:
                # 입력된 문자열을 쉼표 또는 공백을 기준으로 분리하고,
                # 각 해시태그 이름에서 '#', 공백을 제거합니다.
                hashtag_names = [
                    tag.strip().replace('#', '')
                    for tag in hashtags_data.replace(',', ' ').split()
                    if tag.strip() # 비어있는 태그 이름은 제외합니다.
                ]
                # 각 해시태그 이름을 순회하며 처리합니다.
                for tag_name in hashtag_names:
                    # 해당 이름의 Hashtag 객체가 이미 존재하면 가져오고, 없으면 새로 생성합니다.
                    hashtag, created = Hashtag.objects.get_or_create(name=tag_name)
                    # 현재 질문 객체에 이 해시태그를 연결합니다.
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