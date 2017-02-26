from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.serializers.json import DjangoJSONEncoder
from .models import Article, Tag, Relation, Users
from collections import defaultdict
import operator
import json


from django.contrib.auth.models import User as u
from django.contrib.auth import authenticate, login


def remake(s):
    s = s.strip().lower()
    temp = s.split(' ')
    tags = []
    for tag in temp:
        if tag != '':
            tags.append(tag)
    return tags


def getArticles(s):
    articles = defaultdict()
    for tag in remake(s):
        art = Relation.objects.filter(tag=Tag.objects.filter(value=tag))
        for i in art:
            i = i.article
            if i in articles:
                articles[i] += 1
            else:
                articles[i] = 1
    sorted_article = sorted(articles.items(), key = operator.itemgetter(1),\
            reverse = True)
    ans = []
    for i in sorted_article:
        i = i[0]
        ans.append((i.header, i.date, i.text, i.id))
    return ans


def admin(request):
    if request.GET.get('id'):
        article_id = request.GET.get('id')
        text = Article.objects.filter(pk=int(article_id))[0].text
        print text
        return HttpResponse(json.dumps(text, cls=DjangoJSONEncoder), content_type='application/json')

    names = []
    art = []
    for a in Article.objects.all():
        names.append([a.id, a.header])
        art.append(a.text)
    context = {'articls': names, 'view_article': art[0]}
    if request.POST.get('save'):
        print request.GET.get('text')
    return render(request, 'python_blog/home_admin.html', context)


def home(request):
    context = {}
    if request.GET.get('log'):
        return redirect('/home/log/')
    if request.GET.get('sign'):
        return redirect('/home/sign/') 
    if request.GET.get('query'):
        s = request.GET.get('query')
        articles = getArticles(s)
        return HttpResponse(json.dumps(articles, cls=DjangoJSONEncoder), content_type='application/json')
    return render(request, 'python_blog/main.html', context)


def archive(request): 
    articles = Article.objects.all()
    arch = []
    for a in articles:
        arch.append((a.header, a.date, a.text[:500] + '...'))
    context = {'archive': arch}
    return render(request, 'python_blog/archive.html', context)


def log(request):
    if request.POST.get('btn_log'):
        g_email = request.POST.get('email_s')
        g_password = request.POST.get('password_s')
        name = Users.objects.filter(email=g_email)[0]
        check_user = authenticate(username = name.username, password=g_password)
        
        if check_user is not None:
            if check_user.is_active:
                login(request, check_user)
                if name.username == 'ekaterina_bloger_python':
                    return redirect('/home/hadmin/')
                return redirect('/home/')
    return render(request, 'python_blog/log.html', {})


def sign(request):
    if request.POST.get('btn_sign'):
        name = request.POST.get('user_name')
        new_email = request.POST.get('in_email')
        new_password = request.POST.get('in_password')
        conf = request.POST.get('in_conf')

        if (new_password == conf and \
                len(Users.objects.filter(email = new_email)) == 0):
            new_user = Users(username = name, email = new_email, \
                    password = new_password)

            new_user.save()
            add_u = u.objects.create_user(name, new_email, new_password)
            add_u.save()
            return redirect('/home/')
    return render(request, 'python_blog/sign.html', {})


def blog(request, article_id):
    temp = Article.objects.filter(pk=article_id)[0]
    context = {'data': [temp.header, temp.date, temp.text]}
    return render(request, 'python_blog/blog.html', context)
