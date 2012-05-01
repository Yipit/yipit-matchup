from django.db import models
from django.contrib.auth.models import User

INITIAL_RATING = 1000

class Game(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    winner = models.ForeignKey('game.Account', related_name='winner')
    loser = models.ForeignKey('game.Account', related_name='loser')
    winning_score = models.DecimalField(max_digits=4, decimal_places=2)
    losing_score = models.DecimalField(max_digits=4, decimal_places=2)
    ranked = models.BooleanField(default=False)

    def __unicode__(self):
        return u"{} vs {} ({} to {})".format(self.loser, self.winner, self.losing_score, self.winning_score)

    def save(self):
        from rank.engine import RankEngine

        engine = RankEngine(self)
        if engine.update_scores():
            self.ranked=True
        super(Game, self).save()

class Account(models.Model):
    handle = models.CharField(unique=True, max_length=20)
    user = models.OneToOneField('auth.User')
    rank = models.PositiveIntegerField(blank=True, null=True)
    rank_updated = models.DateTimeField(blank=True, null=True)
    rating = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)

    def __unicode__(self):
        return self.handle

    def save(self):
        if not self.rating:
            self.rating = INITIAL_RATING
        super(Account, self).save()

    @property
    def win_count(self):
        return Game.objects.filter(winner=self).count()

    @property
    def loss_count(self):
        return Game.objects.filter(loser=self).count()

    @property
    def games_played(self):
        return self.win_count + self.loss_count
