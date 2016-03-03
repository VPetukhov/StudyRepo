import numpy as np
from math import sqrt


def _counted(fn):
    def wrapper(*args, **kwargs):
        wrapper.called += 1
        return fn(*args, **kwargs)

    wrapper.called = 0
    wrapper.__name__ = fn.__name__
    return wrapper


@_counted
def _f_with_count(func, x):
    return func(x)


def get_mid(func, a):
    gold_sec = (5 ** 0.5 + 1) / 2
    mult = 100
    b = a + 1
    f_a, f_b = func(a), func(b)
    if f_a < f_b:
        a, b = b, a
        f_a, f_b = f_b, f_a

    x_max = 1e6 * (b - a)

    c = b + (b - a) * gold_sec
    f_c = func(c)

    while f_c < f_b and abs(b) < abs(x_max):
        x_new = _parabolic_step(a, b, c, f_a, f_b, f_c)
        if b < x_new < c:
            f_new = func(x_new)
            if f_new < f_c:
                return b, x_new, c
            if f_new > f_b:
                return a, b, x_new
            x_new = c + (c - b) * gold_sec
            f_new = func(x_new)
        else:
            x_lim = c + (c - b) * mult
            if c < x_new < x_lim:
                f_new = func(x_new)
                if f_new < f_c:
                    b, c, x_new = c, x_new, c + (c - b) * gold_sec
                    f_b, f_c, f_new = c, x_new, func(x_new)
            elif x_new > x_lim:
                x_new, f_new = x_lim, func(x_new)
            else:
                x_new = c + (c - b) * gold_sec
                f_new = func(x_new)

        a, b, c = b, c, x_new
        f_a, f_b, f_c = f_b, f_c, f_new

    return sorted([a, b, c])


def _shift_brent(a, b, x_min, x_min2, x_min3, x_mid, f_min, f_min2, f_min3, f_mid, d_f_min = None, d_f_mid = None):
    if f_mid < f_min:
        if x_mid < x_min:
            b = x_min
        else:
            a = x_min

        x_min, x_min2, x_min3, f_min, f_min2, f_min3, d_f_min = x_mid, x_min, x_min2, f_mid, f_min, f_min2, d_f_mid
    else:
        if x_mid < x_min:
            a = x_mid
        else:
            b = x_mid

        if f_mid <= f_min2 or x_min2 == x_min:
            x_min2, x_min3, f_min2, f_min3 = x_mid, x_min2, f_mid, f_min2
        elif f_mid <= f_min3 or x_min3 == x_min2:
            x_min3, f_min3 = x_mid, f_mid

    if d_f_mid is None:
        return a, b, x_min, x_min2, x_min3, f_min, f_min2, f_min3

    return a, b, x_min, x_min2, x_min3, f_min, f_min2, f_min3, d_f_min


def _parabolic_step(x1, x2, x3, f1, f2, f3):
    params = np.linalg.solve([[x1 ** 2, x1, 1], [x2 ** 2, x2, 1], [x3 ** 2, x3, 1]], [f1, f2, f3])
    return -params[1] / (2 * params[0])


def _parabolic_step_der(x1, x2, f1, f2, d_f1):
    params = np.linalg.solve([[x1 ** 2, x1, 1], [x2 ** 2, x2, 1], [2 * x1, 1, 0]], [f1, f2, d_f1])
    return -params[1] / (2 * params[0])


def min_golden(func, a, b, tol=1e-5, max_iter=500, disp=False, trace=False):
    gold_sec = (5 ** 0.5 - 1) / 2
    success = False
    x_values, f_values, n_evals = [], [], []
    _f_with_count.called = 0

    def func_cnt(x): return _f_with_count(func, x)

    step_size = (b - a) * gold_sec
    new_a = b - step_size
    new_b = a + step_size
    f_na = func_cnt(new_a)
    f_nb = func_cnt(new_b)
    for iter_num in range(max_iter):
        if disp:
            print("%d: Xa=%.7f,  Xb=%.7f,  XU=%.7f,  XL=%.7f, FU=%.7f, FL=%.7f" %
                  (iter_num, a, b, new_a, new_b, f_na, f_nb))

        if step_size < tol:
            success = True
            break

        if trace:
            x_min, f_min = (new_a, f_na) if f_na < f_nb else (new_b, f_nb)
            x_values.append(x_min)
            f_values.append(f_min)
            n_evals.append(_f_with_count.called)

        step_size *= gold_sec
        if f_na < f_nb:
            b = new_b
            new_b = new_a
            f_nb = f_na
            new_a = b - step_size
            f_na = func_cnt(new_a)
        else:
            a = new_a
            new_a = new_b
            f_na = f_nb
            new_b = a + step_size
            f_nb = func_cnt(new_b)

    x_min, f_min = (new_a, f_na) if f_na < f_nb else (new_b, f_nb)
    ret_list = [x_min, f_min, (0 if success else 1)]
    if trace:
        hist = {'x': np.array(x_values), 'y': np.array(f_values), 'n_evals': np.array(n_evals)}
        ret_list.append(hist)

    return ret_list


def min_parabolic(func, a, b, tol=1e-5, max_iter=500, disp=False, trace=False):
    x_values, f_values, n_evals = [], [], []
    _f_with_count.called = 0
    success = False

    def func_cnt(x):
        return _f_with_count(func, x)

    f_a = func_cnt(a)
    f_b = func_cnt(b)

    x_mid = (a + b) / 2
    f_mid = func_cnt(x_mid)

    for iter_num in range(max_iter):
        if disp:
            print("%d: Xa=%.7f,  Xb=%.7f,  Xmid=%.7f,  Fmid=%.7f" % (iter_num, a, b, x_mid, f_mid))

        if b - a < tol:
            success = True
            break

        if trace:
            x_values.append(x_mid)
            f_values.append(f_mid)
            n_evals.append(_f_with_count.called)

        parabolic_min = _parabolic_step(a, x_mid, b, f_a, f_mid, f_b)
        f_pm = func_cnt(parabolic_min)
        if parabolic_min < x_mid:
            b, f_b = x_mid, f_mid
        else:
            a, f_a = x_mid, f_mid

        x_mid, f_mid = parabolic_min, f_pm

    ret_list = [x_mid, f_mid, (0 if success else 1)]
    if trace:
        hist = {'x': np.array(x_values), 'y': np.array(f_values), 'n_evals': np.array(n_evals)}
        ret_list.append(hist)

    return ret_list


def min_brent(func, a, b, tol=1e-5, max_iter=500, disp=False, trace=False):
    gold_sec = (5 ** 0.5 - 1) / 2
    success = False
    x_values, f_values, n_evals = [], [], []
    _f_with_count.called = 0
    prev_stepsize = b - a

    def func_cnt(x): return _f_with_count(func, x)

    x_min = (a + b) / 2
    f_min = func_cnt(x_min)
    x_min2 = x_min3 = x_min
    f_min2 = f_min3 = f_min
    for iter_num in range(max_iter):
        preprev_stepsize, prev_stepsize = prev_stepsize, b - a

        if (b - a) < tol:
            success = True
            break

        applied = False
        if not (f_min == f_min2 or f_min == f_min3 or f_min2 == f_min3):
            x_mid = _parabolic_step(x_min, x_min2, x_min3, f_min, f_min2, f_min3)
            applied = b - tol > x_mid > a + tol and abs(x_min - x_mid) < preprev_stepsize

        if not applied:
            x_mid = x_min + gold_sec * (b - x_min) if x_min < (b - a) / 2 else a + gold_sec * (x_min - a)

        a, b, x_min, x_min2, x_min3, f_min, f_min2, f_min3 = _shift_brent(
            a, b, x_min, x_min2, x_min3, x_mid, f_min, f_min2, f_min3, func_cnt(x_mid))

        if trace:
            x_values.append(x_min)
            f_values.append(f_min)
            n_evals.append(_f_with_count.called)

        if disp:
            print("%d: a=%.7f,  b=%.7f,  x=%.7f, w=%.7f, w=%.7f, f_min=%.7f, step type: %s" %
                  (iter_num, a, b, x_min, x_min2, x_min3, f_min, "parabolic" if applied else "golden"))

    ret_list = [x_min, f_min, (0 if success else 1)]
    if trace:
        hist = {'x': np.array(x_values), 'y': np.array(f_values), 'n_evals': np.array(n_evals)}
        ret_list.append(hist)

    return ret_list


def min_cubic(func, a, b, tol=1e-5, max_iter=500, disp=False, trace=False):
    x_values, f_values, n_evals = [], [], []
    _f_with_count.called = 0
    success = False

    def func_cnt(x):
        return _f_with_count(func, x)

    f_a, d_f_a = func_cnt(a)
    f_b, d_f_b = func_cnt(b)

    for iter_num in range(max_iter):
        if disp:
            print("%d: Xa=%.7f,  Xb=%.7f, Fa=%.7f, Fb=%.7f, dFa=%.7f, dFb=%.7f" % (iter_num, a, b, f_a, f_b, d_f_a, d_f_b))

        if b - a < tol:
            success = True
            break

        if trace:
            if f_a < f_b:
                x_values.append(a)
                f_values.append(f_a)
            else:
                x_values.append(b)
                f_values.append(f_b)
            n_evals.append(_f_with_count.called)

        a3, a2, a1, a0 = np.linalg.solve([[a ** 3, a ** 2, a, 1], [b ** 3, b ** 2, b, 1],
                                  [3 * a ** 2, 2 * a, 1, 0], [3 * b ** 2, 2 * b, 1, 0]],
                                 [f_a, f_b, d_f_a, d_f_b])

        def f_cub(x):
            return a0 + a1*x + a2*x**2 + a3*x**3, a1 + 2 * a2*x + 3 * a3*x**2
        cubic_min = (-2 * a2 + 2 * sqrt(a2 ** 2 - 3 * a3 * a1)) / (6 * a3)
        f_cm, d_f_cm = func_cnt(cubic_min)
        if d_f_cm > 0:
            b, f_b, d_f_b = cubic_min, f_cm, d_f_cm
        else:
            a, f_a, d_f_a = cubic_min, f_cm, d_f_cm

        if abs(d_f_cm) < tol:
            break

    ret_list = [a, f_a, (0 if success else 1)]
    if trace:
        hist = {'x': np.array(x_values), 'y': np.array(f_values), 'n_evals': np.array(n_evals)}
        ret_list.append(hist)

    return ret_list


def min_brent_der(func, a, b, tol=1e-5, max_iter=500, disp=False, trace=False):
    success = False
    x_values, f_values, n_evals = [], [], []
    _f_with_count.called = 0
    prev_stepsize = b - a

    def func_cnt(x): return _f_with_count(func, x)

    x_min = (a + b) / 2
    (f_min, d_f_min) = func_cnt(x_min)

    x_min2 = x_min3 = x_min
    f_min2 = f_min3 = f_min
    for iter_num in range(max_iter):
        preprev_stepsize, prev_stepsize = prev_stepsize, b - a

        if (b - a) < tol:
            success = True
            break

        applied = False
        if f_min != f_min2:
            x_mid = _parabolic_step_der(x_min, x_min2, f_min, f_min2, d_f_min)
            applied = b - tol > x_mid > a + tol and abs(x_min - x_mid) < preprev_stepsize and \
                      d_f_min * (x_mid - x_min) < 0

        if f_min != f_min3:
            x_mid_2 = _parabolic_step_der(x_min, x_min3, f_min, f_min3, d_f_min)
            if b - tol > x_mid_2 > a + tol and abs(x_min - x_mid_2) < preprev_stepsize and \
                d_f_min * (x_mid_2 - x_min) < 0 and (not applied or abs(x_mid_2 - x_min) < abs(x_mid - x_min)):
                x_mid = x_mid_2
                applied = True

        if not applied:
            x_mid = ((a + x_min) / 2) if d_f_min > 0 else ((x_min + b) / 2)

        f_mid, d_f_mid = func_cnt(x_mid)
        a, b, x_min, x_min2, x_min3, f_min, f_min2, f_min3, d_f_min = _shift_brent(
            a, b, x_min, x_min2, x_min3, x_mid, f_min, f_min2, f_min3, f_mid, d_f_min, d_f_mid)

        if trace:
            x_values.append(x_min)
            f_values.append(f_min)
            n_evals.append(_f_with_count.called)

        if disp:
            print("%d: a=%.7f,  b=%.7f,  x=%.7f, w=%.7f, w=%.7f, f_min=%.7f, step type: %s" %
                  (iter_num, a, b, x_min, x_min2, x_min3, f_min, "parabolic" if applied else "bisection"))

        if abs(d_f_mid) < tol:
            break

    ret_list = [x_min, f_min, (0 if success else 1)]
    if trace:
        hist = {'x': np.array(x_values), 'y': np.array(f_values), 'n_evals': np.array(n_evals)}
        ret_list.append(hist)

    return ret_list