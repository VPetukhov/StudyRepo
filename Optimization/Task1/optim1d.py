import numpy as np


def counted(fn):
    def wrapper(*args, **kwargs):
        wrapper.called+= 1
        return fn(*args, **kwargs)
    wrapper.called= 0
    wrapper.__name__= fn.__name__
    return wrapper


@counted
def f_with_count(func, x):
    return func(x)


def min_golden(func, a, b, tol=1e-5, max_iter=500, disp=False, trace=False):
    gold_sec = (5**0.5 - 1) / 2
    success = False
    x_values, f_values, n_evals = [], [], []
    f_with_count.called = 0
    func_cnt = lambda x: f_with_count(func, x)

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
            n_evals.append(f_with_count.called)

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
    f_with_count.called = 0
    func_cnt = lambda x: f_with_count(func, x)
    success = False

    f_a = func_cnt(a)
    f_b = func_cnt(b)

    x_mid = (a + b) / 2
    f_mid = func_cnt(x_mid)

    if f_mid > f_a and f_mid > f_b:
        return a, f_a if f_a < f_b else b, f_b#TODO

    for iter_num in range(max_iter):
        if disp:
            print("%d: Xa=%.7f,  Xb=%.7f,  Xmid=%.7f,  Fmid=%.7f" % (iter_num, a, b, x_mid, f_mid))

        if b - a < tol:
            success = True
            break

        if trace:
            x_values.append(x_mid)
            f_values.append(f_mid)
            n_evals.append(f_with_count.called)

        params = np.linalg.solve([[a ** 2, a, 1], [x_mid ** 2, x_mid, 1], [b ** 2, b, 1]], [f_a, f_mid, f_b])
        parabolic_min = -params[1] / (2 * params[0])
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
    gold_sec = (5**0.5 - 1) / 2
    success = False
    x_values, f_values, n_evals = [], [], []
    f_with_count.called = 0
    func_cnt = lambda x: f_with_count(func, x)

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
            n_evals.append(f_with_count.called)

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