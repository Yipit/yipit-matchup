from django.core.management import BaseCommand
from game.models import Game, Account
from rank.engine import RankEngine


class Command(BaseCommand):
    def handle(self, *args, **options):
        Account.objects.all().update(rank=99, rating=1000)
        for game in Game.objects.all().order_by('date'):        
            engine = RankEngine(game=game)
            engine.update_scores()