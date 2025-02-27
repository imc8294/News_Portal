import requests
import os

from backoffice.models import Category, NewsData

from newspaper import Article

def download_image_from_url(img_url): 
    response = requests.get(img_url)

    if response.status_code != 200:
        return './statics/custom_image/fd3dedba1e4c218d763a3d77.jpg'

    filename = f'./statics/custom_image/{generate_random_string()}.jpg' # You can name the file as you want
    with open(filename, 'wb') as file:
        file.write(response.content)
    return filename

def generate_random_string():
    random_bytes = os.urandom(12)
    hex_string = random_bytes.hex()
    return hex_string

def store_news_data_cron(news_data): 
    category_data = Category.objects.get(
        id = 4
    )

    url = news_data['link']
    editted_urls = url.split('&')


    link = editted_urls[0]
    article = Article(link)
    article.download()
    article.parse()

    values_for_news_slug = news_data['title']
    updated_value =  values_for_news_slug.replace(' ','_')
    news_title = news_data['title']
    news_source = news_data['media']
    news_content = article.text
    news_html = article.html
    publish_date = news_data['datetime']
    publish_date.strftime('%b %d,%Y')
    news_status = 1
    news_urls = link
    news_slug = updated_value
    img_file = download_image_from_url(article.top_image)
    values = NewsData(
        html_content=news_html,
        tittle=news_title, 
        category=category_data, 
        source=news_source, 
        content=news_content, 
        created_date=publish_date, 
        news_status=news_status, 
        news_url=news_urls, 
        url_slug=news_slug,
        image = img_file
    )
    values.save()