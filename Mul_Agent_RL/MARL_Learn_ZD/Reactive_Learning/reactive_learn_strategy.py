import numpy as np
import random
import matplotlib.pyplot as plt

p_init_strategy = 0.5


# In this work, 0 for cooperate, 1 for defect
def pd_game(a_x, a_y, r, s, t, p):
    if a_x == 0 and a_y == 0:
        return r, r
    elif a_x == 0 and a_y == 1:
        return s, t
    elif a_x == 1 and a_y == 0:
        return t, s
    elif a_x == 1 and a_y == 1:
        return p, p
    else:
        return "error"
