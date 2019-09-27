import unittest

import numpy as np

from longstaff_schwartz.binomial import BinomialModel, create_binomial_model


def call_payoff(strike):
    return lambda S: np.maximum(S - strike, 0)


def put_payoff(strike):
    return lambda S: np.maximum(strike - S, 0)


def european_call_price(mdl, strike):
    return mdl.evaluate(call_payoff(strike))


def american_call_price(mdl, strike):
    return mdl.evaluate_american_exercisable(call_payoff(strike))


def european_put_price(mdl, strike):
    return mdl.evaluate(put_payoff(strike))


def american_put_price(mdl, strike):
    return mdl.evaluate_american_exercisable(put_payoff(strike))


class TestBinomial(unittest.TestCase):
    '''Tests for `binomial` package.'''

    def test_binomial(self):
        mdl = create_binomial_model(0.1, 0.02, 100, 1, n=100)
        print(mdl)
        print([float(np.round(european_call_price(mdl, s), 2))
               for s in range(90, 110)])

    def test_thayer_watkins_example(self):
        '''Test example values by Thayer Watkins in
           http://www.sjsu.edu/faculty/watkins/binomial.htm
        '''
        u = 1 + 0.1
        d = 1 - 0.1
        r = np.log(1 + 0.05)  # = 0.05 with discrete compounding
        S0 = 100
        T = 1
        n = 1
        strike = 95
        mdl = BinomialModel(u, d, r, S0, T, n)
        npv = european_call_price(mdl, strike)
        self.assertEqual(10.71, np.round(npv, 2))

    def test_cox_ross_rubinstein_example(self):
        '''Test example values by Cox, Ross, Rubinstein in
           "Option pricing: A simplified approach", chapter 4
        '''
        S0 = 80
        n = 3
        T = 3
        strike = 80
        u = 1.5
        d = 0.5
        r = np.log(1.1)
        mdl = BinomialModel(u, d, r, S0, T, n)
        npv = european_call_price(mdl, strike)
        self.assertEqual(34.080, np.round(npv, 2))  # 34.065 in paper
        expected_payoff = np.array([0, 0, 90 - 80, 270 - 80])
        payoff = call_payoff(strike)(mdl.ST)
        self.assertTrue(np.allclose(expected_payoff, payoff))
        self.assertTrue(np.allclose(0.6, mdl.q))
