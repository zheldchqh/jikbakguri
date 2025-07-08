# pybo/urls.py 파일

from django.urls import path
from django.contrib.auth import views as auth_views
from .views.index_views import CustomPasswordChangeForm

from .views import index_views, question_views, answer_views, comment_views, ranking_views
# from . import views  # 이 라인은 주석 처리하거나 삭제합니다.
from common import views as common_views # common 앱의 views를 common_views로 임포트

app_name = 'pybo'

urlpatterns = [
    # index_views.py
    path('', index_views.index, name='index'),
    path('<int:question_id>/', index_views.detail, name='detail'),
    path('accounts/', index_views.accounts, name='accounts'),
    path('accounts/edit_profile/', index_views.edit_profile, name='edit_profile'),
    path('accounts/change_password/', CustomPasswordChangeForm.as_view(), name='change_password'),
    path('accounts/delete/', index_views.delete_account, name='delete_account'),
    path('users/<str:username>/', index_views.user_profile, name='user_profile'),
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

    # comment_views.py
    path('comment/create/<int:answer_id>/', comment_views.comment_create, name='comment_create'),
    path('comment/modify/<int:comment_id>/', comment_views.comment_modify, name='comment_modify'),
    path('comment/delete/<int:comment_id>/', comment_views.comment_delete, name='comment_delete'),

    path('ranking/', ranking_views.user_ranking, name='user_ranking'),    
    # 댓글(Comment) 관련 URL 패턴
    path('comment/create/<int:answer_id>/', common_views.comment_create, name='comment_create_answer'),
    path('comment/modify/<int:comment_id>/', common_views.comment_modify, name='comment_modify_answer'),
    path('comment/delete/<int:comment_id>/', common_views.comment_delete, name='comment_delete_answer'),
]