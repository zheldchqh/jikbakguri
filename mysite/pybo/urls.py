from django.urls import path

from .views import index_views, question_views, answer_views, comment_views

app_name = 'pybo'

urlpatterns = [
    # index_views.py
    path('', index_views.index, name='index'),
    path('<int:question_id>/', index_views.detail, name='detail'),

    # question_views.py
    path('question/create/', question_views.question_create, name='question_create'),
    path('question/modify/<int:question_id>/', question_views.question_modify, name='question_modify'),
    path('question/delete/<int:question_id>/', question_views.question_delete, name='question_delete'),

    path('question/vote/<int:question_id>/', question_views.question_vote, name='question_vote'),

    # answer_views.py
    path('answer/create/<int:question_id>/', answer_views.answer_create, name='answer_create'),
    path('answer/modify/<int:answer_id>/', answer_views.answer_modify, name='answer_modify'),
    path('answer/delete/<int:answer_id>/', answer_views.answer_delete, name='answer_delete'),

    path('answer/vote/<int:answer_id>/', answer_views.answer_vote, name='answer_vote'),

    path('answer/accept/<int:answer_id>/', answer_views.answer_accept, name='answer_accept'),

    # comment_views.py
    path('comment/create/<int:answer_id>/', comment_views.comment_create, name='comment_create'),
    path('comment/modify/<int:comment_id>/', comment_views.comment_modify, name='comment_modify'),
    path('comment/delete/<int:comment_id>/', comment_views.comment_delete, name='comment_delete'),
]