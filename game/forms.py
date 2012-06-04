from django import forms
from game.models import Game, Account
from django.contrib.auth.models import User

class GameForm(forms.Form):
    player_1 = forms.ModelChoiceField(label="Player 1", queryset=Account.objects.order_by('handle'), empty_label="Select Player 1")
    player_2 = forms.ModelChoiceField(label="Player 2", queryset=Account.objects.order_by('handle'), empty_label="Select Player 2")
    score_1 = forms.IntegerField(label="Player 1's Score", max_value=99, min_value=0, widget=forms.TextInput(attrs={'style':'width:50px'}))
    score_2 = forms.IntegerField(label="Player 2's score", max_value=99, min_value=0, widget=forms.TextInput(attrs={'style':'width:50px'}))


    def clean(self):
        try:
            if self.cleaned_data['player_1'] == self.cleaned_data['player_2']:
                raise forms.ValidationError("Player 1 and Player 2 cannot be the same!")
            return self.cleaned_data
        except KeyError:
            pass

    def process(self):
        account_1 = self.cleaned_data['player_1']
        account_2 = self.cleaned_data['player_2']
        score_1 = self.cleaned_data['score_1']
        score_2 = self.cleaned_data['score_2']

        if account_1.rank > account_2.rank:
            upset = True
        else:
            upset = False

        new_game = Game(
            winner=account_1,
            loser=account_2,
            winning_score=score_1,
            losing_score=score_2,
            upset=upset
        )
        new_game.save()
