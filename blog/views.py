from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from blog.models import Page,Category
from blog.forms import PageForm,CategoryForm
# Create your views here.
from django.urls import reverse
from registration.backends.simple.views import RegistrationView


def index(request):
    category_list = Category.objects.order_by('name')[:5]
    page_list = Page.objects.order_by('-title')[:5]
    context_dict = {'message':"Vitalii",'categories':category_list,'pages':page_list}
    return render(request,'blog/index.html',context_dict)

def show_category(request,category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['category'] = category
        context_dict['pages'] = pages
    except:
        context_dict['category'] = None
        context_dict['pages'] = None
    return render(request,'blog/categories.html',context_dict)

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
            print(category,category.slug)
            return show_category(request,category.slug)
        else:
            print(form.errors)

    return render(request,'blog/add_category.html',{'form':form})

def add_page(request,category_name_slug):
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
            return show_category(request,category_name_slug)
        else:
            print(form.errors)
    context_dict = {'form':form,'category':category}
    return render(request, 'blog/add_page.html', context_dict)

@login_required
def restricted(request):
    return HttpResponse("You will see this page when log in")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

class MyRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return reverse('register_profile')








