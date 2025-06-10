# mysite/pybo/urls.py

from django.urls import path

from .views import index_views, question_views, answer_views, comment_views

app_name = 'pybo'

urlpatterns = [
    # index_views.py에 정의된 뷰 함수들과 연결되는 URL 패턴들
    path('', index_views.index, name='index'), # 메인 페이지 (질문 목록)
    path('<int:question_id>/', index_views.detail, name='detail'), # 질문 상세 페이지

    # question_views.py에 정의된 뷰 함수들과 연결되는 URL 패턴들
    path('question/create/', question_views.question_create, name='question_create'), # 질문 등록
    path('question/modify/<int:question_id>/', question_views.question_modify, name='question_modify'), # 질문 수정
    path('question/delete/<int:question_id>/', question_views.question_delete, name='question_delete'), # 질문 삭제

    # 질문 추천(투표) URL 패턴: 템플릿에서 'pybo:vote_question'을 찾으므로 name을 'vote_question'으로 변경합니다.
    path('question/vote/<int:question_id>/', question_views.question_vote, name='vote_question'),

    # answer_views.py에 정의된 뷰 함수들과 연결되는 URL 패턴들
    path('answer/create/<int:question_id>/', answer_views.answer_create, name='answer_create'), # 답변 등록
    path('answer/modify/<int:answer_id>/', answer_views.answer_modify, name='answer_modify'), # 답변 수정
    path('answer/delete/<int:answer_id>/', answer_views.answer_delete, name='answer_delete'), # 답변 삭제

    # 답변 추천(투표) URL 패턴: 템플릿에서 'pybo:vote_answer'를 찾으므로 name을 'vote_answer'로 변경합니다.
    path('answer/vote/<int:answer_id>/', answer_views.answer_vote, name='vote_answer'), # name을 'vote_answer'로 변경!

    path('answer/accept/<int:answer_id>/', answer_views.answer_accept, name='answer_accept'), # 답변 채택

    # comment_views.py에 정의된 뷰 함수들과 연결되는 URL 패턴들
    # <<<<<<< 바로 이 부분을 수정해야 합니다!!! >>>>>>>
    path('comment/create/<int:answer_id>/', comment_views.comment_create, name='comment_create_answer'), # name='comment_create' -> 'comment_create_answer'로 변경!
    # <<<<<<< 이 라인을 위처럼 수정하고 저장해야 합니다. >>>>>>>

    path('comment/modify/<int:comment_id>/', comment_views.comment_modify, name='comment_modify'), # 댓글 수정
    path('comment/delete/<int:comment_id>/', comment_views.comment_delete, name='comment_delete'), # 댓글 삭제
]