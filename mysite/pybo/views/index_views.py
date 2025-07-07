from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from ..models import UserProfile
from django.contrib.auth import logout, authenticate
from ..models import Question
from ..forms import DeleteAccountForm

''' question_list.html '''
def index(request):
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')  # 검색어
    question_list = Question.objects.order_by('-create_date')
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(answer__content__icontains=kw) |  # 답변 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()
    paginator = Paginator(question_list, 10)  # 페이지당 10개
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj, 'page': page, 'kw': kw}
    return render(request, 'pybo/question_list.html', context)

''' question_detail.html '''
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    has_answered = question.answer_set.filter(author=request.user).exists() if request.user.is_authenticated else True
    accepted = question.answer_set.filter(is_accepted=True).first()
    not_accepted = question.answer_set.filter(is_accepted=False)
    context = {'question': question, 'has_answered': has_answered, 'accepted': accepted}
    return render(request, 'pybo/question_detail.html', context)

@login_required
def accounts(request):
    return render(request, 'pybo/mypage.html', {'user': request.user})

class EditProfileForm(forms.ModelForm):
    status = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '상태 메시지를 입력하세요...'})
    )
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        self.user = kwargs.get('instance')
        initial = kwargs.setdefault('initial', {})
        if self.user:
            try:
                initial['status'] = self.user.userprofile.status
            except UserProfile.DoesNotExist:
                pass
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = super().save(commit)
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.status = self.cleaned_data['status']
        if commit:
            profile.save()
        return user

class CustomPasswordChangeForm(PasswordChangeView):
    template_name = 'pybo/change_password.html'
    success_url = '/pybo/accounts/'
    def form_valid(self, form):
        messages.success(self.request, "비밀번호가 성공적으로 변경되었습니다.")
        return super().form_valid(form)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "프로필이 성공적으로 변경되었습니다.")
            return redirect('pybo:accounts')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'pybo/edit_profile.html', {'form': form})

def user_profile(request, username):
    user_obj = get_object_or_404(User, username=username)
    ranking = User.objects.annotate(
        accepted_count=Count('author_answer', filter=Q(author_answer__is_accepted=True))
    ).order_by('-accepted_count')
    rank_dict = {u.id: idx + 1 for idx, u in enumerate(ranking)}
    try:
        profile = user_obj.userprofile
    except UserProfile.DoesNotExist:
        profile = None
    return render(request, 'pybo/user_profile.html', {
        'user_obj': user_obj,
        'profile': profile,
        'rank': rank_dict.get(user_obj.id)
    })

@login_required
def delete_account(request):
    if request.method == 'POST':
        form = DeleteAccountForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = authenticate(username=request.user.username, password=password)
            if user is not None:
                user.delete()
                logout(request)
                messages.success(request, "계정이 성공적으로 삭제되었습니다.")
                return redirect('pybo:index')
            else:
                messages.error(request, "비밀번호가 올바르지 않습니다.")
    else:
        form = DeleteAccountForm()
    return render(request, 'pybo/delete_account.html', {'form': form})