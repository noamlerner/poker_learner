class hand_state(object):
    # max players = 9
    # pot can be up to 999
    def __init__(self):
        '''
        num_players = number of players at table (max = 9)
        turn_to_bet = your turn at the table to bet (max = 9)
        cards = your cards (max per card = 51)
            heart = 0, diamonds = 1, spades = 2, clubs = 3
            card = suit * 13 + (card value - 1)
        pot = current pot value proportional to big blind (max = 9999)
        raises = an array of tuples, (player_num_at_table, raise proportional to big blind) (max = 999)
        num_in_game = the number of players still in the game
        big_blind = the big blind
        '''
        self.num_players = 0
        self.turn_to_bet = 0
        self.cards = (0,0)
        self.pot = 0
        #             tuples: player_num, raise
        self.raises = []
        self.num_in_game = 0
        self.flop = (-1,-1,-1)
        self.turn = -1
        self.river = -1
    def _card_to_str(self, card):
        if card < 10:
            return "0" + str(card)
        else:
            return str(card)
    def _get_raises_str(self):
            raises = ["000" for i in range(self.num_players)]
            for i in self.raises:
                s = str(i[1])
                while len(s) < 3:
                    s = "0" + s
                raises[i[0]] = s
            return "".join(raises)

    def _get_cards_str(self):
        if self.cards[0] > self.cards[1]:
            self.cards = (self.cards[1],self.cards[0])
        return self._card_to_str(self.cards[0]) + self._card_to_str(self.cards[1])

    def _get_table_str(self):
        s = ""
        cards = []
        if self.flop[0] >= 0:
            cards = list(self.flop)
        if self.turn >= 0:
            cards.append(self.turn)
        if self.river >= 0:
            cards.append(self.river)
        s += self._card_to_str(self.river)
        return "".join([self._card_to_str(i) for i in cards])
    def get_state(self):
        return self._get_table_str() + str(self.num_players) + str(self.turn_to_bet) + self._get_cards_str() \
               + str(self.pot) + self._get_raises_str() + str(self.num_in_game)