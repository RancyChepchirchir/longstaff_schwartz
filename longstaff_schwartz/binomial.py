import numpy as np


class BinomialModel:
    '''Simple implementation of Binomial Model (Cox, Ross, Rubinstein 1979)
       for testing purposes.'''

    def __init__(self, u, d, r, S0, T, n):
        self.u = u
        self.d = d
        self.r = r
        self.S0 = S0
        self.T = T
        self.n = n
        self.ST = np.array(list(self.terminal()), dtype='float64')

    def __repr__(self):
        return type(self).__name__ + \
            '(u={u}, d={d}, r={r}, S0={S0}, T={T}, n={n})' \
            .format_map(vars(self))

    @property
    def dt(self):
        return self.T / self.n

    @property
    def q(self):
        return (np.exp(self.r*self.dt) - self.d) / (self.u - self.d)

    def terminal(self):
        S0, u, d, n = self.S0, self.u, self.d, self.n
        for ups in range(n+1):
            yield S0 * u**ups * d**(n-ups)

    def evaluate(self, payoff):
        v = payoff(self.ST)
        q = self.q
        while len(v) > 1:
            v = v[1:]*q + v[:-1]*(1-q)
        return v[0] * np.exp(-self.r * self.T)

    def evaluate_american_exercisable(self, payoff):
        df = np.exp(-self.r * self.dt)
        v = payoff(self.ST)
        s = self.ST
        q = self.q
        while len(v) > 1:
            v = df * (v[1:]*q + v[:-1]*(1-q))
            s = df * (s[1:]*q + s[:-1]*(1-q))
            v = np.maximum(v, payoff(s))
        return v[0]


def create_binomial_model(sigma, r, S0, T, n=10):
    u = np.exp(sigma * np.sqrt(T / n))
    return BinomialModel(u, 1/u, r, S0, T, n)