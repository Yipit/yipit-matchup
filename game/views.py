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
        opponent = request.GET.get('opponent')
        if opponent:
            try:
                winner = Account.objects.get(handle=opponent)
            except Account.DoesNotExist:
                pass
            else:
                self.form = self.form_class({'player_1': winner, 'score_1': 21})
        else:
            self.form = self.form_class()
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

def games_today(request):
    template = 'game/games_today.html'
    today = datetime.datetime.today()
    context = {}
    context['games'] = Game.objects.order_by('-date')
    return render(request, template, context)


class DashboardView(TemplateView):
    template_name = 'account/dashboard.html'


    def get(self, request, *args, **kwargs):
        three_days_ago = datetime.datetime.now() - datetime.timedelta(days=3)
        self.games = Game.objects.filter(date__lt=three_days_ago).order_by('-date')
        all_accounts = Account.objects.all()

        rank_list = [(account, account.rank) for account in all_accounts]
        sorted_rank_list = sorted(rank_list, key=lambda x: x[1])
        self.ranked_players = list(map(lambda x: x[0], sorted_rank_list))
        self.games_today = Game.objects.all().filter(date__gt=datetime.date.today()).count()
        self.players_on_fire = [player for player in all_accounts if player.on_fire]
        
        return self.render_to_response(self.compute_context(request, *args, **kwargs))

    def _group_games_by_day(self):
        three_days_ago = datetime.datetime.now() - datetime.timedelta(days=3)
        games = Game.objects.filter(date__gt=three_days_ago).order_by('date')
        self.first_date = games[0].date
        start_date = datetime.datetime(year=self.first_date.year, month=self.first_date.month, day=self.first_date.day)
        window = datetime.timedelta(days=1)
        games_by_day = []
        now = datetime.datetime.now()

        while start_date < datetime.datetime(year=now.year, month=now.month, day=now.day) + window:
            qs = Game.objects.filter(date__gte=start_date).filter(date__lt=start_date+window)
            games_by_day.append(qs.count())
            start_date += window
        return games_by_day


    def compute_context(self, request, *args, **kwargs):
        context = {}
        context['games'] = self.games
        context['ranked_players'] = self.ranked_players
        context['games_today'] = self.games_today
        context['games_by_day'] = self._group_games_by_day()
        context['start'] = self.first_date
        context['on_fire'] = self.players_on_fire

        return context



