from django.shortcuts import render
from blog.models import Post
from mailings.models import Mailing
from mailings.models import Client


def index(request):
    """Отображение главной страницы"""
    unique_client_count = Client.objects.values('email').distinct().count()
    mailing_count = Mailing.objects.all().count()
    active_mailing_count = Mailing.objects.filter(status='start').count()
    new_posts = Post.objects.order_by('-id')[:3]
    context = {
        'unique_client_count': unique_client_count,
        'mailing_count': mailing_count,
        'active_mailing_count': active_mailing_count,
        'new_posts': new_posts,
    }
    return render(request, 'main/index.html', context)
