import math

from game.models import Account
from rank.models import RankLog

SPREAD_TO_POINTS_EXCHANGED = {
    1: (8, 8),
    2: (7, 10),
    3: (6, 13),
    4: (5, 16),
    5: (4, 20),
    6: (3, 25),
    7: (2, 30),
    8: (2, 35),
    9: (1, 40),
    10: (1, 45),
    11: (0, 50)
}

class RankEngine(object):

    def __init__(self, game=None):
        self.game = game
        if self.game:
            self.winner = self.game.winner
            self.loser = self.game.loser
            self.winning_score = self.game.winning_score
            self.losing_score = self.game.losing_score


    def _compute_spread(self):
        self.spread = self.winner.rating - self.loser.rating
        
        if self.spread > 0:
            self.upset = False
        else:
            self.upset = True

    def update_scores(self):
        self._compute_spread()
        self.spread = math.fabs(self.spread)

        if self.spread < 13:
            index = 1
        elif self.spread < 38:
            index = 2
        elif self.spread < 63:
            index = 3
        elif self.spread < 88:
            index = 4
        elif self.spread < 113:
            index = 5
        elif self.spread < 138:
            index = 6
        elif self.spread < 163:
            index = 7
        elif self.spread < 188:
            index = 8
        elif self.spread < 213:
            index = 9
        elif self.spread < 238:
            index = 10
        else:
            index = 11

        if self.upset:
            upset_indicator = 1
        else:
            upset_indicator = 0

        self.winner.rating += SPREAD_TO_POINTS_EXCHANGED[index][upset_indicator]
        self.loser.rating -= SPREAD_TO_POINTS_EXCHANGED[index][upset_indicator]

        self.winner.save()
        self.loser.save()

        self._update_ranking()

        return True


    def _update_ranking(self):
        rating_list = [(account, float(account.rating)) for account in Account.objects.all()]
        account_list_sorted_by_rating = sorted(rating_list, key=lambda x: x[1], reverse=True)
        ordered_account_list = list(map(lambda x: x[0], account_list_sorted_by_rating))

        counter = 1
        for account in ordered_account_list:
            account.rank = counter
            account.save()

            RankLog.objects.create(player=account, rating=account.rating, rank=account.rank)
            
            counter += 1
            



    # def compute_scores(self):
    #     if not self.game.ranked or self.force:
    #         winner, loser = self.game.winner, self.game.loser
    #         rank_difference = winner.rank - loser.rank

    #         if math.fabs(rank_difference)>2:
    #             if rank_difference > 0:
    #                 multiplier = -1 * rank_difference
    #                 winner.score += rank_difference * 50
    #                 loser.score += multiplier * 50
    #             else:
    #                 winner.score += (-1/ rank_difference) * 200
    #                 loser.score += (1 /rank_difference) * 200
    #         else:
    #             winner.score += 50
    #             loser.score -= 50

    #         winner.save()
    #         loser.save()

    #         self.update_ranking()
    #         return True


