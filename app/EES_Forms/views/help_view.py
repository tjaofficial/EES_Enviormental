from django.shortcuts import render, get_object_or_404 # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.views.decorators.csrf import csrf_exempt # type: ignore
from django.http import JsonResponse # type: ignore
from django.db.models import Q # type: ignore
from ..models import HelpArticle, HelpCategory, ArticleFeedback
import json

lock = login_required(login_url='Login')

@lock
def help_center(request):
    query = request.GET.get('q', '')
    categories = HelpCategory.objects.all()
    if query:
        articles = HelpArticle.objects.filter(title__icontains=query)
    else:
        articles = HelpArticle.objects.all()
    return render(request, 'shared/help_center.html', {
        'categories': categories,
        'articles': articles,
        'query': query
    })

@lock
def help_article(request, article_id):
    article = get_object_or_404(HelpArticle, id=article_id)
    return render(request, 'shared/help_article.html', {'article': article})

@lock
@csrf_exempt
def submit_feedback(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            article_id = data.get('article_id')
            value = data.get('value')  # should be 'yes' or 'no'

            article = HelpArticle.objects.get(id=article_id)
            was_helpful = True if value == 'yes' else False

            ArticleFeedback.objects.create(
                article=article,
                was_helpful=was_helpful,
                user_ip=request.META.get('REMOTE_ADDR')
            )

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=405)

@lock
def search_suggestions(request):
    query = request.GET.get('q', '')
    suggestions = []

    if query:
        articles = HelpArticle.objects.filter(
            Q(title__icontains=query) |
            Q(tags__icontains=query)
        ).distinct()[:8]

        suggestions = [
            {'title': a.title, 'url': f'/help/article/{a.id}/'}
            for a in articles
        ]

    return JsonResponse({'results': suggestions})






