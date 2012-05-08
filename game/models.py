from django.db import models
from django.contrib.auth.models import User

INITIAL_RATING = 1000

class Game(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    winner = models.ForeignKey('game.Account', related_name='winner')
    loser = models.ForeignKey('game.Account', related_name='loser')
    winning_score = models.PositiveIntegerField()
    losing_score = models.PositiveIntegerField()
    ranked = models.BooleanField(default=False)

    def __unicode__(self):
        return u"{} vs {} ({} to {})".format(self.loser, self.winner, self.losing_score, self.winning_score)

    @property
    def pretty_time(self):
        return self.date.strftime("%I:%M%p")

    @property
    def pretty_date(self):
        return self.date.strftime("%A, %B %d %I:%M%p")

    def save(self):
        from rank.engine import RankEngine
        super(Game, self).save()
        engine = RankEngine(self)
        if engine.update_scores():
            self.ranked=True
        

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
    def win_loss_ratio(self):
        return self.win_count / float(self.loss_count)

    @property
    def win_count(self):
        return Game.objects.filter(winner=self).count()

    @property
    def loss_count(self):
        return Game.objects.filter(loser=self).count()

    @property
    def games_played(self):
        return self.win_count + self.loss_count

    @property
    def pretty_rating(self):
        return int(self.rating)
