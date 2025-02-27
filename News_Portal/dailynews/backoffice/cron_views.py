from django.shortcuts import render, HttpResponse, HttpResponseRedirect

from backoffice.utils.utility import store_news_data_cron # type: ignore
from .models import  DomainDetails, KeywordDetails, ExpireDomain
from hashlib import md5
from django.template.loader import render_to_string  # type: ignore
from datetime import datetime, date, timedelta
# import datetime
from GoogleNews import GoogleNews  # type: ignore
import whois  # type: ignore
from django.core.mail import EmailMessage  # type: ignore
from newspaper import Article, fulltext  # type: ignore


def dashboard(request):
    if 'admin-login' in request.session:
        data = {'admin_name': request.session['admin-data']['adminName']}
        return render(request, 'cron_html/dashboard.html', data)
    else:
        return HttpResponseRedirect('/cron_html/login')

def search_data(request):
    if 'admin-login' in request.session:
        keyword_data = KeywordDetails.objects.all().order_by('-id')
        data = {'keyword_data': keyword_data, 'admin_name': request.session['admin-data']['adminName']}
        return render(request, 'cron_html/search_data.html', data)
    else:
        return HttpResponseRedirect('/cron_html/login')

def submitSearchData(request):
    if request.method=="POST":
        start_date = request.POST['start_date']
        last_date  = request.POST['last_date']
        keyword = request.POST['keyword']
        if start_date and last_date and keyword:
            startDateObj = datetime.strptime(start_date, '%Y-%m-%d')
            lastDateObj = datetime.strptime(last_date, '%Y-%m-%d')
            search_data = KeywordDetails.objects.filter(
                keyword = keyword,
                search_start_date = startDateObj,
                search_end_date = lastDateObj
            )
            start_cron = 1
            if search_data:
                for dData in search_data:
                    start_cron = dData.last_run_counting
            else:
                saveKeyWord = KeywordDetails(
                    keyword = keyword,
                    search_start_date = startDateObj,
                    search_end_date = lastDateObj,
                    created_date = datetime.now()
                )
                saveKeyWord.save()
            sStartDate = startDateObj.strftime('%m/%d/%Y')
            eLastDate = lastDateObj.strftime('%m/%d/%Y')
            googleNews = GoogleNews(start=sStartDate, end = eLastDate)
            googleNews.search(keyword)
            for i in range(start_cron, 4999):
                result = googleNews.page_at(i)
                if result:
                    for data_set in result:
                        url = data_set['link']
                        domainUrl = url.split('//')[1]
                        domain = domainUrl.split('/')[0]
                        domain_data = DomainDetails.objects.filter(
                            domain_name = domain
                        )
                        print(domain_data)
                        if not domain_data:
                            try:
                                who_is = whois.whois(domain)
                                if who_is:
                                    registrar = who_is.registrar if 'registrar' in who_is else ''
                                    updated_date = None
                                    if 'updated_date' in who_is and who_is.updated_date:
                                        if isinstance(who_is.updated_date, list):
                                            if isinstance(who_is.updated_date[0], (date, datetime)):
                                                updated_date = who_is.updated_date[0]
                                            else:
                                                updated_date = datetime.fromisoformat(who_is.updated_date[0])
                                        elif isinstance(who_is.updated_date, (date, datetime)):
                                            updated_date = who_is.updated_date

                                    creation_date = None
                                    if 'creation_date' in who_is and who_is.creation_date:
                                        if isinstance(who_is.creation_date, list):
                                            if isinstance(who_is.creation_date[0], (date, datetime)):
                                                creation_date = who_is.creation_date[0]
                                            else:
                                                creation_date = datetime.fromisoformat(who_is.creation_date[0])      
                                        elif isinstance(who_is.creation_date, (date, datetime)):
                                            creation_date = who_is.creation_date
                                    
                                    expiration_date = None
                                    if 'expiration_date' in who_is and who_is.expiration_date:
                                        if isinstance(who_is.expiration_date, list):
                                            if isinstance(who_is.expiration_date[0], (date, datetime)):
                                                expiration_date = who_is.expiration_date[0]
                                            else:
                                                expiration_date = datetime.fromisoformat(who_is.expiration_date[0])
                                        elif isinstance(who_is.expiration_date, (date, datetime)):
                                            expiration_date = who_is.expiration_date

                                    org = who_is.org if 'org' in who_is else ''
                                    address = who_is.address if 'address' in who_is else ''
                                    city = who_is.city if 'city' in who_is else ''
                                    state = who_is.state if 'state' in who_is else ''
                                    zipcode = who_is.zipcode if 'zipcode' in who_is else ''
                                    country = who_is.country if 'country' in who_is else ''
                                    
                                    saveData = DomainDetails(
                                        domain_name = domain,
                                        registrar = registrar,
                                        domain_updated_date= updated_date,
                                        domain_created_date = creation_date,
                                        domain_expire_date=expiration_date,
                                        organization_name= org,
                                        address= address,
                                        city=city,
                                        state=state,
                                        zipcode=zipcode,
                                        country= country,
                                        created_date = datetime.now()
                                    )
                                    saveData.save()
                                    store_news_data_cron(data_set)
                                    
                            except Exception:
                                saveData = DomainDetails(
                                        domain_name = domain,
                                        created_date = datetime.now()
                                    )
                else:
                    break  
            KeywordDetails.objects.filter(keyword=keyword).update(last_run_counting=i)    
        else:
            return HttpResponseRedirect('/backoffice/search_data')
    return HttpResponseRedirect('/backoffice/search_data')


def view_data(request):
    if 'admin-login' in request.session:
        domain_data = DomainDetails.objects.all().order_by('-id')
        data = {'domain_data': domain_data, 'admin_name': request.session['admin-data']['adminName']}
        return render(request, 'cron_html/view_data.html', data)
    else:
        return HttpResponseRedirect('/cron_html/login')

def expire_domain(request):
    if 'admin-login' in request.session:
        domain_data = ExpireDomain.objects.all()
        data = {'domain_data': domain_data, 'admin_name': request.session['admin-data']['adminName']}
        return render(request, 'cron_html/expire_domain.html', data)
    else:
        return HttpResponseRedirect('/cron_html/login')

def updateCounting(request):
    if 'admin-login' in request.session:
        if request.method=="POST":
            id=request.POST['id']
            last_run_counting = request.POST['last_run_counting']
            KeywordDetails.objects.filter(id=id).update(last_run_counting=last_run_counting)
    else:
      return HttpResponseRedirect('/cron_html/login')  
    return HttpResponseRedirect('/cron_html/search_data')

def expireDoaminCron(request):
    today = date.today()
    today = today.strftime('%Y-%m-%d')
    expireData = DomainDetails.objects.raw('SELECT * FROM `urlportal_domaindetails` WHERE `domain_expire_date` < '+ '"'+today+'"')
    for value in expireData:
        domain_data = ExpireDomain.objects.filter(
            domain_name = value.domain_name
        )
        if not domain_data:
            saveData = ExpireDomain(
                domain_name = value.domain_name,
                registrar = value.registrar,
                domain_updated_date= value.domain_updated_date,
                domain_created_date = value.domain_created_date,
                domain_expire_date=value.domain_expire_date,
                organization_name= value.organization_name,
                address= value.address,
                city=value.city,
                state=value.state,
                zipcode=value.zipcode,
                country= value.country,
                created_date = datetime.now()
            )
            saveData.save()
            DomainDetails.objects.filter(id=value.id).delete()
    return HttpResponse('/cron_html/success')

def syncDomain(request):
    """
    function for check expire date of domain and sync in to domain details table
    """
    domain_data = ExpireDomain.objects.all().order_by('-id')
    if domain_data:
        for value in domain_data:
            who_is = whois.whois(value.domain_name)
            if who_is:
                expiration_date = ''
                if 'expiration_date' in who_is and who_is.expiration_date:
                    if isinstance(who_is.expiration_date, list):
                        if isinstance(who_is.expiration_date[0], (date, datetime)):
                            expiration_date = who_is.expiration_date[0]
                        else:
                            expiration_date = datetime.fromisoformat(who_is.expiration_date[0])
                    elif isinstance(who_is.expiration_date, (date, datetime)):
                        expiration_date = who_is.expiration_date
                if expiration_date:
                    exp_date = expiration_date.strftime('%Y-%m-%d')
                    exp_db_date = value.domain_expire_date.strftime('%Y-%m-%d')
                    if exp_date > exp_db_date:
                        registrar = who_is.registrar if 'registrar' in who_is else ''
                        updated_date = ''
                        if 'updated_date' in who_is and who_is.updated_date:
                            if isinstance(who_is.updated_date, list):
                                if isinstance(who_is.updated_date[0], (date, datetime)):
                                    updated_date = who_is.updated_date[0]
                                else:
                                    updated_date = datetime.fromisoformat(who_is.updated_date[0])
                            elif isinstance(who_is.updated_date, (date, datetime)):
                                updated_date = who_is.updated_date

                        creation_date = ''
                        if 'creation_date' in who_is and who_is.creation_date:
                            if isinstance(who_is.creation_date, list):
                                if isinstance(who_is.creation_date[0], (date, datetime)):
                                    creation_date = who_is.creation_date[0]
                                else:
                                    creation_date = datetime.fromisoformat(who_is.creation_date[0])      
                            elif isinstance(who_is.creation_date, (date, datetime)):
                                creation_date = who_is.creation_date
                        org = who_is.org if 'org' in who_is else ''
                        address = who_is.address if 'address' in who_is else ''
                        city = who_is.city if 'city' in who_is else ''
                        state = who_is.state if 'state' in who_is else ''
                        zipcode = who_is.zipcode if 'zipcode' in who_is else ''
                        country = who_is.country if 'country' in who_is else ''
                        saveData = DomainDetails(
                            domain_name = value.domain_name,
                            registrar = registrar,
                            domain_updated_date= updated_date,
                            domain_created_date = creation_date,
                            domain_expire_date=expiration_date,
                            organization_name= org,
                            address= address,
                            city=city,
                            state=state,
                            zipcode=zipcode,
                            country= country,
                            created_date = datetime.now()
                        )
                        saveData.save()
                        ExpireDomain.objects.filter(id=value.id).delete()
    return HttpResponse('/cron_html/success')

def sendMailExpireDomain(request):
    today = date.today()
    con_date = today + timedelta(6)
    con_date = con_date.strftime('%Y-%m-%d')
    expireData = DomainDetails.objects.raw('SELECT * FROM `urlportal_domaindetails` WHERE `domain_expire_date` < '+ '"'+con_date+'"')
    if expireData:
        data = {'domain_data': expireData}
        html_content = render_to_string('expire-template-email.html', data)
        email_msg = EmailMessage(
            'Expire Domain Email', 
            html_content, 
            'Admin<chandramauli.sterco@gmail.com>',
            ['cchaubey55@gmail.com'],
            reply_to=['Admin<chandramauli.sterco@gmail.com>']
        )
        email_msg.content_subtype = 'html'
        email_msg.send(fail_silently=False)
    return HttpResponse(f"Email sent to  members")

def change_password(request):
    if 'admin-login' in request.session:
        data = {'admin_name': request.session['admin-data']['adminName']}
        return render(request, 'change_password.html', data)
    else:
        return HttpResponseRedirect('/cron_html/login')
    
def submitChangePassword(request):
    if 'admin-login' in request.session:
        password = request.POST['password']
        encode_password = md5(password.encode())
        AdminUser.objects.filter(id=request.session['admin-data']['adminId']).update(password=encode_password.hexdigest())
        data = {'msg':'Password Updated successfully'}
        return render(request, 'change_password.html',data)
    else:
        return HttpResponseRedirect('/cron_html/login')

def logout(request):
    try:
        del request.session['admin-login']
        del request.session['admin-data']
    except:
        return HttpResponseRedirect('/cron_html/login')
    return HttpResponseRedirect('/cron_html/login')

def test(request):
    # googlenews=GoogleNews(start='01/01/2025',end='08/01/2025')
    # googlenews.search('Coronavirus')
    # result = googlenews.page_at(1)
    # for data_set in result:
    #     print(data_set.get('link'))
    # url = 'https://www.manilatimes.net/2025/01/08/tmt-newswire/globenewswire/cocrystal-pharma-reports-phase-1-results-with-oral-broad-acting-antiviral-drug-cdi-988-for-prophylaxis-and-treatment-of-norovirus-coronaviruses-and-other-viral-infections/2033287'
    # article = Article(url)
    # article.download()
    # article.parse()
    # print(article.authors)
    # print(article.top_image)
    # print(article.movies)

   

    # data='data:image/gif;base64,R0lGODlhAQABAIAAAP///////yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=='
    # img_data=data.split('base64,')[1].encode('utf8')
    # with open("imageToSave.gif", "wb") as fh:
    #     fh.write(base64.decodebytes(img_data))

    # print("Image has been saved as output_image.gif")
    data = {'title': 'WHO expert explains one key difference between hMPV surge and coronavirus pandemic', 'media': 'Daily Express', 'date': '2 hours ago', 'datetime': datetime.datetime(2025, 1, 8, 22, 49, 44, 629927), 'desc': 'The World Health Organisation (WHO) has issued advice following a surge in hMPV cases in China, with the disease also on the rise in the UK.', 'link': 'https://www.express.co.uk/news/world/1997891/who-expert-hmpv-coronavirus-difference&ved=2ahUKEwj4y7306-aKAxUvSWwGHVC9FqoQxfQBegQIBBAC&usg=AOvVaw31aWQh2PPuLgNt2XCJwb29', 'img': 'data:image/gif;base64,R0lGODlhAQABAIAAAP///////yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=='}
    store_news_data_cron(data)
    #download_image_from_url(article.top_image)
    return HttpResponse('done')






