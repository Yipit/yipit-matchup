from django.contrib import admin
from game.models import Game, Account


class GameAdmin(admin.ModelAdmin):
    list_display = ('date', 'winner', 'loser', 'winning_score', 'losing_score',)
    list_per_page = 100
    search_fields = ['winner__handle', 'loser__handle']

admin.site.register(Game, GameAdmin)
admin.site.register(Account)