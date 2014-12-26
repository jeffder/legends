from django.conf.urls import patterns, include, url
from django.contrib import admin

from main import urls as main_urls


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'legends.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    (r'^$',
        'main.views.index.index'),

    (r'^accounts/login',
        'main.views.auth.login'),

    (r'^accounts/logout',
        'main.views.auth.logout',),

    (r'^accounts/changePassword/done',
        'django.contrib.auth.views.password_change_done',
        {'template_name': 'accounts/change_password_done.html'}),

    (r'^accounts/change_password',
        'main.views.auth.change_password'),

    (r'^accounts/resetPassword/done',
        'django.contrib.auth.views.password_reset_done',
        {'template_name': 'accounts/reset_password_done.html'}),

    (r'^accounts/resetPassword',
        'django.contrib.auth.views.password_reset',
        {'template_name': 'accounts/reset_password.html',
         'email_template_name': 'accounts/reset_password_email.html'}),

    url(r'^legends/', include(main_urls)),
)
