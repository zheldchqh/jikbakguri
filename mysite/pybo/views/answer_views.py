from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import AnswerForm
from ..models import Question, Answer

'''답변 등록'''
@login_required(login_url='common:login')
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST, request.FILES)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)

'''답변 수정'''
@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('pybo:detail', question_id=answer.question.id)
    if request.method == "POST":
        form = AnswerForm(request.POST, request.FILES, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            delete_checked = 'delete_image' in request.POST
            image_uploaded = request.FILES.get('image', None)
            if delete_checked:
                if answer.image:
                    answer.image.delete(save=False)
                    answer.image = None
            if image_uploaded:
                answer.image = image_uploaded
            answer.save()
            return redirect('pybo:detail', question_id=answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'pybo/answer_form.html', context)

'''답변 삭제'''
@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제 권한이 없습니다.')
    else:
        answer.delete()
    return redirect('pybo:detail', question_id=answer.question.id)

'''답변 개추'''
@login_required(login_url='common:login')
def answer_vote(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user == answer.author:
        messages.error(request, '본인의 답변은 개추할 수 없습니다.')
    else:
        answer.voter.add(request.user)
    return redirect('pybo:detail', question_id=answer.question.id)

'''답변 채택'''
@login_required(login_url='common:login')
def answer_accept(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    question = answer.question
    # 질문자만 채택
    if request.user != question.author:
        messages.error(request, '채택할 수 없습니다.')
        return redirect('pybo:detail', question_id=question.id)
    # 채택된 답변 있는지 확인
    if question.answer_set.filter(is_accepted=True).exists():
        messages.error(request, '이미 채택된 답변이 있습니다.')
        return redirect('pybo:detail', question_id=question.id)
    # 채택
    answer.is_accepted = True
    answer.save()
    return redirect('pybo:detail', question_id=question.id)