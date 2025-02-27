from django.db import models   # type: ignore

# Create your models here.
class AdminUser(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    password = models.CharField(max_length=200)
    status = models.IntegerField(default = 0)
    created_date = models.DateTimeField('date published')

class Category(models.Model):
    category_name = models.CharField(max_length=200)
    category_status = models.IntegerField(default = 0)
    category_order = models.IntegerField(default = 1)
    cat_created_date = models.DateTimeField('category created date')

class NewsData(models.Model):
    tittle = models.CharField(max_length=200)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    display_section = models.IntegerField(default=1)
    source = models.CharField(max_length=200)
    image = models.CharField(max_length=200, default="")
    content = models.TextField()
    html_content = models.TextField(default="")
    news_url = models.TextField(default="")
    created_date = models.DateTimeField('date published')
    news_status = models.IntegerField(default = 0)
    url_slug = models.CharField(max_length=255)
    show_type = models.IntegerField(default=1)

class DisplaySection(models.Model):
    name = models.CharField(max_length=200)
    display_status = models.IntegerField(default = 0)
    display_order = models.IntegerField(default = 1)
    display_created_date = models.DateTimeField('Display created date')

class DomainDetails(models.Model):
    domain_name = models.CharField(max_length=100, blank=True, null=True)
    registrar = models.CharField(max_length=150, blank=True, null=True)
    domain_updated_date = models.DateTimeField(blank=True, null=True)
    domain_created_date = models.DateTimeField(blank=True, null=True)
    domain_expire_date = models.DateTimeField(blank=True, null=True)
    organization_name = models.CharField(max_length=150, blank=True, null=True)
    address = models.CharField(max_length=150, blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField()

class ExpireDomain(models.Model):
    domain_name = models.CharField(max_length=100, blank=True, null=True)
    registrar = models.CharField(max_length=150, blank=True, null=True)
    domain_updated_date = models.DateTimeField(blank=True, null=True)
    domain_created_date = models.DateTimeField(blank=True, null=True)
    domain_expire_date = models.DateTimeField(blank=True, null=True)
    organization_name = models.CharField(max_length=150, blank=True, null=True)
    address = models.CharField(max_length=150, blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField()

class KeywordDetails(models.Model):
    keyword = models.CharField(max_length=100, blank=True, null=True)
    search_start_date = models.DateTimeField(blank=True, null=True)
    search_end_date = models.DateTimeField(blank=True, null=True)
    last_run_counting = models.IntegerField(default = 1)
    created_date = models.DateTimeField()