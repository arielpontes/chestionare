from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from questionnaires import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'chestionare.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^clear-test$', 'questionnaires.views.clear_test', name='clear_test'),
    url(r'^questionnaires/(\d+)/$', 'questionnaires.views.solve', name='solve'),
    
    url(r'^admin/', include(admin.site.urls)),
)
