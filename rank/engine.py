import math

from game.models import Account
from rank.models import RankLog


class RankEngine(object):

    def __init__(self, game, force=False):
        self.game = game
        self.force = force

    def compute_scores(self):
        if not self.game.ranked or self.force:
            winner, loser = self.game.winner, self.game.loser
            rank_difference = winner.rank - loser.rank

            #should be rewarded more for beating a better player
            #should be punished more for losing to a worse player
            #e.g. rank 5 player beats rank 3
            if math.fabs(rank_difference)>2:
                if rank_difference > 0:
                    multiplier = -1 * rank_difference
                    winner.score += rank_difference * 50
                    loser.score += multiplier * 50
                
                # losing party should not be punished extremely
                # nor should the winning party be rewarded greatly
                # the greater the difference, the less the impact
                #e.g. rank 3 player beats rank 5, rank_difference = -2
                else:
                    winner.score += (-1/ rank_difference) * 200
                    loser.score += (1 /rank_difference) * 200
            else:
                winner.score += 50
                loser.score -= 50

            winner.save()
            loser.save()

            self.update_ranking()
            return True

    def update_ranking(self):
        score_list = [(account, float(account.score)) for account in Account.objects.all()]
        account_list_sorted_by_score = sorted(score_list, key=lambda x: x[1], reverse=True)
        ordered_account_list = list(map(lambda x: x[0], account_list_sorted_by_score))

        counter = 1
        for account in ordered_account_list:
            account.rank = counter
            account.save()

            RankLog.objects.create(player=account, score=account.score, rank=account.rank)
            
            counter += 1 
