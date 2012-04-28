from django.db import models

class Game(models.Model):
	date = models.DateTimeField(auto_now_add=True)
	player_1 = models.ForeignKey('auth.User', related_name='player_1')
	player_2 = models.ForeignKey('auth.User', related_name='player_2')
	score_1 = models.PositiveIntegerField()
	score_2 = models.PositiveIntegerField()

	def __unicode__(self):
		return u"%s vs %s (%s to %s)" % (self.player_1, self.player_2, self.score_1, self.score_2)
