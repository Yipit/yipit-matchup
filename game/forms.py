from django import forms
from game.models import Game, Account
from django.contrib.auth.models import User

class GameForm(forms.Form):
	player_1 = forms.CharField(label="Player 1's handle")
	player_2 = forms.CharField(label="Player 2's handle")
	score_1 = forms.IntegerField(label="Player 1's score")
	score_2 = forms.IntegerField(label="Player 2's score")

	def clean_player(self, player):
		try:
			return User.objects.get(account__handle=player)
		except User.DoesNotExist:
			return False

	def clean_player_1(self):
		player_1 = self.cleaned_data['player_1']
		if self.clean_player(player_1):
			return player_1
		else:
			raise forms.ValidationError("Could not find user %s" % player_1)

	def clean_player_2(self):
		player_2 = self.cleaned_data['player_2']
		if self.clean_player(player_2):
			return player_2
		else:
			raise forms.ValidationError("Could not find user %s" % player_2)

	def clean(self):
		try:
			if self.cleaned_data['player_1'] == self.cleaned_data['player_2']:
				raise forms.ValidationError("Player_1 and Player_2 cannot be the same!")
			return self.cleaned_data
		except KeyError:
			pass

	def process(self):
		account_1 = Account.objects.get(handle=self.cleaned_data['player_1'])
		account_2 = User.objects.get(handle=self.cleaned_data['player_2'])
		score_1 = self.cleaned_data['score_1']
		score_2 = self.cleaned_data['score_2']

		if score_1 > score_2:
			new_game = Game(
				winner=account_1,
				loser=account_2,
				winning_score=score_1,
				losing_score=score_2
			)
		else:
			new_game = Game(
				winner=account_2,
				loser=account_1,
				winning_score=score_2,
				losing_score=score_1)
		new_game.save()
		