import datetime
import inspect

from django.db.models import Q
from django.core.management import BaseCommand
from game.models import Game, Account
from rank.engine import RankEngine
from rank.models import RankLog



class Command(BaseCommand):

    def handle(self, *args, **options):
        last_week = datetime.datetime.today() - datetime.timedelta(days=7)
        self.games = Game.objects.filter(date__gt=last_week).order_by('-date')
        self.accounts = Account.objects.all()
        results = {}
        stats =  inspect.getmembers(Command, lambda x: inspect.ismethod(x) and x.__name__.startswith('get'))
        for func_name, func in stats:
            results[func_name] = func(self)
        print results

    def get_longest_streak(self):
        streak_info = (None, 0)
        for account in self.accounts:
            games = self.games.filter(Q(winner=account) | Q(loser=account))
            results = ['1' if game.winner == account else '0' for game in games]
            broken_results = "".join(results).split('0')
            streak = max([len(streak) for streak in broken_results])
            if streak > streak_info[1]:
                streak_info = (account, streak)
        return streak_info

    def get_best_ratio(self):
        ratio_info = (None, 0)
        for account in self.accounts:
            try:
                ratio = self.games.filter(winner=account).count() / float(self.games.filter(loser=account).count())
            except ZeroDivisionError:
                return account
            else:
                if ratio > ratio_info[1]:
                    ratio_info = (account, ratio)
        return ratio_info

    def get_predator_and_fearless(self):
        predator_info = (None, 0)
        fearless_info = (None, 0)
        num_accounts = self.accounts.count()
        for account in self.accounts:
            lower_ranked = 0.0
            higher_ranked = 0.0
            games = self.games.filter(winner=account)
            if not games:
                continue
            for game in games:
                if not game.upset:
                    lower_ranked += 1
                else:
                    higher_ranked += 1
            try:
                ratio = (lower_ranked / higher_ranked) * account.rank / num_accounts
            except ZeroDivisionError:
                predator_info = (account, 'undef')
                continue
            else:
                if ratio > predator_info[1]:
                    predator_info = (account, ratio)
                if - ratio < fearless_info:
                    fearless_info = (account, ratio)
        return (predator_info, fearless_info)

    def get_biggest_beat_down(self):
        return max(self.games, key=lambda game: game.winning_score - game.losing_score).id
