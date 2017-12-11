"""
Template for implementing QLearner  (c) 2015 Tucker Balch
"""

import numpy as np
import random as rand
class QLearner(object):

    def __init__(self, \
        num_states=100, \
        num_actions = 4, \
        alpha = 0.3, \
        gamma = 0.9, \
        rar = 0.9999999999, \
        radr = 0.999999, \
        verbose = False):
        self.verbose = verbose
        self.num_actions = num_actions
        self.num_states = num_states
        self.alpha = alpha
        self.gamma = gamma
        self.rar = rar
        self.radr = radr
        self.Q = {}

    def querystate(self, s):
        """
        @summary: Update the state without updating the Q-table
        @param s: The new state
        @returns: The selected action
        """
        if s not in self.Q or self._shouldTakeRandomAction():
            a = rand.randint(0, self.num_actions - 1)
        else:
            a = self._bestAction(actions=self.Q[s])
        return a

    def query(self, s):
        if s not in self.Q:
            print "Have Not Seen State"
            a = rand.randint(0, self.num_actions - 1)
        else:
            a = self._bestAction(actions=self.Q[s])
        return a

    def _shouldTakeRandomAction(self):
        self.rar = self.rar * self.radr
        choice =  np.random.choice(2,p=[1-self.rar, self.rar])
        return  choice

    def _bestAction(self, actions):
        takeAction = 0
        for i in range(len(actions)):
            if actions[i] > actions[takeAction]:
                takeAction = i
        return takeAction

    def reward(self, s, a, r):
        if s not in self.Q:
            self.Q[s] = np.zeros(self.num_actions)
        self.Q[s][a] = self._newQValue(s, a, r)

    def _newQValue(self, s, a, r):
        old_value = (1 - self.alpha) * self.Q[s][a]
        new_value = self.alpha * r
        return old_value + new_value


    def author(self):
        return "nlerner3"

