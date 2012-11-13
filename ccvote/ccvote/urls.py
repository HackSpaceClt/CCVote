from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from main.groupviews import GroupCreate
from main.groupviews import GroupDetails
from main.groupviews import GroupEdit
from main.groupviews import GroupListing
from main.userviews import UserCreate
from main.userviews import UserDeleteConfirm
from main.userviews import UserDetails
from main.userviews import UserEdit
from main.userviews import UserListing
from main.motionviews import MotionCreate
from main.motionviews import MotionDetails
from main.motionviews import MotionEdit
from main.motionviews import MotionListing
from main.loginview import UserLogin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'main.views.home', name='home'),
    url(r'^overlay$', 'main.views.videoOverlay', name='videoOverlay'),

    # Other examples for guidance:
    # url(r'^articles/(\d{4})/(\d{2})/(\d+)/$', 'news.views.article_detail')
    ## calls news.views.article_detail(request, '2003', '03', '03')
    ## named patterns:
    # url(r'^articles/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', 'news.views.article_detail')
    ## calls news.views.article_detail(request, year='2003', month='03', day='03')

    # Login/Logout
    url(r'^login/?$', UserLogin.as_view(), name='login'),
    url(r'^logout/?$', 'main.views.logout', name='logout'),

    # Groups
    url(r'^groups/?$', GroupListing.as_view()),
    url(r'^group/?$', GroupCreate.as_view()),
    url(r'^group/(?P<group_name>\w+)/?$', GroupDetails.as_view()),
    url(r'^group/(?P<group_name>\w+)/edit/?$', GroupEdit.as_view()),
    # Users
    url(r'^users/?$', UserListing.as_view()),
    url(r'^user/?$', UserCreate.as_view()),
    url(r'^user/(?P<user_name>\w+)/?$', UserDetails.as_view()),
    url(r'^user/(?P<user_name>\w+)/edit?$', UserEdit.as_view()),
    url(r'^user/(?P<user_name>\w+)/delete?$', UserDeleteConfirm.as_view()),
    # Motions
    url(r'^motions/?$', MotionListing.as_view()),
    url(r'^motion/?$', MotionCreate.as_view()),
    url(r'^motion/(?P<motion_id>\w+)/?$', MotionDetails.as_view()),
    url(r'^motion/(?P<motion_id>\w+)/edit/?$', MotionEdit.as_view()),
    # url(r'^ccvote/', include('ccvote.foo.urls')),

    # Voting client stuff
    url(r'^voteclient/minimal/?$', 'main.views.VoteClientMinimal', name="VoteClientMinimal"),
    url(r'^voteclient/ajax/?$', 'main.views.VoteClientAjax', name="VoteClientAjax"),
    url(r'^voteclient/longpoll/?$', 'main.views.VoteClientAjaxLongPoll', name="VoteClientAjaxLongPoll"),
    
    # Clerk interface
    url(r'^clerk/?$', 'main.views.ClerkInterface', name="ClerkInterface"),
    url(r'^clerk/ajax/motionpull/(?P<motion_id>\w+)/?$', 'main.views.ClerkAjaxMotionPull', name="ClerkAjaxMotionPull"),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()

# vim: set sts=4 sw=4 expandtab:
