from poker_engine import poker_engine
from poker_learner import poker_learner
import numpy as np
class game():
    def __init__(self):
        self.big_blind = 100
        self.training_iterations = 99999900
        self.players = [poker_learner()]
        for i in range(8):
            self.players.append(poker_learner(learners=self.players[0].learners))
        self.engine = poker_engine()
        self.folded = []
        self.num_players = 9
        self.verbose = True
        for player in self.players:
            player.big_blind = self.big_blind
    def train(self):
        for i in range(self.training_iterations):
            self.num_players = np.random.randint(3, 9)
            self.folded = []
            self.engine.init_game_for(self.num_players)
            self._train_iteration()
            if i % 100 == 0:
                self.players[0].save()
                if self.verbose: print "Reached Iteration " + str(i)
    def _show_flop(self):
        for i in range(self.num_players):
            self.players[i].flop_shown(self.engine.flop)
    def _show_turn(self):
        for i in range(self.num_players):
            self.players[i].turn_shown(self.engine.turn)
    def _show_river(self):
        for i in range(self.num_players):
            self.players[i].river_shown(self.engine.river)
    def _declare_winner(self):
        winner = self.engine.get_winner(self.folded)
        for i in range(self.num_players):
            if i in self.folded:
                continue
            reward = self.players[i].invested
            if i == winner:
                self.players[i].reward(self.players[i].pot)
            else:
                self.players[i].reward(reward*-1)

    def _train_iteration(self):
        for player in range(self.num_players):
            self.players[player].num_players = self.num_players
            self.players[player].new_hand(self.engine.get_hand_for_player(player), player)
            self.players[player].raises(1, self.big_blind / 2)
            self.players[player].raises(2, self.big_blind)

        # preflop
        if self._round_loop(2,self.big_blind):
            self._show_flop()
            if self._round_loop(0,0):
                self._show_turn()
                if self._round_loop(0,0):
                    self._show_river()
                    if self._round_loop(0,0):
                        self._declare_winner()
            return
    def _round_loop(self,end_on, current_bet):
        '''

        :param end_on:
        :return: False if game ended
        '''
        last_to_go = end_on
        on_player = last_to_go + 1
        round_still_on = True
        need_to_call = current_bet
        while round_still_on:
            if self._is_game_over():
                self._hand_out_rewards_all_folded()
                return False
            if on_player in self.folded:
                round_still_on = last_to_go == on_player
                on_player = self._increment_player(on_player)
                continue
            action = self.players[on_player].act()
            new_need_to_call = self._take_action(need_to_call - self.players[on_player].invested, on_player, action)
            round_still_on = last_to_go != on_player
            if new_need_to_call != need_to_call:
                last_to_go = self._decrement_player(on_player)
            on_player = self._increment_player(on_player)
        return True
    def _increment_player(self, player):
        n = player + 1
        if n >= self.num_players:
             n = 0
        return n
    def _decrement_player(self, player):
        n = player -1
        if player < 0:
            n = self.num_players - 1
        return n

    def _is_game_over(self):
        return len(self.folded) +1 == self.num_players
    def _hand_out_rewards_all_folded(self):
        for i in range(self.num_players):
            reward = self.players[i].invested
            if i not in self.folded:
                self.players[i].reward(self.players[i].pot)
                return

    def folds(self, player):
        self.folded.append(player)
        self.players[player].reward(self.players[player].invested * -1)
        for i in range(self.num_players):
            self.players[i].folds()

    def calls(self, player, amount):
        self.players[player].invested += amount
        for i in range(self.num_players):
            self.players[i].calls(amount)

    def raises(self, player, amount):
        self.players[player].invested += amount
        for i in range(self.num_players):
            self.players[player].raises(player,amount)

    def _take_action(self, need_to_call, player, action):
        if action == 0:
            self.folded.append(player)
            self.players[player].reward(self.players[player].invested * -1)
            for i in range(self.num_players):
                self.players[i].folds()
            return need_to_call
        if action == 1:
            if need_to_call > 0:
                self.folds(player)
                return need_to_call

        if action == 2:
            self.players[player].invested += need_to_call
            self.calls(player,need_to_call)
            return need_to_call

        raise_to = 0
        if action < 11:
            raise_to = need_to_call + self.players[player].pot * (action - 2) / 10
        else:
            raise_to = need_to_call + self.players[player].pot * (action - 11)
        if raise_to > 0:
            self.raises(player,raise_to)
            return  raise_to
        return need_to_call
g = game()
g.train()