from django import forms
from game.models import Game, Account
from django.contrib.auth.models import User
from django.db.models import Q

class GameHistoryForm(forms.Form):
    player_1 = forms.ModelChoiceField(label="Player 1", queryset=Account.objects.order_by('handle'), empty_label="Select Player 1")
    player_2 = forms.ModelChoiceField(label="Player 2", queryset=Account.objects.order_by('handle'), empty_label="Select Player 2", required=False)

    def clean(self):
        try:
            if self.cleaned_data['player_1']== self.cleaned_data['player_2']:
                raise forms.ValidationError("Player 1 and Player 2 cannot be the same!")
            return self.cleaned_data
        except KeyError:
            pass

    def process(self):
        player_1 = self.cleaned_data['player_1']
        player_2 = self.cleaned_data['player_2']
        if not player_2:
            return Game.objects.filter(Q(winner=player_1)|Q(loser=player_1))
        else:
            return Game.objects.filter(Q(winner=player_1, loser=player_2)|Q(winner=player_2, loser=player_1))

        