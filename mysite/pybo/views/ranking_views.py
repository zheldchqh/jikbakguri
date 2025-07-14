from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.shortcuts import render

def user_ranking(request):
    ranking = User.objects.annotate(
        accepted_count=Count('author_answer', filter=Q(author_answer__is_accepted=True))
    ).order_by('-accepted_count')

    return render(request, 'pybo/user_ranking.html', {'ranking': ranking})