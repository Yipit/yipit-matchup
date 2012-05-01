from django.db import models

class RankLog(models.Model):
	player = models.ForeignKey('game.Account')
	rank = models.PositiveIntegerField()
	rating = models.DecimalField(max_digits=7, decimal_places=2)
	date_created = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return u"{}, Rank:{} Score:{} ({})".format(self.player, self.rank, self.rating, self.date_created)
