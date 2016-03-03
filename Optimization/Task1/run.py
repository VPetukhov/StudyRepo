from optim1d import *
from scipy.optimize import check_grad, optimize
import matplotlib.pyplot as plt


def func_a(x):
    return -5 * x**5 + 4 * x**4 - 12 * x**3 + 11 * x**2 - 2 * x + 1

def d_func_a(x):
    return -5 * x**5 + 4 * x**4 - 12 * x**3 + 11 * x**2 - 2 * x + 1, -25 * x**4 + 16 * x**3 - 36 * x**2 + 22 * x - 2


def check_df(f, x0):
    if check_grad(lambda x: f(x[0])[0], lambda x: f(x[0])[1], [x0]) > 1e-6:
        raise Exception("Bad gradient")

def main():
    check_df(d_func_a, 11)
    # x_min, f_min, code, hist = min_golden(func_a, -0.5, 0.5, disp=True, trace=True)
    min_parabolic(func_a, -0.5, 0.5, disp=True, trace=True)
    # print(hist['n_evals'])

    x_vals = np.arange(-0.5, 0.5, 0.01)
    plt.plot(x_vals, [func_a(x) for x in x_vals])
    plt.grid(True)
    plt.show()
    # optimize.golden(func_a, brack=[0, 1], full_output=True)


if __name__ == '__main__':
    main()