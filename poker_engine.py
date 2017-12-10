import numpy as np
from deuces.evaluator import Evaluator
from deuces.card import Card
class poker_engine():
    def __init__(self):
        self.ALL_CARDS = np.array([i for i in range(52)])
        self.hands = []
        self.flop = (-1,-1,-1)
        self.turn = -1
        self.river = -1
        self.eval = Evaluator()

    def init_game_for(self, num_players):
        total_cards_in_use = num_players * 2 + 5
        cards = np.random.choice(self.ALL_CARDS, total_cards_in_use, replace=False)
        self.hands = []
        for i in range(num_players):
            self.hands.append((cards[i*2], cards[i*2+1]))
        self.river = cards[-1]
        self.turn = cards[-2]
        self.flop = (cards[-3],cards[-4],cards[-5])


    def get_hand_for_player(self, i):
        return self.hands[i]

    def _get_deuces_card(self, card):
        card_str = ""
        val = card % 13 + 1
        if val < 10 and val > 1:
            card_str = str(val)
        else:
            if val == 1:
                card_str = "A"
            if val == 10:
                card_str = "T"
            if val == 11:
                card_str = "J"
            if val == 12:
                card_str = "Q"
            if val == 13:
                card_str = "K"

        if card <13:
            card_str += "h"
        elif card < 26:
            card_str += "d"
        elif card < 39:
            card_str += "s"
        else:
            card_str += "c"
        return Card.new(card_str)
    def str_to_card(self,s):
        val = s[0]
        card = 0
        if val == "a":
            card = 0
        elif val == "t":
            card = 9
        elif val == "j":
            card = 10
        elif val == "q":
            card = 11
        elif val == "k":
            card = 12
        else:
            card = int(val) - 1
        suit = s[1]
        if suit == "d":
            card += 13
        if suit == "s":
            card += 26
        if suit == "c":
            card += 39
        return card

    def get_winner(self,folded):
        board = [self._get_deuces_card(i) for i in self.flop]
        board.append(self._get_deuces_card(self.turn))
        board.append(self._get_deuces_card(self.river))
        hands = [
            [self._get_deuces_card(self.hands[h][0]), self._get_deuces_card(self.hands[h][1])]
            for h in range(len(self.hands)) if h not in folded
        ]
        scores = [self.eval.evaluate(h,board) for h in hands]
        winner = np.argmin(scores)
        return winner
