from cube_2 import RubiksCube
import numpy as np

env = RubiksCube()
s = env.reset()
num_actions = env.num_actions

d = False
reward = 0.0
while not d:
    a = np.random.randint(num_actions)
    s, r, d, _ = env.step(a)
    reward += r

print('Total reward = %d' % (reward))
