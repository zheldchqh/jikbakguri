# pybo/urls.py 파일

from django.urls import path
# from . import views  # 이 라인은 주석 처리하거나 삭제합니다.
from common import views as common_views # common 앱의 views를 common_views로 임포트

app_name = 'pybo'

urlpatterns = [
    # Index & Detail
    path('', common_views.index, name='index'),
    path('<int:question_id>/', common_views.detail, name='detail'),

    # Question CRUD & Vote
    path('question/create/', common_views.question_create, name='question_create'),
    path('question/modify/<int:question_id>/', common_views.question_modify, name='question_modify'),
    path('question/delete/<int:question_id>/', common_views.question_delete, name='question_delete'),
    path('question/vote/<int:question_id>/', common_views.question_vote, name='vote_question'),

    # Answer CRUD, Vote, Accept
    path('answer/create/<int:question_id>/', common_views.answer_create, name='answer_create'),
    path('answer/modify/<int:answer_id>/', common_views.answer_modify, name='answer_modify'),
    path('answer/delete/<int:answer_id>/', common_views.answer_delete, name='answer_delete'),
    path('answer/vote/<int:answer_id>/', common_views.answer_vote, name='vote_answer'),
    path('answer/accept/<int:answer_id>/', common_views.answer_accept, name='answer_accept'),

    # 댓글(Comment) 관련 URL 패턴
    path('comment/create/<int:answer_id>/', common_views.comment_create, name='comment_create_answer'),
    path('comment/modify/<int:comment_id>/', common_views.comment_modify, name='comment_modify_answer'),
    path('comment/delete/<int:comment_id>/', common_views.comment_delete, name='comment_delete_answer'),
]