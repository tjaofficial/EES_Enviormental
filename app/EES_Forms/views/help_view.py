from django.shortcuts import render, get_object_or_404 # type: ignore
from ..models import HelpArticle, HelpCategory

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

def help_article(request, article_id):
    article = get_object_or_404(HelpArticle, id=article_id)
    return render(request, 'shared/help_article.html', {'article': article})

