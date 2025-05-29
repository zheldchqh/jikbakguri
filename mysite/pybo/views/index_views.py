from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from ..models import Question

''' main '''
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

''' question_detail '''
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    has_answered = question.answer_set.filter(author=request.user).exists() if request.user.is_authenticated else True
    accepted = question.answer_set.filter(is_accepted=True).first()
    not_accepted = question.answer_set.filter(is_accepted=False)
    context = {'question': question, 'has_answered': has_answered, 'accepted': accepted}
    return render(request, 'pybo/question_detail.html', context)