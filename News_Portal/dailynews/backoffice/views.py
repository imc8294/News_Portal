from hashlib import md5
import os
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from backoffice.models import Category, DisplaySection
from backoffice.models import NewsData
from django.core.files.storage import FileSystemStorage
from backoffice.models import AdminUser

# Create your views here.
def dashboard(request):
    if 'admin-login' in request.session:
        data = {
            'admin_name': request.session['admin-data']['adminName'], 
            'menu_name': 'dashboard',
            'sub_menu': 'dashboard'
        }
        return render(request, 'backoffice/dashboard.html', data)
    else:
        return HttpResponseRedirect('/backoffice/login')
    
def login(request):
    if 'admin-login' in request.session:
        return HttpResponseRedirect('/backoffice/dashboard')
    else:
        return render(request, 'backoffice/login.html')

def submitLogin(request):
    if request.method=="POST":
        email=request.POST['email']
        password = request.POST['password']
        if email and password:
            encode_password = md5(password.encode())
            admin_data = AdminUser.objects.filter(
                email = email,
                password = encode_password.hexdigest()
            ) 
            if admin_data:
                adminDetails = {}
                for data in admin_data:
                    adminDetails['adminName'] = data.name
                    adminDetails['adminEmail'] = data.email
                    adminDetails['adminId'] = data.id
                request.session['admin-login'] = True
                request.session['admin-data'] = adminDetails
                return HttpResponseRedirect('/backoffice/dashboard')
        else:
            return HttpResponseRedirect('/backoffice/login')
    return HttpResponseRedirect('/backoffice/login')

def news_category(request):
    if 'admin-login' in request.session:
        category_data = Category.objects.all()
        data = {
            'admin_name': request.session['admin-data']['adminName'],
            'category_data' : category_data,
            'menu_name': 'category',
            'sub_menu': 'view_category'
        }
        return render(request, 'backoffice/category.html', data)
    else:
       return HttpResponseRedirect('/backoffice/login') 
    
def add_category(request):
    if 'admin-login' in request.session:
        data = {
            'admin_name': request.session['admin-data']['adminName'],
            'menu_name': 'category',
            'sub_menu': 'add_category'
            
            }
        return render(request, 'backoffice/add_category.html', data)
    else:
        return HttpResponseRedirect('/backoffice/login')
    
def save_category(request):
    update=''
    if request.method == "POST":
        category_name=request.POST.get('Name')
        category_status=request.POST.get('Status')
        category_order=request.POST.get('Order')
        cat_created_date=request.POST.get('Date')
        values = Category(category_name=category_name, category_status=category_status, category_order=category_order, cat_created_date=cat_created_date)
        values.save()
        update='Data Inserted'
    return HttpResponseRedirect('/backoffice/add_category', {'update' : update})

def edit_category(request, id):
    if 'admin-login' in request.session:
        queryset = Category.objects.get(id = id)
        data = {
            'cat':queryset,
            'menu_name': 'category',
            'sub_menu': 'edit_category'
        }
        return render(request,'backoffice/add_category.html',data)
    else:
        return HttpResponseRedirect('/backoffice/login')

def update_category(request):
    if 'admin-login' in request.session:
        if request.method == "POST":
            category_id = request.POST.get('category_id')
            category_name=request.POST.get('Name')
            category_status=request.POST.get('Status')
            category_order=request.POST.get('Order')
            cat_created_date=request.POST.get('Date')
            queryset = Category.objects.get(id = category_id)
            queryset.category_name=category_name
            queryset.category_status=category_status
            queryset.category_order=category_order
            queryset.cat_created_date=cat_created_date
            queryset.save()
        return HttpResponseRedirect('/backoffice/news_cat')
    else:
        return HttpResponseRedirect('/backoffice/login')

def delete_category(request, id):
    if 'admin-login' in request.session:
        values = Category.objects.get(id = id)
        values.delete()
        return HttpResponseRedirect('/backoffice/news_cat')
    else:
        return HttpResponseRedirect('/backoffice/login')
    
def add_newsdata(request):
    if 'admin-login' in request.session:
        category_data = Category.objects.filter(
            category_status = 1
        )

        display_data = DisplaySection.objects.filter(
            display_status = 1
        )

        data = {
            'admin_name': request.session['admin-data']['adminName'],
            'category_data' : category_data,
            'display_data': display_data,
            'menu_name': 'NewsData',
            'sub_menu': 'view_category'
        }
        return render(request, 'backoffice/add_newsdata.html', data)
    else:
        return HttpResponseRedirect('/backoffice/login')

def save_newsdata(request):
    if 'admin-login' in request.session:
        if request.method == "POST":
            uploaded_file_url = ''
            if request.FILES:
                file_data = request.FILES['news_file']
                fs = FileSystemStorage()
                filename = fs.save(file_data.name, file_data)
                uploaded_file_url = fs.url(filename)
            news_title = request.POST.get('Title')
            news_category = int(request.POST.get('category'))
            category_data = Category.objects.get(
                id = news_category
            )
            news_source = request.POST.get('Source')
            news_content = request.POST.get('content')
            publish_date = request.POST.get('Date')
            news_status = request.POST.get('Status')
            news_urls = request.POST.get('Urls')
            display_section = request.POST.get('display_section')
            values = NewsData(display_section=display_section, tittle=news_title, category=category_data, source=news_source, image=uploaded_file_url, content=news_content, created_date=publish_date, news_status=news_status, url_slug=news_urls)
            values.save()
        return HttpResponseRedirect('/backoffice/add_newsdata')  
    else:
        return HttpResponseRedirect('/backoffice/login')
    
def view_newsdata(request):
    if 'admin-login' in request.session:
        News_data = NewsData.objects.all()
        data = {
            'admin_name': request.session['admin-data']['adminName'],
            'News_data' : News_data,
            'menu_name': 'NewsData',
            'sub_menu': 'view_NewsData',
            
        }
        return render(request, 'backoffice/view_newsdata.html', data)
    else:
        return HttpResponseRedirect('/backoffice/login')


def edit_newsdata(request, id):
    if 'admin-login' in request.session:
        update=''    
        news_data = NewsData.objects.get(id = id)
        category_data = Category.objects.filter(
            category_status = 1
        )
        display_data = DisplaySection.objects.filter(
            display_status = 1
        )
        
        data = {
            'admin_name': request.session['admin-data']['adminName'],
            'edit_news_data': news_data,
            'menu_name': 'NewsData',
            'sub_menu': 'edit_newsdata',
            'display_data': display_data,
            'category_data': category_data,
            
        }
        return render(request,'backoffice/edit_newsdata.html', data)
    else:
        return HttpResponseRedirect('/backoffice/login')

def update_newsdata(request):
    if 'admin-login' in request.session:
        if request.method == "POST":
            title = request.POST.get('Title')
            category=int(request.POST.get('category'))
            category_data = Category.objects.get(
                id = category
            )
            source=request.POST.get('Source')
            
            uploaded_file_url = request.POST.get('old_image')
            if request.FILES.get('news_file'):
                file_data = request.FILES['news_file']
                fs = FileSystemStorage()
                filename = fs.save(file_data.name, file_data)
                #os.remove(uploaded_file_url)
                uploaded_file_url = fs.url(filename)
            news_id = request.POST.get('News_id')
            content=request.POST.get('content')
            publish_date=request.POST.get('Date')
            status=request.POST.get('Status')
            urls=request.POST.get('Urls')
            display_section = request.POST.get('display_section')
            querydata = NewsData.objects.get(id = news_id)
            querydata.tittle=title
            querydata.category=category_data
            querydata.source=source
            querydata.image=uploaded_file_url
            querydata.content=content
            querydata.created_date=publish_date
            querydata.news_status=status
            querydata.url_slug=urls
            querydata.display_section = display_section
            querydata.save()
            
        return HttpResponseRedirect('/backoffice/view_newsdata')
    else:
        return HttpResponseRedirect('/backoffice/login')


def delete_newsdata(request, id):
    if 'admin-login' in request.session:
        values = NewsData.objects.get(id = id)
        values.delete()
        return HttpResponseRedirect('/backoffice/view_newsdata')
    else:
        return HttpResponseRedirect('/backoffice/login')


def logout(request):
    try:
        del request.session['admin-login']
        del request.session['admin-data']
    except:
        return HttpResponseRedirect('/backoffice/login')
    return HttpResponseRedirect('/backoffice/login')