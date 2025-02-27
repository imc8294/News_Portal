from django.urls import path, include  # type: ignore
from backoffice import cron_views, views, backoffice_display as bviews

urlpatterns = [
    
    path('', views.dashboard, name='dashboard'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('login', views.login, name="login"),
    path('submitlogin', views.submitLogin, name="Submit Login"),
    path('news_logout', views.logout, name="Session Logout"),

    path('news_cat', views.news_category, name="Category"),
    path('add_category',views.add_category, name="add_category"),
    path('save_category',views.save_category, name="save_category"),
    path('edit_category/<id>', views.edit_category, name="edit_category"),
    path('update_category', views.update_category, name="Update Category"),
    path('delete_category/<id>', views.delete_category, name="delete_category"),
    
    path('add_newsdata', views.add_newsdata, name="add_newsdata"),
    path('save_newsdata', views.save_newsdata, name="save_newsdata"),
    path('view_newsdata', views.view_newsdata, name="view_newsdata"),
    path('edit_newsdata/<id>', views.edit_newsdata, name="edit_newsdata"),
    path('update_newsdata', views.update_newsdata, name="update_newsdata"),
    path('delete_newsdata/<id>', views.delete_newsdata, name="delete_newsdata"),

    path('news_display', bviews.news_display, name="Display"),
    path('add_display',bviews.add_display, name="add_display"),
    path('save_display',bviews.save_display, name="save_display"),
    path('edit_display/<id>', bviews.edit_display, name="edit_display"),
    path('update_display', bviews.update_display, name="Update Display"),
    path('delete_display/<id>', bviews.delete_display, name="delete_display"),


    #added
    path('search_data', cron_views.search_data, name='search_data'),
    path('submitSearchData', cron_views.submitSearchData, name = 'submitSearchData'),
    path('updateCounting', cron_views.updateCounting, name = 'updateCounting'),
    path('view_data', cron_views.view_data, name='view_data'),
    path('expire_domain', cron_views.expire_domain, name = "expire-domain"),
    path('expire_domain_cron', cron_views.expireDoaminCron, name='expire-domain-cron'),
    path('sync_domain', cron_views.syncDomain, name= 'Sync-Domain'),
    path('send_mail_expire_domain', cron_views.sendMailExpireDomain, name="Send mail expire domain"),
    path('change_password', cron_views.change_password, name="change_password"),
    path('submitChangePassword', cron_views.submitChangePassword, name="submitChangePassword"),
    path('logout', cron_views.logout, name='logout'),
    path('test', cron_views.test, name='test')
    
    
]
