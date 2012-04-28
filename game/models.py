from django.db import models
from django.contrib.auth.models import User

RANK_CHOICES = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10),
    (11, 11),
    (12, 12),
    (13, 13),
    (14, 14),
    (15, 15),
    (16, 16),
    (17, 17),
    (18, 18),
    (19, 19),
    (20, 20),
)

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
        if engine.compute_scores():
            self.ranked=True
        super(Game, self).save()

class Account(models.Model):
    handle = models.CharField(max_length=20)
    user = models.OneToOneField('auth.User')
    rank = models.PositiveIntegerField(blank=True, null=True, choices=RANK_CHOICES)
    rank_updated = models.DateTimeField(blank=True, null=True)
    score = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)

    def __unicode__(self):
        return self.handle

    @property
    def win_count(self):
        return Game.objects.filter(winner=self.user).count()

    @property
    def loss_count(self):
        return Game.objects.filter(loser=self.user).count()

    @property
    def games_played(self):
        return self.win_count + self.loss_count
