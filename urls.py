from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
import settings
from django.conf.urls.static import static
from game.views import AddGameView, DashboardView
from analytics.views import AnalyticsView
#from signup.views import LandingView

admin.autodiscover()

#urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', LandingView.as_view(), name='login'),
    # url(r'^logout/$', 'signup.views.logout', name='logout'),
    url(r'^$', DashboardView.as_view(), name='dashboard'),
    url(r'^add_game/$', AddGameView.as_view(), name='add_game'),
    # url(r'^social/', include('social.foo.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^analytics/$', AnalyticsView.as_view(), name='analytics'),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)