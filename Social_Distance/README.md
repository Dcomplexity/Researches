Social Distance 可以促进合作。在这个模型的基础上探讨，惩罚与合作，reputation的作用。

# New_Value_From_-3_To_-3
当 social distance 的参数设置为 -3 到 3 的时候，探讨 play game distace he update strategy distance 两个参数对 cooperation 的影响。

# Add_Punishers
加入第三种策略，惩罚策略，即惩罚着选择合作，但是他们回去惩罚背叛者，同时自己也会承担惩罚的成本。在这个实验中，背叛者，合作者，惩罚者的初始比例为 0.5:0.25:0.25

# Reputation
每个个体会有一个 Reputation 值，这个 Reputation 值是他们所在的 community 的合作者比例。Reputation 越高的那个 community 越容易被选出来，产生 opponent。

# Reputation_Distance
两个 Reputation 越相近的 community 越容易被选出来。

# Reputation_re
每个个体的 Reputation 为他们所在的 community 的合作者比例。当一个个体选出一个 opponent 时。他们俩之间愿意进行一次博弈的概率与他们的 reputation 有关
$$
\frac{1}{1 + e^{-(r_i * r_j * 4)}}
$$

