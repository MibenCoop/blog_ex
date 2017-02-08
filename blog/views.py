from django.conf.urls import url
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from blog.models import Category, Page, UserProfile
from blog.forms import CategoryForm, PageForm, UserProfileForm
from datetime import datetime

#from django.template.defaulttags import url
from registration.backends.simple.views import RegistrationView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login, logout


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
    message = "hey"
    context_dict = {'message': message, 'id': id, 'page': page}
    # page.views = page.views + 1
    page.save()
    return render(request, 'blog/show_page.html', context_dict)


def categories_list(request):
    category_list = Category.objects.order_by('name')
    page_list = Page.objects.order_by('-title')
    context_dict = {'message': "Vitalii", 'categories': category_list, 'pages': page_list}
    return render(request, 'blog/categories_list.html', context_dict)


def add_category(request):
    form = CategoryForm()
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=True)
            print(category, category.slug)
            return show_category(request, category.slug)
        else:
            print(form.errors)

    return render(request, 'blog/add_category.html', {'form': form})


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
            page.save()
            print(page)
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
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
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
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('index')

    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm({'picture': userprofile.picture,'gender': userprofile.gender})

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('profile', user.username)
        else:
            print(form.errors)
    context_dict = {'form': form, }

    return render(request, 'blog/profile.html', {'userprofile': userprofile, 'selecteduser': user, 'form': form})
