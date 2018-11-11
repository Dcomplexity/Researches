This is a research project.

The project is more about multiagent reinforcement learning and evolutionary game theory.

Here I want to test the git settings. If there is something with the "crlf" on windows and "lf" on linux.

# Learn_Imitate
个体在复杂网络中，update 自己 strategy 的时候，不光可以通过模仿别人的策略，应该还可以通过强化学习等手段，自己学习出策略的 value，来更新自己的策略。

# Repuation Model
个体在每回合博弈开始阶段都有一个初始值为1的 Reputation。当个体在上一轮博弈中使用了背叛策略时，这个 Reputattion 值会下降。下降的大小与他周围邻居中的合作者比例有关系。
$$
r_{i} = r_{i} - r_{i} * n_c / n
$$

# Mul_Agent_rl_Grid_World
在多智能体实验中，个体不仅可以向以前的自己学习（reinforcement learning)，还可以向其他个体吸取经验，这个过程可不可以在多智能体强化学习的环境中，有更好的效果呢。

# Mul_Agent_rl_zd_Strategy
探讨多只能强化学习与 ZD Strategy 结合的可能性。

# Social_Structure_and_Game_Theory
Social Distance 可以促进合作。在这个模型的基础上探讨，惩罚与合作，reputation的作用。

# Stochastic_Evolutionary_Game
Nowak 2018 年的文章 Evolution of cooperation in stochastic game. python 复现。
