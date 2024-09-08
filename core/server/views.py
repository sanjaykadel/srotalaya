# myapp/views.py
from django.shortcuts import render
from .models import InfoSource

def index(request):
    info_sources = InfoSource.objects.all()
    category_choices = InfoSource.CATEGORY_CHOICES
    return render(request, 'server/index.html', {
        'news_sources': info_sources,
        'category_choices': category_choices
    })



