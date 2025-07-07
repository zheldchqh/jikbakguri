# pybo/urls.py

from django.urls import path, re_path
# 뷰 함수들을 직접 임포트하여 혼동을 줄입니다.
from .views import index_views, question_views, answer_views, comment_views
# 해시태그 관련 뷰가 views.py의 어떤 파일에 있는지 확인하고 임포트합니다.
# 만약 `views/hashtag_views.py`가 따로 있다면 `from .views import hashtag_views` 추가
# 현재는 `index_views`에 있다고 가정하고 작성합니다.

app_name = 'pybo'

urlpatterns = [
    # index_views.py (기존 목록 및 상세)
    path('', index_views.index, name='index'),
    path('<int:question_id>/', index_views.detail, name='detail'),

    # question_views.py (기존 질문 관련)
    path('question/create/', question_views.question_create, name='question_create'),
    path('question/modify/<int:question_id>/', question_views.question_modify, name='question_modify'),
    path('question/delete/<int:question_id>/', question_views.question_delete, name='question_delete'),
    path('question/vote/<int:question_id>/', question_views.question_vote, name='question_vote'),

    # answer_views.py (기존 답변 관련)
    path('answer/create/<int:question_id>/', answer_views.answer_create, name='answer_create'),
    path('answer/modify/<int:answer_id>/', answer_views.answer_modify, name='answer_modify'),
    path('answer/delete/<int:answer_id>/', answer_views.answer_delete, name='answer_delete'),
    path('answer/vote/<int:answer_id>/', answer_views.answer_vote, name='answer_vote'),
    path('answer/accept/<int:answer_id>/', answer_views.answer_accept, name='answer_accept'),

    # comment_views.py (기존 댓글 관련)
    path('comment/create/<int:answer_id>/', comment_views.comment_create, name='comment_create'),
    path('comment/modify/<int:comment_id>/', comment_views.comment_modify, name='comment_modify'),
    path('comment/delete/<int:comment_id>/', comment_views.comment_delete, name='comment_delete'),

    # Hashtag 관련 URL (index_views에 포함되어 있다고 가정)
    re_path(r'^hashtags/(?P<hashtag_slug>[\w가-힣]+)/$', index_views.hashtag_detail, name='hashtag_detail'),
]