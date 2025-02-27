
from django.shortcuts import render, HttpResponse, HttpResponseRedirect # type: ignore

from backoffice.models import NewsData,Category

# Create your views here.


def home_page(request):

    first_section_data = NewsData.objects.filter(
        news_status = 1,
        display_section=1
    )

    second_section_data = NewsData.objects.filter(
        news_status =1,
        display_section=2
    )

    third_section_data = NewsData.objects.filter(
        news_status =1,
        display_section=4
    )

    data_for_latest_news = NewsData.objects.filter(
        news_status = 1,
        display_section = 5
    )

    latest_news_right_side = NewsData.objects.filter(
        news_status = 1,
        display_section = 6
    )

    latest_news_small_box_left = NewsData.objects.filter(
        news_status = 1,
        display_section = 7 
    )

    latest_news_small_box_right = NewsData.objects.filter(
        news_status = 1,
        display_section = 8 
    )

    trending_news = NewsData.objects.filter(
        news_status = 1,
        display_section = 9
    )
    bottom_news = NewsData.objects.filter(
        news_status = 1,
        display_section = 10
    )

    bottom_left_news = NewsData.objects.filter(
        news_status = 1,
        display_section = 11
    )

    bottom_right_news = NewsData.objects.filter(
        news_status = 1,
        display_section = 12
    )

    data = {
        'section_1' : first_section_data,
        'section_2' : second_section_data,
        'section_3' : third_section_data,
        'section_4' : data_for_latest_news,
        'section_5' : latest_news_right_side,
        'section_6' : latest_news_small_box_left,
        'section_7' : latest_news_small_box_right,
        'section_8' : bottom_news,
        'section_9' : trending_news,
        'section_10' : bottom_left_news,
        'section_11' : bottom_right_news
        
    }
    return render(request, 'frontend/dashboard.html', data)

def category(request):

    trending_news = NewsData.objects.filter(
        news_status = 1,
        display_section = 9
    )

    politice_section = NewsData.objects.filter(
        news_status = 1,
        display_section = 13
    )

    politice_section_right = NewsData.objects.filter(
        news_status = 1,
        display_section = 14
    )

    sports_section = NewsData.objects.filter(
        news_status = 1,
        display_section = 15
    )

    soprts_section_right = NewsData.objects.filter(
        news_status = 1,
        display_section = 16
    )

    data = {
        'section_3' : trending_news,
        'section_1' : politice_section,
        'section_2' : politice_section_right,
        'section_4' : sports_section,
        'section_5' : soprts_section_right


    }
    

    return render(request, 'frontend/category.html', data)

def single(request):

    trending_news = NewsData.objects.filter(
        news_status = 1,
        display_section = 9
    )

    single_news  = NewsData.objects.filter(
        news_status = 1,
        display_section = 17
    )

    data= {
        'section_9' : trending_news,
        'section_1' : single_news
    }

    return render(request, 'frontend/single.html', data)


def contact(request):
    return render(request, 'frontend/contact.html')