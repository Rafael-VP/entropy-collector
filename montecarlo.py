import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import statistics as st


matplotlib.rcParams['agg.path.chunksize'] = 10000


def monte_carlo(seeds, fx="x**2", a=0, b=1, n=300):
    f = eval("lambda x: " + fx)

    plt_vals = []
    x_vals = []
    y_vals = []

    # for i in range(a, b, 1000):
    #   x_vals.append(i)

    for i in np.arange(0, 1, 0.01):
        x_vals.append(i)

    for i in x_vals:
        i = (f)(i)
        y_vals.append(i)

    for i in range(n):
        ar = np.zeros(n)

        for i in range(len(ar)):
            np.random.seed(seeds[0])
            seeds.pop(0)
            ar[i] = np.random.uniform(a, b)

        integral = 0.0

        for i in ar:
            # integral += f(i)
            integral += (f)(i)

        ans = (b-a)/float(n)*integral

        plt_vals.append(ans)

    plt.title(f"Function: {fx}")
    plt.plot(x_vals, y_vals)
    plt.show()

    plt.title("Distribution of areas calculated")
    plt.hist(plt_vals, bins=30, ec="black")
    plt.xlabel("Areas")
    plt.show()
    print(f"Mean: {st.mean(plt_vals)}\nGeometric Mean:{st.geometric_mean(plt_vals)}\nHarmonic Mean: {st.harmonic_mean(plt_vals)}\nMedian: {st.median(plt_vals)}\nMode: {st.mode(plt_vals)}\nVariance: {st.variance(plt_vals)}\nStandard Deviation:{st.stdev(plt_vals)}")

    return seeds


def monte_carlo_trig(seeds, fx="sin", a=0, b=np.pi, n=300):
    f = eval("lambda x: np." + fx + "(x)")
    plt_vals = []

    for i in range(n):
        ar = np.zeros(n)

        for i in range(len(ar)):
            np.random.seed(seeds[0])
            seeds.pop(0)
            ar[i] = np.random.uniform(a, b)

        integral = 0.0

        for i in ar:
            integral += (f)(i)

        ans = (b-a) / float(n) * integral

        plt_vals.append(ans)

    plt.title("Distributions of areas calculated")
    plt.hist(plt_vals, bins=30, ec="black")
    plt.xlabel("Areas")
    plt.show()
    print(f"Mean: {st.mean(plt_vals)}\nGeometric Mean:{st.geometric_mean(plt_vals)}\nHarmonic Mean: {st.harmonic_mean(plt_vals)}\nMedian: {st.median(plt_vals)}\nMode: {st.mode(plt_vals)}\nVariance: {st.variance(plt_vals)}\nStandard Deviation:{st.stdev(plt_vals)}")

    return seeds


def monte_carlo_pi(seeds, max_num=10000):
    counter = 0

    for i in range(max_num):
        np.random.seed(int(seeds[0]))
        seeds.pop(0)
        x = np.random.rand(1)
        np.random.seed(int(seeds[0]))
        seeds.pop(0)
        y = np.random.rand(1)

        if y**2+x**2 <= 1:
            counter += 1

    return 4*counter/max_num, seeds
