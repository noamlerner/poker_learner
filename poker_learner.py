from QLearner import QLearner
from hand_state import hand_state
import numpy as np
class poker_learner():
    def __init__(self,learners=None):
        self.cards = [i for i in range(52)]
        # fold, check, call, they can raise any tenth of the pot, or up to 10x the pot
        num_actions = 22
        #  pre-flop, flop, turn, river
        if learners is None:
            self.learners = [
                QLearner(num_actions=num_actions),
                QLearner(num_actions=num_actions),
                QLearner(num_actions=num_actions),
                QLearner(num_actions=num_actions)
            ]
        else:
            self.learners = learners
        self.state = hand_state()
        self.num_players = 0
        self.big_blind = -1
        self.choices = [[],[],[],[]]
        self.pot = 0
        self.invested = 0

    def new_hand(self, my_cards, turn_to_bet):
        self.pot = 0
        self.invested = 0
        self.turn_to_bet = turn_to_bet
        state = hand_state()
        state.num_players = self.num_players
        state.turn_to_bet = self.turn_to_bet
        state.cards = my_cards
        state.pot = 0
        self.num_in_game = self.num_players
        self.choices = [[],[],[],[]]
        self.state = state

    def _get_pot_state(self,amount):
        a = int(amount / self.big_blind)
        if a > 9999:
            a = 9999
        return a
    def _add_to_pot(self, amount):
        self.pot += amount
        self.state.pot = self._get_pot_state(self.pot)

    def _get_raise_state(self, amount):
        if self.pot == 0:
            self.pot = amount
        a = float(amount)/self.pot
        if a < 1:
            return int(a * 10)
        elif a == 1:
            return 10
        else:
            a = int(a) + 10
            if a > 999:
                a = 999
            return a

    def raises(self, player, amount):
        self._add_to_pot(amount)
        self.state.raises.append((player,self._get_raise_state(amount)))

    def calls(self, amount):
        self._add_to_pot(amount)

    def folds(self):
        self.state.num_in_game-=1

    def flop_shown(self,flop):
        self.state.flop = flop

    def turn_shown(self, turn):
        self.state.turn = turn

    def river_shown(self, river):
        self.state.river =river

    def act(self):
        state = self.state.get_state()
        action = -1
        if self.state.flop[0] < 0:
            action = self.learners[0].querystate(state)
            self.choices[0].append((state,action))
        elif self.state.turn < 0:
            action = self.learners[1].querystate(state)
            self.choices[1].append((state,action))
        elif self.state.river < 0:
            action = self.learners[2].querystate(state)
            self.choices[2].append((state,action))
        else:
            action = self.learners[3].querystate(state)
            self.choices[3].append((state, action))
        return action

    def reward(self, reward):
        for i in range(4):
            for choice in self.choices[i]:
                self.learners[i].reward(choice[0], choice[1], reward)

    def save(self):
        for i in range(4):
            f = open("learners/" + str(i),'w+')
            f.write(str(self.learners[i].Q))
            f.close()

    def load(self):
        for i in range(4):
            f = open("./learners/" + str(i), 'r')
            self.learners[i].Q = eval(f.read())
            f.close()
