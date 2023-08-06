from sklearn.linear_model import LinearRegression
import numpy as np
n = 10
p = 3
z = np.random.normal(0, 1, size=(n, p))
y = z[:,p-1]
x = z[:,:p-1]
print(x.shape, y.shape)
C =
cov_matrix = np.cov(z)
beta_hat = np.linalg.solve(a, b)
print(beta_hat)
print(np.mean(y - np.dot(x, beta_hat)))
print(LinearRegression().fit(x, y).coef_)