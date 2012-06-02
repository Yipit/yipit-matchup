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
    url(r'^game_add/$', 'game.views.process_game', name='game_add'),
    url(r'^analytics/$', AnalyticsView.as_view(), name='analytics'),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)