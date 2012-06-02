import datetime

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

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


def process_game(request):
    if request.POST:
        winning_score = request.POST.get('score_1')
        losing_score = request.POST.get('score_2')
        if not losing_score:
            losing_score = 0
            winning_score = 0
        if losing_score and not winning_score:
            winning_score = 21
        winner_id = request.POST.get('player_1')[1:]
        loser_id = request.POST.get('player_2')[1:]
        postdict = {u'score_1': unicode(winning_score), u'player_2': loser_id, u'score_2': unicode(losing_score), u'player_1': winner_id}
        try:
            form = GameForm(postdict)
            if form.is_valid():
                form.process()
            else:
                print "hello"
        except:
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            return HttpResponseRedirect(reverse('dashboard'))
    else:
        return HttpResponseRedirect(reverse('dashboard'))


class DashboardView(TemplateView):
    template_name = 'account/dashboard.html'

    def get_recent_games(self):
        three_days_ago = datetime.datetime.now() - datetime.timedelta(days=3)
        return Game.objects.filter(date__gt=three_days_ago).order_by('-date')

    def get_ranked_players(self):
        ranked_accounts = Account.objects.filter(ranked=True).order_by('handle')
        rank_list = [(account, account.rank) for account in ranked_accounts]
        sorted_rank_list = sorted(rank_list, key=lambda x: x[1])
        return list(map(lambda x: x[0], sorted_rank_list))

    def prepare_add_game_form(self):
        pass

    def get_active_players(self):
        return [account for account in Account.objects.all() if account.user.is_active]

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.compute_context(request, *args, **kwargs))

    def compute_context(self, request, *args, **kwargs):
        context = {}
        context['ranked_players'] = self.get_ranked_players()
        context['accounts'] = self.get_active_players()
        context['games'] = self.get_recent_games()
        return context
