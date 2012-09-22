from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from main.groupviews import GroupCreate
from main.groupviews import GroupDetails
from main.groupviews import GroupEdit
from main.groupviews import GroupListing

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'main.views.home', name='home'),
    url(r'^login/?$', 'main.views.login', name='login'),
    url(r'^groups/?$', GroupListing.as_view()),
    url(r'^group/?$', GroupCreate.as_view()),
    url(r'^group/(?P<group_name>\w+)/?$', GroupDetails.as_view()),
    url(r'^group/(?P<group_name>\w+)/edit/?$', GroupEdit.as_view()),
    # url(r'^ccvote/', include('ccvote.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
