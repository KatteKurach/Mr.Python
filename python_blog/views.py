from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.serializers.json import DjangoJSONEncoder
from .models import *
from collections import defaultdict
import operator
import json


from django.contrib.auth.models import User as u
from django.contrib.auth import authenticate, login, logout


def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == "google-oauth2":
        print '_______here________'
        # do something


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
        ans.append((i.header, str(i.date)[:10], i.text[:250], i.id))
    return ans


def saveArticle(id, header, text):
    art = Article.objects.filter(pk = int(id))[0]
    art.header = header
    art.text = text
    art.save()


def deleteArticle(id):
    Article.objects.filter(pk = int(id)).delete()


def admin(request):
    if request.GET.get('type') and request.GET.get('type') == 'save':
        id = request.GET.get('id')
        header = request.GET.get('header')
        text = request.GET.get('article')
        saveArticle(id, header, text)

    elif request.GET.get('type') and request.GET.get('type') == 'delete':
        id = request.GET.get('id')
        deleteArticle(id)

    if request.GET.get('id'):
        article_id = request.GET.get('id')
        article = Article.objects.filter(pk=int(article_id))[0]
        data = {'article': article.text, 'title': article.header}
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')

    names = []
    art = []
    for a in Article.objects.all():
        names.append([a.id, a.header])
        art.append(a.text)
    names[0][1] = names[0][1].strip()
    context = {'articls': names, 'view_article': art[0]}
    if request.POST.get('save'):
        print request.GET.get('text')
    return render(request, 'python_blog/home_admin.html', context)


def home(request):
    context = {'user': True}
    if request.user.is_authenticated:
        if request.user.social_auth.filter(provider='google-oauth2'):
            if len(Users.objects.filter(email=request.user.email)) == 0:
                new_user = Users(username=request.user.username,
                                 email=request.user.email,
                                 password='google')
                new_user.save()
                if len(u.objects.filter(email=request.user.email)) == 0:
                    add_u = u.objects.create_user(request.user.username, request.user.email, 'google')
                    add_u.save()
            print 'user is using Google Account!'
        if request.user.social_auth.filter(provider='github'):
            if len(Users.objects.filter(email=request.user.email)) == 0:
                new_user = Users(username=request.user.username,
                                 email=request.user.email,
                                 password='github')
                new_user.save()
                if len(u.objects.filter(email=request.user.email)) == 0:
                    add_u = u.objects.create_user(request.user.username, request.user.email, 'github')
                    add_u.save()
            print 'user is using Github Account!'
        context['user'] = False
    if request.GET.get('log_out'):
        logout(request)
    if request.GET.get('query'):
        s = request.GET.get('query')
        if s != '':
            articles = getArticles(s)
        return HttpResponse(json.dumps(articles, cls=DjangoJSONEncoder), content_type='application/json')
    return render(request, 'python_blog/main.html', context)


def archive(request):
    articles = Article.objects.all()
    arch = []
    for a in articles:
        arch.append((a.header, a.date, a.text[:500] + '...', a.id))
    context = {'archive': arch}
    return render(request, 'python_blog/archive.html', context)


def log(request):
    if request.GET.get('btn_log'):
        g_email = request.GET.get('email_s')
        g_password = request.GET.get('password_s')
        name = Users.objects.filter(email=g_email)
        print g_email
        if (len(name) == 0):
            data =  {'status': 'error'}
            return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')
        name = name[0]
        check_user = authenticate(username = name.username, password=g_password)

        if check_user is not None:
            if check_user.is_active:
                login(request, check_user)
                data =  {'status': 'ok'}
                if name.username == 'ekaterina_bloger_python':
                    return redirect('/home/hadmin/')
                    data = {'status': 'admin'}
                return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')
        else:
            data = {'status': 'error'}
            return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')
    return render(request, 'python_blog/log.html', {})


def sign(request):
    if request.GET.get('btn_sign'):
        name = request.GET.get('user_name')
        new_email = request.GET.get('in_email')
        new_password = request.GET.get('in_password')
        conf = request.GET.get('in_conf')

        if len(Users.objects.filter(email = new_email)) == 0:
            new_user = Users(username = name, email = new_email,
                             password = new_password)
            new_user.save()
            add_u = u.objects.create_user(name, new_email, new_password)
            add_u.save()
            data =  {'status': 'ok'}
        else:
            data = {'status': 'bad_email'}
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')
    return render(request, 'python_blog/sign.html', {})


def add_comment(article_id, request):
    text = request.GET.get('text_comment')
    if request.user.is_authenticated:
        u_email = request.user.email
        u = Users.objects.filter(email = u_email)[0]
        new_com = Comments(username = u, value = text)
        new_com.save()
        new_rel = CommentsToArticles(arcticle = Article.objects.filter(pk=int(article_id))[0], \
                comment = new_com)
        new_rel.save()
        return True
    return False


def getLikes(article_id):
    likes = Likes.objects.filter(article = article_id)
    return len(likes)


def addLike(article_id, request):
    if request.user.is_authenticated:
        u_email = request.user.email
        u = Users.objects.filter(email=u_email)[0]
        user_like = Likes.objects.filter(user=u, article=Article.objects.filter(pk=int(article_id))[0])
        if len(user_like) < 1:
            new_like = Likes(article=Article.objects.filter(pk=int(article_id))[0], user=u)
            new_like.save()
        return True
    return False


def blog(request, article_id):
    if request.GET.get('btn_add'):
        result = add_comment(article_id,  request)
        data =  {'status': 'ok', 'user': str(request.user)}
        if result == False:
            data['status'] = 'error'
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')

    if request.GET.get('btn_like'):
        result = addLike(article_id, request)
        likes = getLikes(article_id)
        data =  {'status': 'ok', 'likes': likes}
        if result == False:
            data['status'] = 'error'
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')

    temp = Article.objects.filter(pk=article_id)[0]
    comments = CommentsToArticles.objects.filter(arcticle=temp)
    com = []
    for i in comments:
        com.append([i.comment.username.username, i.comment.value])
    context = {'log_user': request.user, 'data': [temp.header, temp.date, temp.text], \
            'comments': com, 'cal_likes': getLikes(article_id)}
    return render(request, 'python_blog/blog.html', context)
