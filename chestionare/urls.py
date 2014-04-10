from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from chestionare.views import current_datetime

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'chestionare.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^current_datetime/$', current_datetime),
)
