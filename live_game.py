from poker_learner import poker_learner
from QLearner import QLearner
from poker_learner import poker_learner
learners = []
for i in range(4):
    f = open("./learners/" + str(i),'r')
    learners.append(QLearner())
    learners[i].Q = eval(f.read())
    f.close()
p = poker_learner(learners=learners)

