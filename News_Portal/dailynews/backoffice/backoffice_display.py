
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from backoffice.models import DisplaySection

def news_display(request):
    if 'admin-login' in request.session:
        display_data = DisplaySection.objects.all()
        data = {
            'admin_name': request.session['admin-data']['adminName'],
            'display_data' : display_data,
            'menu_name': 'display',
            'sub_menu': 'view_display'
        }
        return render(request, 'backoffice/display.html', data)
    else:
       return HttpResponseRedirect('/backoffice/login') 
    
def add_display(request):
    if 'admin-login' in request.session:
        data = {
            'admin_name': request.session['admin-data']['adminName'],
            'menu_name': 'display',
            'sub_menu': 'add_display'
        }
        return render(request, 'backoffice/add_display.html', data)
    else:
        return HttpResponseRedirect('/backoffice/login')
    
def save_display(request):
    update=''
    if request.method == "POST":
        name=request.POST.get('Name')
        display_status=request.POST.get('Status')
        display_order=request.POST.get('Order')
        display_created_date=request.POST.get('Date')
        values = DisplaySection(name=name, display_status=display_status, display_order=display_order, display_created_date=display_created_date)
        values.save()
        update='Data Inserted'
    return HttpResponseRedirect('/backoffice/news_display', {'update' : update})

def edit_display(request, id):
    if 'admin-login' in request.session:
        queryset = DisplaySection.objects.get(id = id)
        data = {
            'display': queryset,
            'menu_name': 'display',
            'sub_menu': 'view_display'
        }
        return render(request,'backoffice/add_display.html',data)
    else:
        return HttpResponseRedirect('/backoffice/login')

def update_display(request):
    if 'admin-login' in request.session:
        if request.method == "POST":
            display_id = request.POST.get('category_id')
            name=request.POST.get('Name')
            display_status=request.POST.get('Status')
            display_order=request.POST.get('Order')
            display_created_date=request.POST.get('Date')
            queryset = DisplaySection.objects.get(id = display_id)
            queryset.name=name
            queryset.display_status=display_status
            queryset.display_order=display_order
            queryset.display_created_date=display_created_date
            queryset.save()
        return HttpResponseRedirect('/backoffice/news_display')
    else:
        return HttpResponseRedirect('/backoffice/login')

def delete_display(request, id):
    if 'admin-login' in request.session:
        values = DisplaySection.objects.get(id = id)
        values.delete()
        return HttpResponseRedirect('/backoffice/news_display')
    else:
        return HttpResponseRedirect('/backoffice/login')
   