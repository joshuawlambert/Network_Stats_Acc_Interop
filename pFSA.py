import pandas
import sklearn
import sklearn.preprocessing
import sklearn.linear_model
import numpy as np
import random
import itertools
from time import time
#import seaborn
#from matplotlib import pyplot as plt


def snp_fsa_logistic(X, y, n=3, initial_cols=None, minmax='max'):
    if minmax=='max':
        mm_fn = max
    elif minmax=='min':
        mm_fn = min

    cols = list(X.columns)
    current_cols = list(random.sample(cols, n))
    results = {tuple(sorted(current_cols)): evaluate(X[current_cols], y)[1]}
    runs = 0
    curmax, lastmax = 0, 0


        runs += 1
        lastmax = curmax
        curmax = mm_fn(results.values())


def score(model, X, y, method=None):
    return model.score(X, y)


def evaluate(X, y, degree=2):
    poly = sklearn.preprocessing.PolynomialFeatures(degree, interaction_only=True)
    model = sklearn.linear_model.LogisticRegression(solver='liblinear', fit_intercept=True)
    with_int = poly.fit_transform(X)
    model = model.fit(with_int, y)
    return model, score(model, with_int, y)


def gen_random(snps=500, samples=200):
    random_snps = pandas.DataFrame(np.random.randint(0, 2, (samples, snps), int),
                                   index=range(200),
                                   columns=['rs'+str(i) for i in range(snps)])
    phenotypes = np.random.randint(0, 2, 200, int)
    return random_snps, phenotypes

if __name__ == '__main__':
    random_snps, phenotypes = gen_random(snps=int(100))
    scores, rounds = [], []
    times = []
    for i in range(10):
        t = time()
        fsa = snp_fsa_logistic(random_snps, phenotypes, n=3)
        dur = time() - t
        scores.append(fsa[0][1])
        rounds.append(fsa[1])
        times.append(dur)
        print(i, dur)


    for i in np.logspace(1, 3, 20):
        random_snps, phenotypes = gen_random(int(i))
        t = time()
        snp_fsa_logistic(random_snps, phenotypes, n=3)
        print(i, time()-t)
