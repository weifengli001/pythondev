from sklearn import svm, grid_search
import numpy as np
from sklearn import datasets

digits = datasets.load_digits()

gammas = np.logspace(-6, -1, 10)
svc = svm.SVC()
clf = grid_search.GridSearchCV(estimator=svc,param_grid=dict(gamma=gammas), n_jobs=-1, refit=True)

clf.fit(digits.data[:1000], digits.target[:1000])

print(clf.best_score_)
print(clf.best_params_)
print(clf.best_estimator_.gamma)