import statistics as st
import matplotlib.pyplot as plt


def simulate(seeds, amount, rtype):
    results = []

    for i in range(amount):
        results.append(seeds[0] % rtype + 1)
        seeds.pop(0)

    plt.title("Distribution of results")
    plt.hist(results, bins=30, ec="black")
    plt.xlabel("Result")
    plt.ylabel("Type")
    plt.show()

    print(f"Results: {results}")
    print(f"Mean: {st.mean(results)}\nGeometric Mean:{st.geometric_mean(results)}\nHarmonic Mean: {st.harmonic_mean(results)}\nMedian: {st.median(results)}\nMode: {st.mode(results)}\nVariance: {st.variance(results)}\nStandard Deviation:{st.stdev(results)}")

    return seeds
