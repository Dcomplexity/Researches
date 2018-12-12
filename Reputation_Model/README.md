# 1_pd_original
pd, original, 100*100 lattice, 

# 2_pd_reputation
pd, reputation system.
In this work, I set two reputation update method.

+ "decrease_by_step": rep = rep - rep * co_frac
+ "set_frac": rep = co_frac

Two individuals will play the prisoners' dilemma if 
$$
rep\_fre < \frac{1}{1 + 100 * e^{-(rep_i * rep_j) * 8}}
$$
Such reputation system can promote cooperation .

# 3_pgg_original

# 4_pgg_reputation

self_host, reputation

# 4_pgg_reputation

add_other, reputation