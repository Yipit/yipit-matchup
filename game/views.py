import datetime

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
        self.opponent = Account.objects.get(handle=request.GET.get('opponent'))
        self.form = self.form_class({'player_2': self.opponent, 'score_1': 21})
        return self.render_to_response(self.compute_context(request, *args, **kwargs))

    def post(self, request, *args, **kwargs):
        self.form = self.form_class(request.POST)
        if self.form.is_valid():
            self.form.process()
            self.form = self.form_class()
            self.message = "Game record added!"
            self.alert_class = "alert-success"
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            self.message = "Oops! There were some issues processing your submission!"
            self.alert_class = "alert-error"
        return self.render_to_response(self.compute_context(request, *args, **kwargs))

    def compute_context(self, request, *args, **kwargs):
        context = {}
        context['form'] = self.form
        context['message'] = self.message
        context['alert_class'] = self.alert_class
        context['add_game'] = True
        return context


class DashboardView(TemplateView):
    template_name = 'account/dashboard.html'


    def get(self, request, *args, **kwargs):

        self.games = Game.objects.order_by('-date')
        all_accounts = Account.objects.all()

        rank_list = [(account, account.rank) for account in all_accounts]
        sorted_rank_list = sorted(rank_list, key=lambda x: x[1])
        self.ranked_players = list(map(lambda x: x[0], sorted_rank_list))
        self.games_today = Game.objects.all().filter(date__gt=datetime.date.today()).count()
        
        return self.render_to_response(self.compute_context(request, *args, **kwargs))

    def compute_context(self, request, *args, **kwargs):
        context = {}
        context['games'] = self.games
        context['ranked_players'] = self.ranked_players
        context['games_today'] = self.games_today

        return context



