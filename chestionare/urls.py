from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'chestionare.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'questionnaires.views.index', name='index'),
    url(r'^clear-test$', 'questionnaires.views.clear_test', name='clear_test'),
    url(r'^questionnaires/(\d+)/$', 'questionnaires.views.show', name='show'),
    #url(r'^questionnaires/(\d+)/page(\d+)$', 'questionnaires.views.show', name='show'),
    
    url(r'^questionnaires/(\d+)/results$', 'questionnaires.views.results', name='results'),
    
    url(r'^admin/', include(admin.site.urls)),
)
