# common/views.py 파일

# --- 필요한 임포트 (common/views.py에 모두 모아야 합니다) ---
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q # 검색 기능에 필요
from django.core.paginator import Paginator # 페이징에 필요

# 이제 pybo 앱의 모델과 폼을 common/views.py에서 직접 임포트해야 합니다.
# 경로는 '앱이름.models' 또는 '앱이름.forms' 형태가 됩니다.
from pybo.models import Question, Answer, Comment # pybo 앱의 모델들
from pybo.forms import QuestionForm, AnswerForm, CommentForm # pybo 앱의 폼들
from .forms import UserForm # common 앱의 UserForm

# 기존에 from django.urls import reverse as resolve_url 가 맨 아래에 있었는데,
# 이를 맨 위쪽 임포트 문들과 함께 옮겨두는 것이 좋습니다.
from django.urls import reverse # resolve_url 대신 reverse를 직접 임포트합니다.

# --- 로그인/회원가입 (common 앱의 역할) ---
def logout_view(request):
    logout(request)
    return redirect('pybo:index')

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.save()
            login_user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password1'))
            if login_user:
                login(request, login_user)
            messages.success(request, '회원가입 및 로그인이 완료되었습니다.')
            return redirect('pybo:index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})

# --- pybo 앱 관련 뷰 함수들 (이 모든 함수들이 common/views.py에 있어야 합니다!) ---

def index(request):
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')

    question_list = Question.objects.order_by('-create_date')
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(answer__content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(answer__author__username__icontains=kw)
        ).distinct()

    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj, 'page': page, 'kw': kw}
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answer_form = AnswerForm()
    context = {'question': question, 'answer_form': answer_form}
    return render(request, 'pybo/question_detail.html', context)


@login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.is_anonymous = form.cleaned_data['is_anonymous']
            question.save()
            messages.success(request, '질문이 성공적으로 등록되었습니다.')
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = QuestionForm()
    return render(request, 'pybo/question_form.html', {'form': form})


@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('pybo:detail', question_id=question.id)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now() # 수정일시 저장
            question.save()
            messages.success(request, '질문이 수정되었습니다.')
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    return render(request, 'pybo/question_form.html', {'form': form})

@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제 권한이 없습니다.')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    messages.success(request, '질문이 삭제되었습니다.')
    return redirect('pybo:index')

@login_required(login_url='common:login')
def question_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.user == question.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다.')
    elif request.user in question.voter.all():
        messages.info(request, '이미 추천하셨습니다.')
    else:
        question.voter.add(request.user)
        messages.success(request, '질문을 추천했습니다.')

    return redirect('pybo:detail', question_id=question.id)

# --- 답변 (Answer) 관련 뷰 함수들 ---
@login_required(login_url='common:login')
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            messages.success(request, '답변이 성공적으로 등록되었습니다.')
            # 여기가 수정될 부분!
            detail_url = reverse('pybo:detail', kwargs={'question_id': question.id})
            return redirect(f"{detail_url}#answer_{answer.id}")
            
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)


@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('pybo:detail', question_id=answer.question.id)

    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            messages.success(request, '답변이 수정되었습니다.')
            return redirect('pybo:detail', question_id=answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form} # 수정폼에 답변 객체 전달
    return render(request, 'pybo/answer_form.html', context)

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제 권한이 없습니다.')
        return redirect('pybo:detail', question_id=answer.question.id)
    answer.delete()
    messages.success(request, '답변이 삭제되었습니다.')
    return redirect('pybo:detail', question_id=answer.question.id)

@login_required(login_url='common:login')
def answer_vote(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user == answer.author:
        messages.error(request, '본인이 작성한 답변은 추천할 수 없습니다.')
    elif request.user in answer.voter.all():
        messages.info(request, '이미 추천하셨습니다.')
    else:
        answer.voter.add(request.user)
        messages.success(request, '답변을 추천했습니다.')
    return redirect('pybo:detail', question_id=answer.question.id)

@login_required(login_url='common:login')
def answer_accept(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    # 질문 작성자만 답변을 채택할 수 있도록 권한 확인
    if request.user != answer.question.author:
        messages.error(request, '답변 채택 권한이 없습니다.')
        return redirect('pybo:detail', question_id=answer.question.id)

    # 이미 채택된 답변이 있는지 확인 (선택 사항: 여러 답변 채택 허용 여부에 따라)
    if answer.question.answer_set.filter(is_accepted=True).exists():
        messages.info(request, '이미 채택된 답변이 있습니다.')
        return redirect('pybo:detail', question_id=answer.question.id)

    answer.is_accepted = True
    answer.save()
    messages.success(request, '답변이 채택되었습니다.')
    return redirect('pybo:detail', question_id=answer.question.id)

# --- 댓글 (Comment) 관련 뷰 함수들 ---
@login_required(login_url='common:login')
def comment_create(request, answer_id): # 답변에 대한 댓글
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.answer = answer # 답변과 연결
            comment.save()
            messages.success(request, '댓글이 성공적으로 등록되었습니다.')
            return redirect('pybo:detail', question_id=answer.question.id)
    else:
        form = CommentForm()
    context = {'answer': answer, 'form': form}
    return render(request, 'pybo/question_detail.html', context) # 질문 상세 페이지로 리디렉션

@login_required(login_url='common:login')
def comment_modify(request, comment_id): # 댓글 수정
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('pybo:detail', question_id=comment.answer.question.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.modify_date = timezone.now()
            comment.save()
            messages.success(request, '댓글이 수정되었습니다.')
            return redirect('pybo:detail', question_id=comment.answer.question.id)
    else:
        form = CommentForm(instance=comment)
    context = {'comment': comment, 'form': form}
    return render(request, 'pybo/comment_form.html', context) # comment_form.html 템플릿 필요

@login_required(login_url='common:login')
def comment_delete(request, comment_id): # 댓글 삭제
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '삭제 권한이 없습니다.')
        return redirect('pybo:detail', question_id=comment.answer.question.id)
    comment.delete()
    messages.success(request, '댓글이 삭제되었습니다.')
    return redirect('pybo:detail', question_id=comment.answer.question.id)

# resolve_url 함수는 장고의 urls에서 URL을 반환하는데 사용됩니다.
# answer_create에서 redirect를 위해 사용될 수 있습니다.
# 이 라인은 이제 필요 없습니다. 맨 위로 옮겨서 reverse를 직접 임포트했습니다.
# from django.urls import reverse as resolve_url