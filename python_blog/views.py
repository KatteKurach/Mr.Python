from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Article, Tag, Relation, Users

def home(request):
    context = {}
    if request.GET.get('log'):
        return render(request, 'python_blog/log.html', {})
    if request.GET.get('sign'):
        return redirect('/home/sign/') 
    if request.GET.get('search_btn'):
        print request.GET.get('search_s')
    return render(request, 'python_blog/main.html', context)

def archive(request): 
    articles = Article.objects.all()
    arch = []

    for a in articles:
        arch.append((a.header, a.date, a.text[:500] + '...'))
    context = {'archive': arch}
    return render(request, 'python_blog/archive.html', context)



def log(request):
    return render(request, 'python_blog/log.html', {})

def sign(request):
    if request.POST.get('btn_sign'):
        name = request.POST.get('user_name')
        new_email = request.POST.get('in_email')
        new_password = request.POST.get('in_password')
        conf = request.POST.get('in_conf')
        if (new_password == conf and len(Users.objects.filter(email = new_email)) == 0):
            new_user = Users(username = name, email = new_email, password = new_password)
            new_user.save()
            return render(request, 'python_blog/main.html', {})
    return render(request, 'python_blog/sign.html', {})

def blog(request):
    temp = Article.objects.all()[0]
    context = {'data': [temp.header, temp.date, temp.text]}
    return render(request, 'python_blog/blog.html', context)

