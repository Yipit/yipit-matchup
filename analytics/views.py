import datetime

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout

from django.views.generic.base import TemplateView

from analytics.forms import GameHistoryForm
from game.models import Game, Account

class AnalyticsView(TemplateView):
    template_name = 'analytics/basic.html'
    form_class = GameHistoryForm
    games = None
    message = ""
    alert_class = ""

    def get(self, request, *args, **kwargs):
        self.form = self.form_class()
        return self.render_to_response(self.compute_context(request, *args, **kwargs))

    def post(self, request, *args, **kwargs):
        self.form = self.form_class(request.POST)
        if self.form.is_valid():
            self.games = self.form.process().order_by('-date')
        else:
            self.message = "Oops! There were some issues processing your submission!"
            self.alert_class = "alert-error"
        return self.render_to_response(self.compute_context(request, *args, **kwargs))

    def compute_context(self, request, *args, **kwargs):
        context = {}
        context['form'] = self.form
        context['message'] = self.message
        context['alert_class'] = self.alert_class
        context['games'] = self.games
        return context