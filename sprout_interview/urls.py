from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sprout_interview.views.home', name='home'),
    # url(r'^sprout_interview/', include('sprout_interview.foo.urls')),

    url(r'^tweets/', include('tweets.urls', namespace="tweets")),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/', admin.site.urls),

)
