from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
	date = models.DateTimeField(auto_now_add=True)
	winner = models.ForeignKey('auth.User', related_name='winner')
	loser = models.ForeignKey('auth.User', related_name='loser')
	winning_score = models.PositiveIntegerField()
	losing_score = models.PositiveIntegerField()

	def __unicode__(self):
		return u"{} vs {} ({} to {})".format(self.loser, self.winner, self.losing_score, self.winning_score)


class Account(models.Model):
	handle = models.CharField(max_length=20)
	user = models.OneToOneField('auth.User')

	def __unicode__(self):
		return self.handle
