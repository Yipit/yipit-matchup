from django.core.management import BaseCommand

from rank.engine import RankEngine


class Command(BaseCommand):
    def handle(self, *args, **options):
        engine = RankEngine()
        engine._update_ranking()