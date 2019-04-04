# The Project Note

## Notes of 'The Social Origins of Networks and Diffusion'

The model of social network formation is based on the premise that people in social networks not only have social ties but also have social identities, which define their proximity or distance from others within a dimension of social life.

### Contention 1

Individuals' social identities are defined by their association with, and participation in, social groups.

### Contention 2

The social distance between individuals $i$ and $j$ , $x_{ij}$, within a dimension of social life is defined as their closest partition level: $x_{ij} = 1$ if $i$ and $j$ belong to the same group, $x_{ij} = 2$ if $i$ and $j$ are both under the next-highest partition, and so forth.

### Contention 3

The probability that a social tie will form between individuals $i$ and $j$ increases with their social proximity. This is modeled by choosing an individual $i$ at random and a distance $x$ with probability $p(x) = ce^{-\alpha x}$, where $\alpha$ is a tunable parameter that controls homophile, and $c$ is a normalizing constant. A node $j$ is then chosen randomly from among all nodes at distance $x$ from $i$.

### Contention 4

Each individual is randomly assigned to a position in dimension $h_{1}$. The correlation between an individual's social positions across dimensions (i.e., social consolidation) is modeled by assigning an individual's social positions in $h_2 — h_H$ at distance $y$ from her position in $h_1$ with the probability $p(y) = ce^{\beta y}$, where $\beta$ is a tunable social consolidation parameter, and $c$ is a normalizing constant.

 









