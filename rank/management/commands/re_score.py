from django.core.management import BaseCommand
from game.models import Game, Account
from rank.engine import RankEngine
from rank.models import RankLog


class Command(BaseCommand):
    def handle(self, *args, **options):
        RankLog.objects.all().delete()
        Account.objects.all().update(rank=None, rating=1000)
        for game in Game.objects.all().order_by('date'):
            print game        
            engine = RankEngine(game=game)
            engine.update_scores()