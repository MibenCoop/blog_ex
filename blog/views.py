from django.conf.urls import url
from django.core.serializers import json
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, render_to_response
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from blog.models import Category, Page, UserProfile, Comment 
from blog.forms import CategoryForm, PageForm, UserProfileForm, CommentForm
from datetime import datetime

#from django.template.defaulttags import url
from registration.backends.simple.views import RegistrationView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
import re


def index(request):
    category_list = Category.objects.order_by('name')[:5]
    page_list = Page.objects.order_by('-title')[:5]
    context_dict = {'categories': category_list, 'pages': page_list}
    return render(request, 'blog/index.html', context_dict)


def favorite(request, page_id):
    page = get_object_or_404(Page, pk=page_id)
    context_dict = {}
    try:
        if page.favorite == True:
            page.favorite = False
            page.save()
            message = page.favorite
        else:
            page.favorite = True
            page.save()
            message = page.favorite
        context_dict = {'id': page_id, 'page': page, 'message': message}
    except (KeyError, Page.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def watched_page(request, page_id):
    page = get_object_or_404(Page, pk=page_id)
    context_dict = {}
    try:
        if page.views == True:
            page.views = False
            page.save()
            message = page.views
        else:
            page.views = True
            page.save()
            message = page.views
        context_dict = {'id': page_id, 'page': page, 'message': message}
    except (KeyError, Page.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['category'] = category
        context_dict['pages'] = pages
    except:
        context_dict['category'] = None
        context_dict['pages'] = None
    return render(request, 'blog/show_category.html', context_dict)


def show_page(request, id):
    try:
        page = Page.objects.get(id=id)
    except:
        return reverse('index')
    try:
        username = request.user.username
        userprofile = UserProfile()
        if (username):
             userprofile = UserProfile.objects.get_or_create(id=request.user.id)[0]
    except:
        username = None
        userprofile = None
    like = False;dislike = False
    user = request.user
    if user:
        page = get_object_or_404(Page, id=id)
        if page.likes.filter(id=user.id).exists():
            like = True; dislike = False
        elif page.dislikes.filter(id=user.id).exists():
            dislike = True;like = False
        else:
            like = False; dislike = False
        if page.favorite.filter(id = user.id).exists():
            favorite = True
        else:
            favorite = False
    else:
        user = None
    comments = Comment.objects.filter(owner=id).order_by('-date_print')
    page.save()
    form = CommentForm()

    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author= request.user
            comment.avatar = userprofile.picture
            comment.owner = id
            comment.save()
            return HttpResponseRedirect(request.path)
        else:
            print(form.errors)


    context_dict = {'comments': comments, 'id': id, 'page': page,
                    'userprofile': userprofile,'form':form,'like':like,'dislike':dislike,
                    'favorite':favorite,}
    return render(request, 'blog/show_page.html', context_dict)


def categories_list(request):
    category_list = Category.objects.order_by('name')
    page_list = Page.objects.order_by('-title')
    user = request.user
    context_dict = {'message': "lol", 'categories': category_list, 'pages': page_list}
    return render(request, 'blog/categories_list.html', context_dict)

def about(request):
   return render(request,'blog/about.html')



def add_category(request):
    form = CategoryForm()
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=True)
            return show_category(request, category.slug)
        else:
            print(form.errors)

    return render(request, 'blog/add_category.html', {'form': form})


def add_to_feed(request,page):
    user = UserProfile.objects.get(id = request.user.id)
    page = Page.objects.get(title = page.title,author = page.author,date_print=page.date_print)
    subscribers_u = user.subscribers.all()
    subscribers = []
    for subscriber in subscribers_u:
        subscriber = UserProfile.objects.get(id = subscriber.id)
        subscribers.append(subscriber)
    for subscriber in subscribers:
        subscriber.feed.add(page)
    pass



def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    form = PageForm()
    if request.method == "POST":
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            page.category = category
            page.author = request.user
            page.save()
            #print(page)
            add_to_feed(request,page)
            return show_category(request, category_name_slug)
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'blog/add_page.html', context_dict)




@login_required
def restricted(request):
    return HttpResponse("You will see this page when log in")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))



@login_required
def register_profile(request):
    form = UserProfileForm()
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            userprofile = form.save(commit=False)
            userprofile.username = request.user
            userprofile.id = request.user.id
            userprofile.save()
            return redirect('index')
        else:
            print(form.errors)

    context_dict = {'form': form, }
    #return JsonResponse({'success': False})
    return render(request, 'blog/profile_registration.html', context_dict)



class MyRegistrationView(RegistrationView):
    def get_success_url(self,user):
        return reverse('register_profile')

@login_required
def profile(request, id):
    userprofile = UserProfile.objects.get(id = id)
    form = UserProfileForm({'picture': userprofile.picture,'gender': userprofile.gender})
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            comments = Comment.objects.filter(author = userprofile.username)
            for comment in comments:
                comment.avatar = userprofile.picture
                comment.save()
            return redirect('profile', userprofile.id)
        else:
            print(form.errors)
    context_dict = {'form': form, }

    return render(request, 'blog/profile.html', {'userprofile': userprofile,'form': form})

def delete_page(request,id):
    try:
        page = Page.objects.get(id=id)
    except:
        return reverse('index')
    category_name_slug = page.category
    comments = Comment.objects.filter(owner = id).delete()
    page = Page.objects.get(id=id).delete()
    #page.save(commit = True)
    context_dict = {'category_name_slug': category_name_slug}
    # page.views = page.views + 1
    return render(request, 'blog/index.html', context_dict)

@login_required
def edit_page(request,id):
    try:
        page = get_object_or_404(Page,id=id)
    except Page.DoesNotExist:
        return redirect('index')
    form = PageForm({'title': page.title,'content': page.content})

    if request.method == "POST":
        form = PageForm(request.POST, request.FILES, instance=page)
        if form.is_valid():
            form.save(commit=True)
            return redirect('show_page', id)
        else:
            print(form.errors)
    context_dict = {'form': form, }
    return render(request, 'blog/show_page.html', {'form': form,'id':id})



@login_required
def list_notes(request):
    username = request.user.username
    pages = Page.objects.filter(author=username).order_by('-date_print')
    context_dict = {'pages':pages,}
    return render(request, 'blog/list_notes.html', context_dict)


def delete_comment(request,id):
    try:
        comment = Comment.objects.get(id=id)
    except:
        return reverse('index')
    comment_owner = comment.owner
    comment = Comment.objects.get(id=id).delete()
    return redirect('show_page', comment_owner)


@login_required
def edit_comment(request,id):
    try:
        comment = get_object_or_404(Comment,id=id)
        page_id = comment.owner
    except Comment.DoesNotExist:
        return redirect('index')
    form = CommentForm({'content': comment.content})
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save(commit=True)
            return redirect('show_page', page_id)
        else:
            print(form.errors)
    context_dict = {'form': form,'id':id }
    return render(request, 'blog/edit_comment.html', context_dict)




@login_required
def like(request,id,):
    user = request.user
    page = get_object_or_404(Page, id=id)
    if page.likes.filter(id=user.id).exists():
        page.likes.remove(user)

    else:
        page.likes.add(user)
        page.dislikes.remove(user)
    return redirect('show_page', id)


@login_required
def dislike(request,id,):
    user = request.user
    page = get_object_or_404(Page, id=id)
    if page.dislikes.filter(id=user.id).exists():
        page.dislikes.remove(user)
    else:
        page.dislikes.add(user)
        page.likes.remove(user)
    return redirect('show_page', id)


@login_required
def favorite(request,id,):
    user = request.user
    page = get_object_or_404(Page, id=id)
    if page.favorite.filter(id=user.id).exists():
        page.favorite.remove(user)
    else:
        page.favorite.add(user)
    return redirect('show_page', id)


@login_required
def action_list(request):
    pages = Page.objects.filter(likes = request.user ).order_by('-date_print')[:5]
    favorite_pages = Page.objects.filter(favorite = request.user).order_by('-date_print')[:5]
    context_dict = { 'pages':pages ,'favorite_pages':favorite_pages }
    return render(request,'blog/action_list.html',context_dict)

def subscribe_status(request,userprofile):
    if userprofile.subscribers.filter(id = request.user.id).exists():
        subscribe = True
    else:
        subscribe = False
    return subscribe

@login_required
def profiles_list(request):
    users  = UserProfile.objects.all()
    most_popular = []
    subscribes = []
    for user in users:
        print(user.username)
        if user.total_pages > 0:
            pages = Page.objects.filter(author = user.username).order_by("-likes")[:1]
            for page in pages:
                most_popular.append(page)
        else:
            most_popular.append(0)

        if user.subscribers.filter(id=request.user.id).exists():
            subscribes.append(1)
        else:
            subscribes.append(0)
    users = zip(users,most_popular,subscribes)
    me = request.user
    context_dict = {'users':users,'me':me,}
    return render(request,'blog/profiles_list.html',context_dict)



@login_required
def person_profile(request,id):
    try:
        userprofile = UserProfile.objects.get(id=id)
    except UserProfile.DoesNotExist:
        return redirect('index')

    subscribe = subscribe_status(request,userprofile)
    pages = userprofile.pages.order_by("-likes")[:3]
    form = UserProfileForm({'picture': userprofile.picture,'gender': userprofile.gender})
    context_dict = {'form': form,'userprofile':userprofile,'pages':pages,'subscribe':subscribe }
    return render(request,'blog/person_profile.html',context_dict)

@login_required
def person_pages(request,id):
    try:
        userprofile = UserProfile.objects.get(id=id)
    except UserProfile.DoesNotExist:
        return redirect('index')
    pages = userprofile.pages.order_by("-date_print")
    context_dict = {'userprofile':userprofile,'pages':pages, }
    return render(request,'blog/person_pages.html',context_dict)

@login_required
def subscribe(request,id):
    userP = get_object_or_404(UserProfile, id = request.user.id)
    personP = get_object_or_404(UserProfile, id=id)
    person = get_object_or_404(User, id = id)

    if personP.subscribers.filter(id=request.user.id).exists():
        personP.subscribers.remove(request.user)
        userP.authors.remove(person)
    else:
        personP.subscribers.add(request.user)
        userP.authors.add(person)
    return redirect('person_profile', id)


@login_required
def user_subscribes(request,id):
    usersprofiles = UserProfile.objects.get(id = id)
    persons = usersprofiles.authors.all()
    users = []
    for person in persons:
        user = UserProfile.objects.get(id = person.id)
        users.append(user)
    context_dict = {'users':users,}
    return render(request,'blog/user_subscribes.html',context_dict)


@login_required
def feed(request):
    userprofile = UserProfile.objects.get(id = request.user.id)
    news = userprofile.feed.all()
    context_dict = {'news':news,}
    return render(request,'blog/feed.html',context_dict)















def validate_username(request):
    username = request.GET.get('username', None)
    result = re.findall(r'[a,A][d,D][m,M][i,I][n,N]',username)
    if result:
        data = {
            'is_taken': True
        }
    else:
        data = {
            'is_taken': User.objects.filter(username = username).exists()
        }

    print(data['is_taken'])
    if data['is_taken']:
        data['error_message'] = 'A user with this username already exists.'
    return JsonResponse(data)