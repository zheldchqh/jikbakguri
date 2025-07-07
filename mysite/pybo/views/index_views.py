from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import Question, Hashtag
from ..forms import QuestionForm

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

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    has_answered = question.answer_set.filter(author=request.user).exists() if request.user.is_authenticated else True
    accepted = question.answer_set.filter(is_accepted=True).first()
    context = {'question': question, 'has_answered': has_answered, 'accepted': accepted}
    print("➡ detail view에서 question.hashtags:", question.hashtags.all())
    return render(request, 'pybo/question_detail.html', context)

def question_list(request):
    questions = Question.objects.all().order_by('-create_date')
    hashtags = Hashtag.objects.all()
    return render(request, 'pybo/question_list.html', {'questions': questions, 'hashtags': hashtags})

@login_required
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            return redirect('pybo:question_list')
    else:
        form = QuestionForm()
    return render(request, 'pybo/question_form.html', {'form': form})

def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    return render(request, 'pybo/question_detail.html', {'question': question})

def hashtag_detail(request, hashtag_slug):
    # URL에서 전달받은 slug를 이용해 Hashtag 객체를 찾습니다.
    # 해당 Hashtag가 없으면 404 오류를 발생시킵니다.
    hashtag = get_object_or_404(Hashtag, slug=hashtag_slug)
    
    # 해당 해시태그에 연결된 모든 질문을 가져와 최신순으로 정렬합니다.
    # (Question 모델의 ManyToManyField에 related_name='questions'가 설정되어 있다고 가정)
    questions = hashtag.questions.all().order_by('-create_date')
    
    context = {'hashtag': hashtag, 'questions': questions}
    return render(request, 'pybo/hashtag_detail.html', context)