from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout

from django.views.generic.base import TemplateView

from game.forms import GameForm
from game.models import Game, Account


class AddGameView(TemplateView):
	template_name = 'game/add_game.html'
	form_class = GameForm
	message = ""
	alert_class = ""

	def get(self, request, *args, **kwargs):
		self.form = self.form_class()
		return self.render_to_response(self.compute_context(request, *args, **kwargs))

	def post(self, request, *args, **kwargs):
		self.form = self.form_class(request.POST)
		if self.form.is_valid():
			self.form.process()
			self.form = self.form_class()
			self.message = "Game record added!"
			self.alert_class = "alert-success"
		else:
			self.message = "Oops! There were some issues processing your submission!"
			self.alert_class = "alert-error"
		return self.render_to_response(self.compute_context(request, *args, **kwargs))

	def compute_context(self, request, *args, **kwargs):
		context = {}
		context['form'] = self.form
		context['message'] = self.message
		context['alert_class'] = self.alert_class
		return context


class DashboardView(TemplateView):
    template_name = 'account/dashboard.html'

    def get(self, request, *args, **kwargs):
        self.games = Game.objects.all()
        wins_list = [(account, account.win_count) for account in Account.objects.all()]
        winner_list = sorted(wins_list, key=lambda x: wins_list[1])
        self.winner_list = list(map(lambda x: x[0], winner_list))
        return self.render_to_response(self.compute_context(request, *args, **kwargs))

    def compute_context(self, request, *args, **kwargs):
        context = {}
        context['winner_list'] = self.winner_list
        context['games'] = self.games
        return context